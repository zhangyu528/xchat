import threading
import asyncio
import uvicorn
from app.main import app_sio
from socketio import AsyncClient
import pytest

@pytest.fixture(scope="module")
def run_server():
    config = uvicorn.Config(app_sio, host="127.0.0.1", port=5002, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run)
    thread.start()
    # 等待服务端启动
    asyncio.run(asyncio.sleep(1))
    yield
    server.should_exit = True
    thread.join()


@pytest.mark.asyncio
async def test_socketio_connect(run_server):
    client = AsyncClient()
    connected = False

    @client.event
    async def connect():
        nonlocal connected
        connected = True

    await client.connect("http://127.0.0.1:5002")
    await asyncio.sleep(1)
    assert connected is True

    await client.disconnect()