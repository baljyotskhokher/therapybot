import os
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = "therapy_bot"
COLLECTION_NAME = "conversations"

_client: MongoClient | None = None


def get_db():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client[DB_NAME]


def _build_chat_log(messages: list[dict]) -> list[dict]:
    now = datetime.now(timezone.utc).isoformat()
    log = []
    for i, msg in enumerate(messages):
        log.append({
            "index": i,
            "role": msg.get("role", "unknown"),
            "content": msg.get("content", ""),
            "timestamp": now,
        })
    return log


def upsert_conversation(session_id: str, messages: list[dict], analysis: dict | None = None) -> None:
    db = get_db()
    collection = db[COLLECTION_NAME]
    set_fields: dict = {
        "session_id": session_id,
        "messages": messages,
        "chat_log": _build_chat_log(messages),
        "message_count": len(messages),
        "updated_at": datetime.now(timezone.utc),
    }
    if analysis:
        set_fields["latest_analysis"] = analysis
        if analysis.get("needs_instant_care"):
            set_fields["needs_instant_care"] = True
            set_fields["instant_care_reason"] = analysis.get("instant_care_reason", "")
    collection.update_one(
        {"session_id": session_id},
        {
            "$set": set_fields,
            "$setOnInsert": {
                "created_at": datetime.now(timezone.utc),
            },
        },
        upsert=True,
    )


def get_conversation(session_id: str) -> list[dict]:
    db = get_db()
    collection = db[COLLECTION_NAME]
    doc = collection.find_one({"session_id": session_id})
    if doc:
        return doc.get("messages", [])
    return []


def delete_conversation(session_id: str) -> None:
    db = get_db()
    collection = db[COLLECTION_NAME]
    collection.delete_one({"session_id": session_id})
