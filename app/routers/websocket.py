from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.websocket_service import WebSocketService

router = APIRouter()

@router.websocket("/api/v1/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, db: Session = Depends(get_db)):
    try:
        await WebSocketService.handle_connection(websocket, room_id, db)
        
        while True:
            try:
                data = await websocket.receive_text()
                await WebSocketService.process_message(websocket, room_id, data, db)
            except Exception as e:
                print(f"Error processing WebSocket message: {e}")
                break
                
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for room {room_id}")
    except Exception as e:
        print(f"Unexpected WebSocket error: {e}")
    finally:
        WebSocketService.handle_disconnection(websocket, room_id)