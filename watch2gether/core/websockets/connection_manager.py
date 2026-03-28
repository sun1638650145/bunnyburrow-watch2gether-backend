import asyncio

from typing import Dict, Optional

from fastapi import WebSocket

from watch2gether import logger


class ConnectionManager(object):
    """WebSockets连接管理器.

    Attributes:
        room_connections: Dict[str, Dict[int, WebSocket]],
            用于存储根据WebSocket房间ID分组的活跃WebSocket连接的信息;
            第一层键为房间ID, 第二层键为客户端ID, 值为WebSocket实例.
    """
    def __init__(self):
        """初始化WebSockets连接管理器."""
        self.room_connections: Dict[str, Dict[int, WebSocket]] = dict()

    async def broadcast(self,
                        data: Dict,
                        room_id: str,
                        client_id: Optional[int] = None):
        """在指定房间中广播数据.

        Args:
            data: Dict,
                广播的数据(使用JSON格式).
            room_id: str,
                发起广播数据的房间ID.
            client_id: int, default=None,
                (可选)广播数据的客户端ID, 填写此参数则不对自身广播.
        """
        room = self.room_connections.get(room_id)

        await_tasks = []
        for received_client_id, websocket in room.items():
            if client_id != received_client_id:  # 避免广播风暴.
                await_tasks.append(
                    asyncio.create_task(websocket.send_json(data))
                )

        # 并发运行, 广播数据.
        await asyncio.gather(*await_tasks)

        websocket = room.get(client_id)  # 获取广播数据的客户端.
        if websocket:
            logger.info(f'房间({room_id})中的客户端({websocket.client.host}:{websocket.client.port})广播数据.')
        else:
            logger.warning(f'房间({room_id})中广播数据(包含自身客户端)!')

    async def connect(self,
                      room_id: str,
                      client_id: int,
                      websocket: WebSocket):
        """接受WebSocket客户端的连接.

        Args:
            room_id: str,
                WebSocket房间ID.
            client_id: int,
                WebSocket客户端ID.
            websocket: WebSocket,
                WebSocket实例.
        """
        await websocket.accept()

        # 如果房间不存在, 则先创建房间.
        if room_id not in self.room_connections:
            self.room_connections[room_id] = dict()

        room = self.room_connections.get(room_id)
        room[client_id] = websocket

        logger.info(f'客户端({websocket.client.host}:{websocket.client.port})成功连接到房间({room_id}).')
        logger.info(f'房间({room_id})当前活跃的连接数为{len(room)}.')

    def disconnect(self, room_id: str, client_id: int):
        """断开WebSocket客户端连接.

        Args:
            room_id: str,
                WebSocket房间ID.
            client_id: int,
                WebSocket客户端ID.
        """
        room = self.room_connections.get(room_id)
        websocket = room.pop(client_id)

        logger.info(f'房间({room_id})中的客户端({websocket.client.host}:{websocket.client.port})断开连接.')

        # 如果房间中没有活跃的连接, 则直接关闭房间.
        if not room:
            self.room_connections.pop(room_id)
            logger.info(f'房间({room_id})中没有活跃的连接, 房间已关闭.')
        else:
            logger.info(f'房间({room_id})当前活跃的连接数为{len(room)}.')

    def has_client(self, room_id: str, client_id: int) -> bool:
        """检查指定房间中是否已存在相同ID的客户端.

        Args:
            room_id: str,
                WebSocket房间ID.
            client_id: int,
                WebSocket客户端ID.

        Return:
            返回指定房间中是否存在相同ID的客户端.
        """
        return client_id in self.room_connections.get(room_id, dict())

    async def unicast(self,
                      data: Dict,
                      room_id: str,
                      client_id: int,
                      received_client_id: int):
        """在指定房间中单播数据.

        Args:
            data: Dict,
                单播的数据(使用JSON格式).
            room_id: str,
                发起单播数据的房间ID.
            client_id: int,
                发起单播的客户端ID.
            received_client_id: int,
                接收单播的客户端ID.
        """
        try:
            room = self.room_connections.get(room_id)
            websocket = room.get(client_id)
            received_websocket = room.get(received_client_id)
            await received_websocket.send_json(data)

            logger.info(f'客户端({websocket.client.host}:{websocket.client.port})在房间({room_id})中'
                        f'向客户端({received_websocket.client.host}:{received_websocket.client.port})单播数据.')
        except AttributeError:
            logger.error(f'房间({room_id})中接收单播的客户端不存在!')
