from typing import List, Optional

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from watch2gether import logger
from watch2gether.core import get_current_time


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

        logger.info(f'{get_current_time()}: 客户端'
                    f'({websocket.client.host}:{websocket.client.port})连接成功.')

    def disconnect(self, websocket: WebSocket):
        """断开WebSocket客户端连接.

        Args:
            websocket: WebSocket,
                一个websocket连接.
        """
        self.active_connections.remove(websocket)

        logger.info(f'{get_current_time()}: 客户端'
                    f'({websocket.client.host}:{websocket.client.port})断开连接.')

    async def broadcast(self,
                        data: dict,
                        websocket: Optional[WebSocket] = None):
        """对连接的WebSocket客户端进行广播(传输JSON数据).

        Args:
            data: dict,
                广播的数据(JSON格式).
            websocket: WebSocket, default=None,
                (可选)广播数据来源的WebSocket客户端.
        """
        for connection in self.active_connections:
            await connection.send_json(data)

        if websocket:
            client_message = f'({websocket.client.host}:{websocket.client.port})'  # noqa: E501
        else:
            client_message = ''
        logger.info(f'{get_current_time()}: 客户端{client_message}广播数据.')


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
            await manager.broadcast(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
