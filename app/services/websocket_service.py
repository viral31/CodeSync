from fastapi import WebSocket
from sqlalchemy.orm import Session
import json

from app.websocket_manager import manager
from app.services.room_service import RoomService

class WebSocketService:
    @staticmethod
    async def handle_connection(websocket: WebSocket, room_id: str, db: Session):
        """Handle new WebSocket connection and send initial room data"""
        await manager.connect(websocket, room_id)
        
        try:
            room = RoomService.get_room(db, room_id)
            if room:
                await websocket.send_text(json.dumps({
                    "type": "code_update",
                    "code": room.code,
                    "userId": "system"
                }))
        except Exception as e:
            print(f"Error sending initial room data: {e}")
    
    @staticmethod
    def handle_disconnection(websocket: WebSocket, room_id: str):
        """Handle WebSocket disconnection"""
        manager.disconnect(websocket, room_id)
    
    @staticmethod
    async def process_message(websocket: WebSocket, room_id: str, data: str, db: Session):
        """Process incoming WebSocket message"""
        try:
            message = json.loads(data)
            
            if message.get("type") == "code_update":
                # Update room code in database
                try:
                    RoomService.update_room_code(db, room_id, message.get("code", ""))
                except Exception as e:
                    print(f"Error updating room code: {e}")
                
                # Broadcast to other users in the room
                await manager.broadcast_to_room(room_id, message, websocket)
                
        except json.JSONDecodeError as e:
            print(f"Invalid JSON received: {e}")
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Invalid JSON format"
            }))
            raise
        except Exception as e:
            print(f"Error processing WebSocket message: {e}")
            raise