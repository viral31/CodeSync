# CodeSync - Real-time Pair Programming

Real-time collaborative code editor with AI autocomplete. Two developers can join the same room and code together instantly.

## 🚀 Live Demo

**Frontend Application:** https://codesync-frontend-rho.vercel.app/

**Backend API:** https://web-production-e4870.up.railway.app/

**Try the API:**
- Create room: `POST https://web-production-e4870.up.railway.app/api/v1/rooms/`
- WebSocket: `wss://web-production-e4870.up.railway.app/api/v1/ws/{room_id}`

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
- `POST /api/v1/rooms/` - Create room
- `POST /api/v1/autocomplete` - AI suggestions
- `ws://localhost:8000/api/v1/ws/{room_id}` - Real-time sync

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
2. Create room: `POST /api/v1/rooms/`
3. Connect via WebSocket: `ws://localhost:8000/api/v1/ws/{room_id}`
4. Send code updates in real-time

## Scaling & Architecture

### Current Implementation
**WebSocket Management:**
- **In-memory storage:** `Dict[str, List[WebSocket]]` for active connections
- **Single server:** All connections handled by one FastAPI instance
- **Room-based grouping:** Users join rooms by `room_id`, multiple users per room
- **Real-time sync:** Direct WebSocket broadcasting within same server
- **Persistent data:** Room content stored in PostgreSQL, survives disconnections

**Current Capacity:**
- ~1,000 concurrent WebSocket connections per server
- ~100 active rooms simultaneously
- Limited by single server memory and CPU

**Limitations:**
- No horizontal scaling (can't add more servers)
- Connections lost on server restart
- All users must connect to same server instance

### Future Scaling Solutions

**For 10,000+ concurrent users:**

**1. Redis Message Broker**
```python
# Replace in-memory dict with Redis pub/sub
import redis
redis_client = redis.Redis()

async def broadcast_to_room(room_id: str, message: dict):
    await redis_client.publish(f"room:{room_id}", json.dumps(message))
```

**2. Load Balancer + Multiple Servers**
```
User A → Server 1 (room123)
User B → Server 2 (room123)  # Different server, same room
User C → Server 3 (room123)
```

**3. Distributed Connection Registry**
```python
# Store connection metadata in Redis
connection_registry = {
    "room123": ["server1:conn1", "server2:conn2", "server3:conn3"],
    "room456": ["server1:conn4"]
}
```

**4. Cross-Server Message Flow**
```
User types → Server 1 → Redis pub/sub → All servers → WebSocket broadcast
```

**Implementation Steps:**
1. Replace `ConnectionManager.active_connections` with Redis
2. Add Redis pub/sub for cross-server messaging
3. Implement connection registry for room management
4. Add load balancer with sticky sessions
5. Handle server failures and reconnections

**Expected Results:**
- Support 10,000+ concurrent users
- Horizontal scaling across multiple servers
- Zero-downtime deployments
- Fault tolerance and automatic failover

## Current Limitations
**WebSocket:** Single server, in-memory storage, no horizontal scaling
**Features:** Anonymous users, last-write-wins, no cursor tracking

**Planned:** Redis scaling, operational transforms, user auth, syntax highlighting, comprehensive tests

## Testing
```bash
# API test
curl -X POST http://localhost:8000/api/v1/rooms/

# WebSocket test
# Use browser dev tools: ws://localhost:8000/api/v1/ws/{room_id}
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