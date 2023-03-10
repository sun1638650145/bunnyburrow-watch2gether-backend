"""测试流媒体服务."""
from fastapi.testclient import TestClient

import watch2gether as w2g


class TestStreaming(object):
    def test_streaming(self):
        """测试流媒体服务."""
        client = TestClient(w2g.app)
        w2g.streaming.video_directory = w2g.convert_mp4_to_m3u8(
            mp4_filepath='./tests/assets/我们亲爱的Steve.mp4',
            m3u8_filepath='./tests/assets/我们亲爱的Steve/我们亲爱的Steve.m3u8'
        )

        response = client.get('/video/我们亲爱的Steve/')
        assert response.status_code == 200
