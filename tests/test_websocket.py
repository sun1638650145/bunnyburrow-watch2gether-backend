"""测试WebSocket服务器."""
from time import time
from fastapi.testclient import TestClient

import watch2gether as w2g


class TestWebSocket(object):
    async def test_broadcast(self):
        """测试WebSocket服务器广播."""
        client = TestClient(app=w2g.app)
        client_id = int(time())  # 使用时间戳创建一个用户ID.

        manager = w2g.websocket.manager
        test_data = {'msg': 'Hello, World!'}

        with client.websocket_connect(f'/ws/{client_id}/') as websocket:
            await manager.broadcast(test_data, None)  # 广播自身.

            data = websocket.receive_json()
            assert data == {'msg': 'Hello, World!'}

    async def test_unicast(self):
        """测试WebSocket服务器单播."""
        client = TestClient(app=w2g.app)
        client_id = int(time())  # 使用时间戳创建一个用户ID.

        manager = w2g.websocket.manager
        test_data = {'msg': 'Hello, World!'}

        with client.websocket_connect(f'/ws/{client_id}/') as websocket:
            await manager.unicast(test_data, client_id, client_id)  # 单播自身.

            data = websocket.receive_json()
            assert data == {'msg': 'Hello, World!'}
