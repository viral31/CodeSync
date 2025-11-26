# CodeSync - Real-time Pair Programming

Real-time collaborative code editor with AI autocomplete. Two developers can join the same room and code together instantly.

## Features
- Room-based collaboration with unique IDs
- Real-time code synchronization via WebSockets
- AI-powered autocomplete (Google Gemini)
- Persistent storage in PostgreSQL


## Tech Stack
- **Backend:** FastAPI, WebSockets, PostgreSQL, SQLAlchemy
- **AI:** Google Gemini API

## Quick Start

**Requirements:** Python 3.12+, PostgreSQL

```bash
# Clone the repository
git clone https://github.com/viral31/CodeSync.git
cd CodeSync

# Install dependencies
pip install -r requirements.txt

# Database setup
# Option 1: PostgreSQL (Recommended)
psql -U postgres
CREATE DATABASE codesync;
\q

# Option 2: SQLite (for testing)
# No setup needed - will create automatically

# Environment setup
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start server
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
- **Standardized responses:** Consistent API response format
- **Global exception handling:** Custom exception classes with proper HTTP status codes
- **Last-write-wins:** Simple conflict resolution

## API Response Format

All API responses follow a standardized format:

**Success Response:**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { /* actual response data */ },
  "error_code": null
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error description",
  "error_code": "ERROR_TYPE",
  "data": null
}
```

## AI-Powered Autocomplete

The application uses **Google Gemini AI** for intelligent code suggestions:

**Features:**
- Real-time AI code completions
- Context-aware suggestions based on existing code
- Multi-language support (Python, JavaScript, etc.)
- Graceful fallback to mock suggestions if API unavailable

**Setup:**
1. Get free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file: `GEMINI_API_KEY=your_key_here`
3. Restart the server

**Benefits:**
- ✅ **Free tier** - Generous usage limits
- ✅ **Fast responses** - Low latency completions
- ✅ **Code-aware** - Understands programming context
- ✅ **Reliable** - Falls back to rule-based suggestions

## Usage
1. Start server: `python run.py`
2. Create room: `POST /rooms/`
3. Connect via WebSocket: `ws://localhost:8000/ws/{room_id}`
4. Send code updates in real-time

## Limitations & Future
**Current:** Anonymous users, last-write-wins, no cursor tracking

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