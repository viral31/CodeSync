from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import RoomCreate
from app.models.response import ApiResponse
from app.services.room_service import RoomService
from app.exceptions import DatabaseException

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/", response_model=ApiResponse)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    try:
        room_id = RoomService.create_room(db)
        return ApiResponse(
            success=True,
            message="Room created successfully",
            data={"roomId": room_id}
        )
    except Exception as e:
        raise DatabaseException("Failed to create room")