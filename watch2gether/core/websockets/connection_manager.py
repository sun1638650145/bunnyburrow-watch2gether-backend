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
        room = self.room_connections[room_id]

        await_tasks = []
        for received_client_id, websocket in room.items():
            if client_id != received_client_id:  # 避免广播风暴.
                await_tasks.append(
                    asyncio.create_task(websocket.send_json(data))
                )

        # 并发运行, 广播数据.
        await asyncio.gather(*await_tasks)

        if client_id is not None:
            websocket = room[client_id]  # 获取广播数据的客户端.

            logger.info(f'房间({room_id})中的客户端({_get_client_address(websocket)})广播数据.')
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

        room = self.room_connections[room_id]
        room[client_id] = websocket

        logger.info(f'客户端({_get_client_address(websocket)})成功连接到房间({room_id}).')
        logger.info(f'房间({room_id})当前活跃的连接数为{len(room)}.')

    def disconnect(self, room_id: str, client_id: int):
        """断开WebSocket客户端连接.

        Args:
            room_id: str,
                WebSocket房间ID.
            client_id: int,
                WebSocket客户端ID.
        """
        room = self.room_connections[room_id]
        websocket = room.pop(client_id)

        logger.info(f'房间({room_id})中的客户端({_get_client_address(websocket)})断开连接.')

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
            room = self.room_connections[room_id]
            websocket = room[client_id]
            received_websocket = room[received_client_id]
            await received_websocket.send_json(data)

            logger.info(f'客户端({_get_client_address(websocket)})在房间({room_id})中'
                        f'向客户端({_get_client_address(received_websocket)})单播数据.')
        except AttributeError:
            logger.error(f'房间({room_id})中接收单播的客户端不存在!')


def _get_client_address(websocket: WebSocket) -> str:
    """获取WebSocket客户端的地址.

    Args:
        websocket: WebSocket,
            WebSocket实例.

    Return:
        `host:port`格式的WebSocket客户端地址; 如果无法获取则返回'unknown'.
    """
    host = _get_client_host(websocket)
    port = _get_client_port(websocket)

    if host is None or port is None:
        return 'unknown'
    else:
        return f'{host}:{port}'


def _get_client_host(websocket: WebSocket) -> Optional[str]:
    """获取WebSocket客户端的主机地址.
    优先从请求头`X-Forwarded-For`中获取客户端的真实IP地址.

    Args:
        websocket: WebSocket,
            WebSocket实例.

    Return:
        WebSocket客户端的主机地址.
    """
    x_forwarded_for = websocket.headers.get('x-forwarded-for')
    client = websocket.client

    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    elif client is not None:
        return client.host
    else:
        return None


def _get_client_port(websocket: WebSocket) -> Optional[int]:
    """获取WebSocket客户端的端口号.

    Args:
        websocket: WebSocket,
            WebSocket实例.

    Return:
        WebSocket客户端的端口号.
    """
    client = websocket.client

    if client is not None:
        return client.port
    else:
        return None
