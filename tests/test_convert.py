"""测试转换功能."""
import watch2gether as w2g


class TestConvert(object):
    def test_convert_mp4_to_m3u8(self):
        """测试流媒体转换函数."""
        assert w2g.convert_mp4_to_m3u8(
            mp4_filepath='./tests/assets/flower.mp4',
            m3u8_filepath='./tests/assets/flower/flower.m3u8',
            video_encoder='libx264',
            audio_encoder='aac',
            crf=23,
            preset='veryfast',
            bitrate=128,
            audio_channels=2,
            m3u8_format='hls',
            hls_time=2,
            hls_playlist_type='vod',
            hls_segment_filename='stream'
        )
