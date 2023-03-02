from datetime import datetime
from typing import List

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from watch2gether import logger


def _get_current_time() -> str:
    """获取当前时间."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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

        logger.info(f'{_get_current_time()}: 客户端'
                    f'({websocket.client.host}:{websocket.client.port})连接成功.')

    def disconnect(self, websocket: WebSocket):
        """断开WebSocket客户端连接.

        Args:
            websocket: WebSocket,
                一个websocket连接.
        """
        self.active_connections.remove(websocket)

        logger.info(f'{_get_current_time()}: 客户端'
                    f'({websocket.client.host}:{websocket.client.port})断开连接.')

    async def broadcast(self, websocket: WebSocket, data: dict):
        """对连接的WebSocket客户端进行广播(传输JSON数据).

        Args:
            websocket: WebSocket,
                广播数据来源的WebSocket客户端.
            data: dict,
                广播的数据(JSON格式).
        """
        for connection in self.active_connections:
            await connection.send_json(data)

        logger.info(f'{_get_current_time()}: 客户端'
                    f'({websocket.client.host}:{websocket.client.port})广播数据.')


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
            await manager.broadcast(websocket, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
