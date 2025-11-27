from typing import Dict, List
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        try:
            await websocket.accept()
            if room_id not in self.active_connections:
                self.active_connections[room_id] = []
            self.active_connections[room_id].append(websocket)
        except Exception as e:
            print(f"Error connecting WebSocket to room {room_id}: {e}")
            raise

    def disconnect(self, websocket: WebSocket, room_id: str):
        try:
            if room_id in self.active_connections:
                self.active_connections[room_id].remove(websocket)
                if not self.active_connections[room_id]:
                    del self.active_connections[room_id]
        except ValueError:
            print(f"WebSocket not found in room {room_id} during disconnect")
        except Exception as e:
            print(f"Error during WebSocket disconnect: {e}")

    async def broadcast_to_room(self, room_id: str, message: dict, sender: WebSocket = None):
        if room_id in self.active_connections:
            disconnected_connections = []
            for connection in self.active_connections[room_id]:
                if connection != sender:
                    try:
                        await connection.send_text(json.dumps(message))
                    except Exception as e:
                        print(f"Failed to send message to WebSocket: {e}")
                        disconnected_connections.append(connection)
            
            # Clean up disconnected connections
            for connection in disconnected_connections:
                try:
                    self.active_connections[room_id].remove(connection)
                except ValueError:
                    pass  # Connection already removed
            
            # Remove empty room
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

manager = ConnectionManager()