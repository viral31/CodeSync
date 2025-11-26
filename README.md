# CodeSync - Real-time Pair Programming

Real-time collaborative code editor with AI autocomplete. Two developers can join the same room and code together instantly.

## Features
- Room-based collaboration with unique IDs
- Real-time code synchronization via WebSockets
- AI-powered autocomplete (Google Gemini)
- Persistent storage in PostgreSQL
- Clean, responsive interface

## Tech Stack
- **Backend:** FastAPI, WebSockets, PostgreSQL, SQLAlchemy
- **AI:** Google Gemini API

## Quick Start

**Requirements:** Python 3.12+, PostgreSQL

```bash
pip install -r requirements.txt
# Copy .env.example to .env and add your GEMINI_API_KEY
python run.py
```

**Backend URL:** http://localhost:8000

## API Endpoints
- `POST /rooms/` - Create room
- `POST /autocomplete` - AI suggestions
- `ws://localhost:8000/ws/{room_id}` - Real-time sync

## AI Setup
1. Copy `.env.example` to `.env`
2. Get API key: [Google AI Studio](https://makersuite.google.com/app/apikey)
3. Add your key to `.env`: `GEMINI_API_KEY=your_actual_key`
4. Restart server

**Features:** Context-aware suggestions, multi-language support, graceful fallback

## Architecture
- **Layered backend:** Routers → Services → Models
- **WebSocket manager:** Room-based connection tracking
- **Redux state:** Centralized WebSocket and code state
- **Last-write-wins:** Simple conflict resolution

## Usage
1. Start servers → Open localhost:3000
2. Create/join room → Share room ID
3. Code together in real-time
4. AI suggestions appear after 600ms pause

## Limitations & Future
**Current:** Anonymous users, last-write-wins, basic UI, no cursor tracking

**Planned:** Operational transforms, user auth, syntax highlighting, Redis scaling, comprehensive tests

## Testing
```bash
# API test
curl -X POST http://localhost:8000/rooms/

# WebSocket test
# Use browser dev tools: ws://localhost:8000/ws/{room_id}
```

## Project layout

```
CodeSync/
├── app/
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic
│   ├── models/           # Database models
│   ├── middleware/       # Exception handlers
│   ├── database.py       # DB setup
│   ├── websocket_manager.py  # WebSocket handling
│   └── main.py          # Main FastAPI app
├── requirements.txt
├── run.py               # Server startup
├── Dockerfile
└── README.md
```