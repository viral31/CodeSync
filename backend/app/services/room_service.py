import uuid
from sqlalchemy.orm import Session
from app.database import Room

class RoomService:
    @staticmethod
    def create_room(db: Session) -> str:
        room_id = str(uuid.uuid4())[:8]
        room = Room(id=room_id, code="")
        db.add(room)
        db.commit()
        return room_id
    
    @staticmethod
    def get_room(db: Session, room_id: str) -> Room:
        return db.query(Room).filter(Room.id == room_id).first()
    
    @staticmethod
    def update_room_code(db: Session, room_id: str, code: str):
        room = db.query(Room).filter(Room.id == room_id).first()
        if room:
            room.code = code
            db.commit()