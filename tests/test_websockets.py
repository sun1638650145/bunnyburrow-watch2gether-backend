"""测试WebSocket服务."""
import pytest

from fastapi import WebSocketDisconnect
from fastapi.testclient import TestClient

import watch2gether as w2g


manager = w2g.websocket.manager  # 获取WebSocket连接管理器.


class TestWebSockets(object):
    async def test_connection_refused(self):
        """测试使用相同客户端ID连接被拒."""
        client = TestClient(w2g.app)

        with client.websocket_connect('/ws/2023/'):
            assert len(manager.active_connections) == 1

            # 使用相同客户端ID连接.
            with pytest.raises(WebSocketDisconnect):
                with client.websocket_connect('/ws/2023/'):
                    assert len(manager.active_connections) == 1  # noqa: E501 连接被拒且仍为1个活跃连接.

    async def test_broadcast(self):
        """测试广播数据."""
        client_a = TestClient(w2g.app)
        client_b = TestClient(w2g.app)

        with (client_a.websocket_connect('/ws/1001/') as websocket_a,
              client_b.websocket_connect('/ws/1002/') as websocket_b):
            # 模拟来自客户端a的广播, 且对自身广播.
            await manager.broadcast({'msg': 'Hi!'})
            # 模拟来自客户端a的广播, 不对自身广播.
            await manager.broadcast({'msg': 'Hello, World!'}, 1001)

            data_a = websocket_a.receive_json()
            # 客户端b会收到两条数据.
            data_b1 = websocket_b.receive_json()
            data_b2 = websocket_b.receive_json()

            assert len(manager.active_connections) == 2
            assert data_a == {'msg': 'Hi!'}
            assert data_b1 == {'msg': 'Hi!'}
            assert data_b2 == {'msg': 'Hello, World!'}

    async def test_unicast(self):
        """测试单播数据."""
        client_a = TestClient(w2g.app)
        client_b = TestClient(w2g.app)

        with (client_a.websocket_connect('/ws/1001/'),
              client_b.websocket_connect('/ws/1002/') as websocket):
            # 模拟来自客户端a的单播.
            await manager.unicast({'msg': 'Hi!'}, 1001, 1002)
            # 模拟来自客户端a的单播, 发送到不存在的客户端.
            await manager.unicast({'msg': 'Hi!'}, 1001, 1003)

            data = websocket.receive_json()

            assert len(manager.active_connections) == 2
            assert data == {'msg': 'Hi!'}
