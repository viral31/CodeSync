from pydantic import BaseModel

class RoomCreate(BaseModel):
    pass

class RoomResponse(BaseModel):
    roomId: str

class AutocompleteRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str

class AutocompleteResponse(BaseModel):
    suggestion: str

class CodeUpdate(BaseModel):
    roomId: str
    code: str
    userId: str