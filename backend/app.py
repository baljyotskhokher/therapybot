import uuid
import os
import inspect
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from llm import get_therapy_response
from db import upsert_conversation, get_conversation, delete_conversation
from analysis import analyze_conversation

BACKEND_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ALERTS_LOG = os.path.join(BACKEND_DIR, "alerts.log")

app = FastAPI(title="Therapy Bot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    analysis: dict | None = None


class ConversationResponse(BaseModel):
    session_id: str
    messages: list[dict]


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Therapy Bot API"}



@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    try:
        history = get_conversation(session_id)
    except Exception:
        history = []

    history.append({"role": "user", "content": req.message})

    try:
        reply = get_therapy_response(history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    history.append({"role": "assistant", "content": reply})

    analysis = {}
    try:
        analysis = analyze_conversation(history)
    except Exception as e:
        print(f"[WARN] Analysis failed: {e}")

    if analysis.get("needs_instant_care"):
        reason = analysis.get("instant_care_reason", "unspecified")
        flags = analysis.get("red_flags", [])
        lines = [
            "",
            "=" * 60,
            f"[!!!]  NEEDS INSTANT CARE  |  session: {session_id}",
            f"    Reason : {reason}",
        ]
        for i, fl in enumerate(flags, 1):
            lines.append(f"    Flag {i}: [{fl.get('severity','?').upper()}] {fl.get('flag')} -- {fl.get('trigger_text','')[:80]}")
        lines.append("=" * 60)
        alert_text = "\n".join(lines)
        print(alert_text, flush=True)
        try:
            with open(ALERTS_LOG, "a", encoding="utf-8") as lf:
                lf.write(f"[{datetime.utcnow().isoformat()}] {alert_text}\n\n")
        except Exception as log_err:
            print(f"[WARN] Could not write alert log: {log_err}", flush=True)

    try:
        upsert_conversation(session_id, history, analysis)
    except Exception as e:
        print(f"[WARN] DB upsert failed: {e}")

    return ChatResponse(session_id=session_id, reply=reply, analysis=analysis)


@app.get("/conversation/{session_id}", response_model=ConversationResponse)
def get_session(session_id: str):
    messages = get_conversation(session_id)
    return ConversationResponse(session_id=session_id, messages=messages)


@app.delete("/conversation/{session_id}")
def clear_session(session_id: str):
    delete_conversation(session_id)
    return {"status": "deleted", "session_id": session_id}
