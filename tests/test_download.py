"""测试下载服务."""
from pathlib import Path

import pytest

from pytest_httpserver import HTTPServer

import watch2gether as w2g


class TestDownload(object):
    def test_video_download_successful(self, httpserver: HTTPServer):
        """测试视频下载成功."""
        # 注意: 需要先进行`test_convert.py`的测试生成流媒体资源!
        # 这样可以重复利用资源, 进而降低测试时间.
        m3u8_data = Path('./tests/assets/flower/flower.m3u8').read_bytes()
        ts_data = Path('./tests/assets/flower/stream_0.ts').read_bytes()

        httpserver.expect_request('/videos/flower/flower.m3u8').respond_with_data(m3u8_data)
        httpserver.expect_request('/videos/flower/stream_0.ts').respond_with_data(ts_data)

        videos_directory = w2g.download_m3u8(
            url=httpserver.url_for('/videos/flower/flower.m3u8'),
            m3u8_directory='./tests/assets/video/',
            info=True
        )

        assert videos_directory.absolute() == Path('./tests/assets/video/').absolute()  # noqa: E501

    def test_video_not_exists(self, httpserver: HTTPServer):
        """测试视频文件不存在."""
        httpserver.expect_request('/video/flower/').respond_with_json({'detail': 'Not Found'}, status=404)  # noqa: E501

        with pytest.raises(SystemExit) as pytest_exit:
            w2g.download_m3u8(
                url=httpserver.url_for('/video/flower/'),
                m3u8_directory='./tests/assets/video/'
            )

        assert pytest_exit.value.code == 1

    def test_no_network(self):
        """测试无网络连接."""
        with pytest.raises(SystemExit) as pytest_exit:
            w2g.download_m3u8(
                url='http://localhost/video/playlist.m3u8',  # noqa: E501 使用localhost没有服务监听的端口模拟.
                m3u8_directory='./tests/assets/video/'
            )

        assert pytest_exit.value.code == 1
