from fastapi import HTTPException

class RoomNotFoundException(HTTPException):
    def __init__(self, room_id: str):
        super().__init__(
            status_code=404,
            detail=f"Room {room_id} not found"
        )

class ValidationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=400,
            detail=message
        )

class DatabaseException(HTTPException):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            status_code=500,
            detail=message
        )