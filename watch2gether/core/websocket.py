from typing import Dict, Optional

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from watch2gether import logger
from watch2gether.core import get_current_time


class WebSocketConnectionManager(object):
    """WebSocket连接管理器.

    Attributes:
        active_connections: dict,
            存储连接的WebSocket客户端, 键值分别是client_id和WebSocket实例.
    """
    def __init__(self):
        """初始化WebSocket连接管理器."""
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        """接受WebSocket客户端连接.

        Args:
            websocket: WebSocket,
                一个websocket连接.
            client_id: int,
                websocket客户端ID, 仅用于标识连接的客户端.
        """
        await websocket.accept()
        self.active_connections[client_id] = websocket

        logger.info(f'{get_current_time()}: 客户端'
                    f'({websocket.client.host}:{websocket.client.port})连接成功.')
        logger.info(f'{get_current_time()}: '
                    f'当前活跃的连接数为{len(self.active_connections)}.')

    def disconnect(self, client_id: int):
        """断开WebSocket客户端连接.

        Args:
            client_id: int,
                websocket客户端ID, 仅用于标识连接的客户端.
        """
        connection = self.active_connections[client_id]
        del self.active_connections[client_id]

        logger.info(f'{get_current_time()}: 客户端'
                    f'({connection.client.host}:{connection.client.port})断开连接.')  # noqa: E501
        logger.info(f'{get_current_time()}: '
                    f'当前活跃的连接数为{len(self.active_connections)}.')

    async def broadcast(self,
                        data: dict,
                        exclude_client_id: Optional[int] = None):
        """对连接的WebSocket客户端进行广播(传输JSON数据).

        Args:
            data: dict,
                广播的数据(JSON格式).
            exclude_client_id: int, default=None,
                (可选)不希望接收广播的WebSocket客户端ID.
        """
        for client_id, connection in self.active_connections.items():
            if client_id != exclude_client_id:  # 默认情况, 发送数据的WebSocket客户端不广播自身.
                await connection.send_json(data)

        if exclude_client_id:
            client_message = (f'({self.active_connections[exclude_client_id].client.host}'  # noqa: E501
                              f':{self.active_connections[exclude_client_id].client.port})')  # noqa: E501
        else:
            client_message = ''
        logger.info(f'{get_current_time()}: 客户端{client_message}广播数据.')

    async def unicast(self, data: dict, client_id: int, target_client_id: int):
        """对连接的WebSocket客户端进行单播(传输JSON数据).

        Args:
            data: dict,
                广播的数据(JSON格式).
            client_id: int,
                发送单播的websocket客户端ID.
            target_client_id: int,
                接收单播的WebSocket客户端ID.
        """
        connection = self.active_connections[target_client_id]
        await connection.send_json(data)

        logger.info(f'{get_current_time()}: 客户端'
                    f'({self.active_connections[client_id].client.host}'
                    f':{self.active_connections[client_id].client.port})'
                    f'向客户端({connection.client.host}:{connection.client.port})单播数据.')  # noqa: E501


router = APIRouter()
manager = WebSocketConnectionManager()  # 实例化WebSocket连接管理器.


def generate_logout_data(client_id: int) -> dict:
    """生成用户异常退出时的数据.

    Args:
        client_id: int,
            websocket客户端ID, 异常退出连接的客户端.

    Return:
        用户退出的数据(JSON数据).
    """
    return dict({
        'data': {
            'msg': 'logout',
            'user': {'clientID': client_id}
        },
        'meta': {'type': 'shake_hand'}
    })


@router.websocket('/ws/{client_id}/')
async def create_websocket_endpoint(websocket: WebSocket, client_id: int):
    """创建WebSocket服务器.

    Args:
        websocket: WebSocket,
            一个websocket连接.
        client_id: int,
            websocket客户端ID, 仅用于标识连接的客户端.
    """
    await manager.connect(websocket, client_id)

    try:
        while True:
            # 接收并转发数据.
            data = await websocket.receive_json()
            target_client_id = data['meta'].get('to')

            if target_client_id:
                # 单播模式.
                await manager.unicast(data, client_id, target_client_id)
            else:
                # 广播模式.
                await manager.broadcast(data, exclude_client_id=client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        # 与WebSocket服务器异常断开连接, 广播用户退出消息.
        await manager.broadcast(generate_logout_data(client_id))
