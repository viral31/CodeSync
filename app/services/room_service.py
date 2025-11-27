import uuid
from sqlalchemy.orm import Session
from app.database import Room

class RoomService:
    @staticmethod
    def create_room(db: Session) -> str:
        try:
            room_id = str(uuid.uuid4())[:8]
            room = Room(id=room_id, code="")
            db.add(room)
            db.commit()
            return room_id
        except Exception as e:
            db.rollback()
            print(f"Error creating room: {e}")
            raise
    
    @staticmethod
    def get_room(db: Session, room_id: str) -> Room:
        try:
            return db.query(Room).filter(Room.id == room_id).first()
        except Exception as e:
            print(f"Error getting room {room_id}: {e}")
            return None
    
    @staticmethod
    def update_room_code(db: Session, room_id: str, code: str):
        try:
            room = db.query(Room).filter(Room.id == room_id).first()
            if room:
                room.code = code
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error updating room {room_id}: {e}")
            raise