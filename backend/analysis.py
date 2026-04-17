import json
import re
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

RED_FLAGS = [
    "suicide", "suicidal", "kill myself", "end my life", "want to die",
    "don't want to live", "dont want to live", "self harm", "self-harm",
    "cutting myself", "hurt myself", "overdose", "no reason to live",
    "better off dead", "disappear forever", "can't go on", "cannot go on",
    "give up on life", "end it all", "not worth living",
]

ANALYSIS_PROMPT = """You are a clinical AI assistant analyzing a therapy chat session.
Given the full conversation, return a JSON object with EXACTLY this structure (no markdown, raw JSON only):

{
  "mood": "<one word: calm | anxious | sad | angry | hopeful | distressed | numb | other>",
  "themes": ["<topic1>", "<topic2>"],
  "sentiment_score": <float -1.0 to 1.0>,
  "summary": "<1-2 sentence plain-language summary of what the user is going through>",
  "red_flags": [
    {
      "flag": "<short label e.g. suicidal ideation>",
      "severity": "<low | medium | high | critical>",
      "trigger_text": "<exact quote from user that triggered this flag>",
      "reason": "<brief clinical reason>"
    }
  ],
  "needs_instant_care": <true | false>,
  "instant_care_reason": "<empty string if false, else clear reason why immediate help is needed>"
}

Return ONLY the JSON. No explanation, no markdown fences."""


def _keyword_red_flag_check(message: str) -> dict | None:
    lower = message.lower()
    for flag in RED_FLAGS:
        if flag in lower:
            return {
                "flag": "crisis keyword detected",
                "severity": "critical",
                "trigger_text": message,
                "reason": f"User message contains high-risk phrase: '{flag}'",
            }
    return None


def analyze_conversation(conversation_history: list[dict]) -> dict:
    keyword_flag = None
    for msg in conversation_history:
        if msg.get("role") == "user":
            kf = _keyword_red_flag_check(msg.get("content", ""))
            if kf:
                keyword_flag = kf
                break

    conversation_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in conversation_history
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": ANALYSIS_PROMPT},
                {"role": "user", "content": f"Conversation to analyze:\n\n{conversation_text}"},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=600,
        )
        raw = response.choices[0].message.content.strip()

        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
        analysis = json.loads(raw)

    except Exception as e:
        analysis = {
            "mood": "unknown",
            "themes": [],
            "sentiment_score": 0.0,
            "summary": "Analysis unavailable.",
            "red_flags": [],
            "needs_instant_care": False,
            "instant_care_reason": "",
            "analysis_error": str(e),
        }

    if keyword_flag:
        existing_flags = analysis.get("red_flags", [])
        if not any(f.get("trigger_text") == keyword_flag["trigger_text"] for f in existing_flags):
            existing_flags.insert(0, keyword_flag)
        analysis["red_flags"] = existing_flags
        analysis["needs_instant_care"] = True
        if not analysis.get("instant_care_reason"):
            analysis["instant_care_reason"] = keyword_flag["reason"]

    return analysis
