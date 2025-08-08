"""测试下载服务."""
from pathlib import Path

import pytest

import watch2gether as w2g


class TestDownload(object):
    def test_video_download_successful(self):
        """测试视频下载成功."""
        videos_directory = w2g.download_m3u8(
            url='https://naver.github.io/egjs-view360/pano/equirect/m3u8/equi.m3u8',
            m3u8_directory='./tests/assets/video/',
            info=True
        )

        assert videos_directory.absolute() == Path('./tests/assets/video/').absolute()  # noqa: E501

    def test_video_not_exists(self):
        """测试视频文件不存在."""
        with pytest.raises(SystemExit) as pytest_exit:
            w2g.download_m3u8(
                url='https://github.com/video/playlist.m3u8',
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
