import socketio
from socketio import AsyncServer
# 可以连接到数据库或存储用户连接
connected_users = {}

def register_socketio_events(sio: AsyncServer):

    # 连接事件
    @sio.on('connect')
    async def handle_connect(sid, environ):
        print(f"✅ Connected: {sid}")

    # 加入房间
    @sio.on('join')
    async def handle_join(sid, data):
        room = data.get("room")
        await sio.enter_room(sid, room)
        await sio.emit("joined", {"sid": sid, "room": room}, room=room)

    # 接收消息
    @sio.on('message')
    async def handle_message(sid, data):
        room = data.get("room")
        msg = data.get("message")
        await sio.emit("message", {"sid": sid, "message": msg}, room=room)

    # 离开事件
    @sio.on('disconnect')
    async def handle_disconnect(sid):
        print(f"❌ Disconnected: {sid}")
