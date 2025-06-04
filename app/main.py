# app/main.py
from fastapi import FastAPI
from app.routers import user
import socketio
from app.socketio_app import register_socketio_events

app = FastAPI()
app.include_router(user.router, prefix="/api")


# 初始化 Socket.IO
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[])
register_socketio_events(sio)

# 用 ASGIApp 包装
app_sio = socketio.ASGIApp(sio, other_asgi_app=app)