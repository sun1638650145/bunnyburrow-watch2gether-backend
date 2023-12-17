"""测试WebSocket服务."""
import pytest

from fastapi import WebSocketDisconnect
from fastapi.testclient import TestClient

import watch2gether as w2g


manager = w2g.websocket.manager  # 获取WebSocket连接管理器.


class TestWebSockets(object):
    def test_connection_refused(self):
        """测试使用相同客户端ID连接被拒."""
        client = TestClient(w2g.app)

        with client.websocket_connect('/ws/2023/'):
            assert len(manager.active_connections) == 1

            # 使用相同客户端ID连接.
            with pytest.raises(WebSocketDisconnect):
                with client.websocket_connect('/ws/2023/'):
                    assert len(manager.active_connections) == 1  # noqa: E501 连接被拒且仍为1个活跃连接.

    @pytest.mark.asyncio
    async def test_broadcast(self):
        """测试广播数据."""
        client_a, client_b = TestClient(w2g.app), TestClient(w2g.app)
        s_data_a = {'msg': 'Hi!'}
        s_data_b = {'text': 'Hello, World!'}
        s_data_c = 'Not JSON!'

        with (client_a.websocket_connect('/ws/1001/') as websocket_a,
              client_b.websocket_connect('/ws/1002/') as websocket_b):
            # 模拟由客户端a(实际上由服务器)发起广播, 且对自身广播.
            await manager.broadcast(s_data_a)
            # 由客户端a发起广播.
            websocket_a.send_json({
                'props': {'type': 'websocket.broadcast'},
                'data': s_data_b
            })
            # 客户端a发送无法解析的JSON数据.
            websocket_a.send_text(s_data_c)

            r_data_a = websocket_a.receive_json()
            # 客户端b会收到两条数据.
            r_data_b1 = websocket_b.receive_json()
            r_data_b2 = websocket_b.receive_json()

            assert len(manager.active_connections) == 2
            assert r_data_a == s_data_a
            assert r_data_b1 == s_data_a
            assert r_data_b2.get('data') == s_data_b

    def test_unicast(self):
        """测试单播数据."""
        client_a, client_b = TestClient(w2g.app), TestClient(w2g.app)
        s_data = {'msg': 'Hi!'}

        with (client_a.websocket_connect('/ws/1001/') as websocket_a,
              client_b.websocket_connect('/ws/1002/') as websocket_b):
            # 客户端a向客户端b发起单播.
            websocket_a.send_json({
                'props': {
                    'type': 'websocket.unicast',
                    'receivedClientID': 1002
                },
                'data': s_data
            })
            # 客户端a向不存在的客户端发起单播.
            websocket_a.send_json({
                'props': {
                    'type': 'websocket.unicast',
                    'receivedClientID': 2023
                },
                'data': s_data
            })

            r_data = websocket_b.receive_json()

            assert len(manager.active_connections) == 2
            assert r_data.get('data') == s_data
