"""测试WebSocket服务器."""
from fastapi.testclient import TestClient

import watch2gether as w2g


class TestWebSocket(object):
    async def test_websocket(self):
        """测试WebSocket服务器."""
        client = TestClient(app=w2g.app)
        manager = w2g.websocket.manager
        test_data = {'msg': 'Hello, World!'}

        with client.websocket_connect('/ws/') as websocket:
            await manager.broadcast(test_data, None)

            data = websocket.receive_json()
            assert data == {'msg': 'Hello, World!'}
