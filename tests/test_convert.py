"""测试转换服务."""
from pathlib import Path

import pytest

import watch2gether as w2g


class TestConvert(object):
    def test_video_conversion_successful(self):
        """测试视频格式转换成功."""
        videos_directory = w2g.convert_mp4_to_m3u8(
            mp4_filepath='./tests/assets/flower.mp4',
            m3u8_directory='./tests/assets/flower/',
            video_encoder='libx264',
            audio_encoder='aac',
            crf=23,
            preset='veryfast',
            bitrate=128,
            audio_channels=2,
            log_level='error',
            m3u8_format='hls',
            hls_time=2,
            hls_playlist_type='vod',
            hls_segment_filename='stream'
        )

        assert videos_directory.absolute() == Path('./tests/assets/').absolute()  # noqa: E501

    def test_file_not_exists(self):
        """测试视频文件不存在."""
        with pytest.raises(SystemExit) as pytest_exit:
            w2g.convert_mp4_to_m3u8(
                mp4_filepath='./tests/flower.mp4',
                m3u8_directory='./tests/assets/flower/'
            )

        assert pytest_exit.value.code == 127
