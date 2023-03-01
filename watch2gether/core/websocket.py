from typing import List

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect


class WebSocketConnectionManager(object):
    """WebSocket连接管理器.

    Attributes:
        active_connections: list of WebSocket,
            连接的WebSocket客户端列表.
    """
    def __init__(self):
        """初始化WebSocket连接管理器."""
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """接受WebSocket客户端连接.

        Args:
            websocket: WebSocket,
                一个websocket连接.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """断开WebSocket客户端连接.

        Args:
            websocket: WebSocket,
                一个websocket连接.
        """
        self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        """对连接的WebSocket客户端进行广播(传输JSON数据).

        Args:
            data: dict,
                广播的数据(JSON格式).
        """
        for connection in self.active_connections:
            await connection.send_json(data)


router = APIRouter()
manager = WebSocketConnectionManager()  # 实例化WebSocket连接管理器.


@router.websocket('/ws/')
async def create_websocket_endpoint(websocket: WebSocket):
    """创建WebSocket服务器.

    Args:
        websocket: WebSocket,
            一个websocket连接.
    """
    await manager.connect(websocket)

    try:
        while True:
            # 接收并转发(广播)数据.
            data = await websocket.receive_json()
            await manager.broadcast(data)
            # TODO(Steve): 配置服务器端的日志.
    except WebSocketDisconnect:
        manager.disconnect(websocket)
