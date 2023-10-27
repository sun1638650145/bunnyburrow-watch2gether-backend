"""测试流媒体服务."""
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import watch2gether as w2g


w2g.streaming.videos_directory = Path('./tests/assets/')


class TestStreaming(object):
    @pytest.mark.parametrize(
        'url, expected_status_code',
        [
            ('/video/flower/', 200),
            ('/videos/flower/flower.m3u8', 200),
            ('/flower/', 404),
            ('/videos/flower/flower.m3u', 404)
        ]
    )
    async def test_streaming(self, url, expected_status_code):
        """测试流媒体服务."""
        client = TestClient(w2g.app)

        response = client.get(url)
        assert response.status_code == expected_status_code
