"""测试WebSocket服务."""
import pytest

from fastapi import WebSocketDisconnect
from fastapi.testclient import TestClient

import watch2gether as w2g


@pytest.fixture
def client():
    return TestClient(w2g.app)


@pytest.fixture
def manager():
    return w2g.websocket.manager


class TestWebSockets(object):
    def test_allows_same_client_id_in_different_rooms(self, client, manager):
        """测试允许在不同房间中使用相同客户端ID."""
        room_r0_id, room_r1_id = 'r0', 'r1'
        client_id = 2026

        with (client.websocket_connect(f'/ws/{room_r0_id}/{client_id}/'),
              client.websocket_connect(f'/ws/{room_r1_id}/{client_id}/')):
            room_r0 = manager.room_connections[room_r0_id]
            room_r1 = manager.room_connections[room_r1_id]

            assert set(room_r0) == {client_id}
            assert set(room_r1) == {client_id}

    def test_rejects_duplicate_client_id(self, client, manager):
        """测试在同一房间中使用相同客户端ID连接被拒."""
        room_id, client_id = 'r0', 2026

        with client.websocket_connect(f'/ws/{room_id}/{client_id}/'):
            room = manager.room_connections[room_id]

            assert set(room) == {client_id}

            # 在同一房间中使用相同客户端ID连接.
            with pytest.raises(WebSocketDisconnect) as exc_info:
                with client.websocket_connect(f'/ws/{room_id}/{client_id}/'):
                    pass

            assert exc_info.value.code == 1008
            assert set(room) == {client_id}  # noqa: E501 连接被拒且仍为1个活跃连接.

    def test_client_broadcast(self, client, manager):
        """测试由客户端发起广播."""
        room_id = 'r0'
        sender_client_id = 2026
        receiver_a_client_id, receiver_b_client_id = 2024, 2025

        data = {'text': 'Hello, World!'}

        with (
            client.websocket_connect(f'/ws/{room_id}/{sender_client_id}/') as sender_websocket,  # noqa: E501
            client.websocket_connect(f'/ws/{room_id}/{receiver_a_client_id}/') as receiver_a_websocket,  # noqa: E501
            client.websocket_connect(f'/ws/{room_id}/{receiver_b_client_id}/') as receiver_b_websocket  # noqa: E501
        ):
            room = manager.room_connections[room_id]

            # 发送方客户端发送无法解析的广播数据.
            sender_websocket.send_text('Hello, World!')
            # 发送方客户端再次发起广播.
            sender_websocket.send_json({
                'props': {
                    'type': 'websocket.broadcast'
                },
                'data': data
            })

            assert len(room) == 3
            assert receiver_a_websocket.receive_json()['data'] == data
            assert receiver_b_websocket.receive_json()['data'] == data

    @pytest.mark.asyncio
    async def test_system_broadcast(self, client, manager):
        """测试由系统发起广播."""
        room_id = 'r0'
        receiver_a_client_id, receiver_b_client_id = 2025, 2026

        data = {'text': 'Hello, World!'}

        with (
            client.websocket_connect(f'/ws/{room_id}/{receiver_a_client_id}/') as receiver_a_websocket,  # noqa: E501
            client.websocket_connect(f'/ws/{room_id}/{receiver_b_client_id}/') as receiver_b_websocket  # noqa: E501
        ):
            room = manager.room_connections[room_id]

            await manager.broadcast(data, room_id)

            assert len(room) == 2
            assert receiver_a_websocket.receive_json() == data
            assert receiver_b_websocket.receive_json() == data

    def test_unicast(self, client, manager):
        """测试单播数据."""
        room_id = 'r0'
        sender_client_id, receiver_client_id = 2025, 2026

        data = {'text': 'Hello, World!'}

        with (
            client.websocket_connect(f'/ws/{room_id}/{sender_client_id}/') as sender_websocket,  # noqa: E501
            client.websocket_connect(f'/ws/{room_id}/{receiver_client_id}/') as receiver_websocket  # noqa: E501
        ):
            room = manager.room_connections[room_id]

            # 发送方客户端向不存在的客户端发起单播.
            sender_websocket.send_json({
                'props': {
                    'type': 'websocket.unicast',
                    'receivedClientID': 2023
                },
                'data': data
            })
            # 发送方客户端向接收方发起单播.
            sender_websocket.send_json({
                'props': {
                    'type': 'websocket.unicast',
                    'receivedClientID': receiver_client_id
                },
                'data': data
            })

            assert len(room) == 2
            assert receiver_websocket.receive_json()['data'] == data

    def test_closes_room_when_last_client_disconnects(self, client, manager):
        """测试最后一个客户端断开时关闭房间."""
        room_id, client_id = 'r0', 2026

        with client.websocket_connect(f'/ws/{room_id}/{client_id}/'):
            room = manager.room_connections[room_id]

            assert len(room) == 1

        assert room_id not in manager.room_connections
