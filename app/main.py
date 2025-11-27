from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session
import json

from app.database import create_tables, get_db
from app.routers import rooms, autocomplete, websocket
from app.middleware.exception_handler import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler
)

app = FastAPI(title="CodeSync API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        "*"  # Remove this in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)
app.include_router(autocomplete.router)
app.include_router(websocket.router)

# Add exception handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.on_event("startup")
def startup_event():
    create_tables()



@app.get("/")
def read_root():
    return {"message": "CodeSync API is running"}