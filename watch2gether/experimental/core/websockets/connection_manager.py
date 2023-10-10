import asyncio

from typing import Dict, Optional

from fastapi import WebSocket

from watch2gether import experimental_logger as logger


class ConnectionManager(object):
    """WebSockets连接管理器.

    Attributes:
        active_connections: Dict[int, WebSocket],
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

    async def broadcast(self, data: Dict, client_id: Optional[int] = None):
        """广播数据.

        Args:
            data: Dict,
                广播的数据(使用JSON格式).
            client_id: int, default=None,
                (可选)广播数据的客户端, 填写此参数则不对自身广播.
        """
        await_tasks = []
        for received_client_id, websocket in self.active_connections.items():
            if client_id != received_client_id:  # 避免广播风暴.
                await_tasks.append(
                    asyncio.create_task(websocket.send_json(data))
                )

        # 并发运行, 广播数据.
        await asyncio.gather(*await_tasks)

        websocket = self.active_connections.get(client_id)  # 获取广播数据的客户端.
        if websocket:
            logger.info(f'客户端({websocket.client.host}:{websocket.client.port})广播数据.')  # noqa: E501
        else:
            logger.warning('广播数据(包含自身客户端)!')

    async def unicast(self,
                      data: Dict,
                      client_id: int,
                      received_client_id: int):
        """单播数据.

        Args:
            data: Dict,
                单播的数据(使用JSON格式).
            client_id: int,
                发起单播的客户端ID.
            received_client_id: int,
                接收单播的客户端ID.
        """
        try:
            websocket = self.active_connections.get(client_id)
            received_websocket = self.active_connections.get(received_client_id)  # noqa: E501
            await received_websocket.send_json(data)

            logger.info(f'客户端({websocket.client.host}:{websocket.client.port})'
                        f'向客户端({received_websocket.client.host}:{received_websocket.client.port})单播数据.')  # noqa: E501
        except AttributeError:
            logger.error('接收单播的客户端不存在!')
