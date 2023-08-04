"""测试流媒体服务."""
from fastapi.testclient import TestClient

import watch2gether as w2g


class TestStreaming(object):
    def test_streaming(self):
        """测试流媒体服务."""
        client = TestClient(w2g.app)
        w2g.streaming.video_directory = w2g.convert_mp4_to_m3u8(
            mp4_filepath='./tests/assets/flower.mp4',
            m3u8_directory='./tests/assets/flower/'
        )

        # 请求成功.
        response = client.get('/video/flower/')
        assert response.status_code == 200
        # 请求的资源不存在.
        response = client.get('/flower/')
        assert response.status_code == 404
