from json.decoder import JSONDecodeError

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from watch2gether import logger
from watch2gether.core.websockets import ConnectionManager


router = APIRouter()
manager = ConnectionManager()  # 实例化WebSocket连接管理器.


@router.websocket('/ws/{client_id}/')
async def create_websocket_endpoint(client_id: int, websocket: WebSocket):
    """创建WebSocket服务.

    Args:
        client_id: int,
            WebSocket客户端ID(路径参数).
        websocket: WebSocket,
            WebSocket实例.
    """
    # 首先进行客户端ID校验.
    if client_id in manager.active_connections:
        await websocket.close(code=1008,  # Policy Violation.
                              reason='具有相同ID的客户端已存在, 连接被拒绝!')

        logger.warning(f'客户端({websocket.client.host}:{websocket.client.port})'
                       f'试图以已存在客户端ID#{client_id}连接被拒!')
    else:
        await manager.connect(client_id, websocket)

        try:
            while True:
                try:
                    data = await websocket.receive_json()
                    props = data.get('props', dict())
                    received_client_id = props.get('receivedClientID', -1)

                    # 对工作类型进行判断.
                    if (props.get('type') == 'websocket.unicast'
                            and received_client_id > 0):
                        await manager.unicast(data, client_id, received_client_id)  # noqa: E501
                    else:
                        await manager.broadcast(data, client_id)
                except JSONDecodeError:
                    logger.warning(f'客户端({websocket.client.host}:{websocket.client.port})'  # noqa: E501
                                   f'发送无法解析的JSON数据!')
        except WebSocketDisconnect:
            manager.disconnect(client_id)
