from typing import Dict

from fastapi import WebSocket

from watch2gether import experimental_logger as logger


class ConnectionManager(object):
    """WebSockets连接管理器.

    Attributes:
        active_connections: dict[int, WebSocket],
            用于存储活跃的WebSocket连接的信息, 键值对为客户端ID和WebSocket实例.
    """
    def __init__(self):
        """初始化WebSockets连接管理器."""
        self.active_connections: Dict[int, WebSocket] = dict()

    async def connect(self, client_id: int, websocket: WebSocket):
        """接受WebSocket客户端的连接.

        Args:
            client_id: int,
                WebSocket客户端ID.
            websocket: WebSocket,
                WebSocket实例.
        """
        await websocket.accept()
        self.active_connections[client_id] = websocket

        logger.info(f'客户端({websocket.client.host}:{websocket.client.port})连接成功.')  # noqa: E501
        logger.info(f'当前活跃的连接数为{len(self.active_connections)}.')

    def disconnect(self, client_id: int):
        """断开WebSocket客户端连接.

        Args:
            client_id: int,
                WebSocket客户端ID.
        """
        websocket = self.active_connections.pop(client_id)

        logger.info(f'客户端({websocket.client.host}:{websocket.client.port})断开连接.')  # noqa: E501
        logger.info(f'当前活跃的连接数为{len(self.active_connections)}.')
