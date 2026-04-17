# Therapy Bot

A full-stack AI-powered therapy chatbot with real-time crisis detection, conversation analysis, and MongoDB persistence.

---

## Features

- **Conversational AI** — Powered by Groq's `llama-3.3-70b-versatile` model with a warm, human-like therapy persona
- **Crisis Detection** — Automatically identifies red flags (suicidal ideation, self-harm, etc.) via keyword scanning + LLM analysis
- **Instant Care Alerts** — Prints alerts to the terminal and logs them to `backend/alerts.log` when a critical flag is detected
- **Conversation Analysis** — Every message triggers a structured JSON analysis: mood, themes, sentiment score, red flags, and care recommendation
- **MongoDB Persistence** — Full conversation history, chat logs, and analysis stored in MongoDB Atlas
- **Dark / Light Mode** — Theme toggle with localStorage persistence
- **Session Continuity** — Session ID stored in browser `localStorage` so conversations persist across page refreshes

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Vite, TailwindCSS, shadcn/ui, Framer Motion |
| Backend | Python, FastAPI, Uvicorn |
| LLM | Groq API (`llama-3.3-70b-versatile`) |
| Database | MongoDB Atlas |
| Analysis | Custom LLM-based analysis pipeline |

---

## Project Structure

```
chatgpt/
├── backend/
│   ├── app.py            # FastAPI routes
│   ├── llm.py            # Groq LLM integration + system prompt
│   ├── analysis.py       # Conversation analysis + red flag detection
│   ├── db.py             # MongoDB connection + CRUD
│   ├── requirements.txt  # Python dependencies
│   └── .env              # API keys (not committed)
├── frontend/
│   ├── src/
│   │   ├── pages/Index.tsx       # Main chat page
│   │   ├── components/chat/      # ChatBubble, ChatInput, ChatHeader, etc.
│   │   └── hooks/useTheme.ts     # Dark/light mode hook
│   └── index.html
├── run.py                # Starts both backend and frontend together
└── README.md
```

---

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ / npm
- A [Groq API key](https://console.groq.com)
- A [MongoDB Atlas](https://cloud.mongodb.com) cluster

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/therapy-bot.git
cd therapy-bot
```

### 2. Configure environment variables

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

### 3. Install Python dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 5. Run the app

```bash
python run.py
```

This starts:
- **Backend** → `http://localhost:8003`
- **Frontend** → `http://localhost:8080`

> `run.py` automatically cleans any stale processes on port 8003 before starting.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/chat` | Send a message, get a reply + analysis |
| `GET` | `/conversation/{session_id}` | Retrieve full conversation history |
| `DELETE` | `/conversation/{session_id}` | Clear a session |

### Example `/chat` request

```json
POST /chat
{
  "session_id": "optional-existing-session-id",
  "message": "I've been feeling really anxious lately"
}
```

### Example response

```json
{
  "session_id": "abc123",
  "reply": "I hear you — anxiety can feel really overwhelming. Can you tell me more about what's been going on?",
  "analysis": {
    "mood": "anxious",
    "themes": ["anxiety", "stress"],
    "sentiment_score": -0.5,
    "summary": "User is experiencing anxiety and seeking support.",
    "red_flags": [],
    "needs_instant_care": false,
    "instant_care_reason": ""
  }
}
```

---

## Crisis Detection

When a user message contains a high-risk phrase or the LLM detects critical intent, the backend:

1. Prints a visible alert in the terminal:
```
============================================================
[!!!]  NEEDS INSTANT CARE  |  session: abc123
    Reason : User expressed explicit suicidal ideation
    Flag 1: [CRITICAL] suicidal ideation -- I want to kill myself
============================================================
```

2. Appends the alert to `backend/alerts.log` with a UTC timestamp
3. Sets `needs_instant_care: true` in the MongoDB document

---

## MongoDB Schema

Each session document in `therapy_bot.conversations`:

```json
{
  "session_id": "string",
  "messages": [{ "role": "user|assistant", "content": "string" }],
  "chat_log": [{ "index": 0, "role": "user", "content": "string", "timestamp": "ISO" }],
  "message_count": 4,
  "latest_analysis": { ... },
  "needs_instant_care": false,
  "instant_care_reason": "",
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime"
}
```

---

## Notes

- The `.env` file is excluded from version control via `.gitignore` — never commit your API keys
- The bot is **not** a replacement for a licensed therapist — it is a supportive tool only
- For production use, restrict CORS origins in `backend/app.py`
