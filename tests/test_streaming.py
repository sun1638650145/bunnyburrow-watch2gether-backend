"""测试流媒体服务."""
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import watch2gether as w2g


# 注意: 需要先进行`test_convert.py`的测试生成流媒体资源!
#  这样可以重复利用资源, 进而降低测试时间.
w2g.streaming.videos_directory = Path('./tests/assets/')
# 添加文件处理器, 增加对logger的测试覆盖.
w2g.experimental_logger.add_file_handler('./watch2gether.log')


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
