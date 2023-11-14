import os
import subprocess
import sys

from pathlib import Path
from typing import Literal, Union

from watch2gether import logger


HLSPlaylistType = Literal['event', 'vod']
LogLevel = Literal['quiet', 'panic', 'fatal', 'error', 'warning',
                   'info', 'verbose', 'debug', 'trace']
Preset = Literal['ultrafast', 'superfast', 'veryfast', 'faster',
                 'fast', 'medium', 'slow', 'slower', 'veryslow']


def convert_mp4_to_m3u8(mp4_filepath: Union[str, os.PathLike],
                        m3u8_directory: Union[str, os.PathLike],
                        video_encoder: str = 'libx264',
                        audio_encoder: str = 'aac',
                        crf: int = 23,
                        preset: Preset = 'veryfast',
                        bitrate: int = 128,
                        audio_channels: int = 2,
                        log_level: LogLevel = 'error',
                        m3u8_format: str = 'hls',
                        hls_time: int = 2,
                        hls_playlist_type: HLSPlaylistType = 'vod',
                        hls_segment_filename: str = 'stream') -> Path:
    """将视频从mp4格式转换成m3u8格式, 以满足对流媒体的支持;
    如不了解`ffmpeg`的使用, 建议使用默认参数.

    Args:
        mp4_filepath: str or os.PathLike,
            mp4文件的路径, 封装参数`ffmpeg -i input.mp4`.
        m3u8_directory: str or os.PathLike,
            m3u8文件夹的路径, 封装参数`ffmpeg output.m3u8`.
        video_encoder: str, default='libx264',
            视频编码器, 封装参数`ffmpeg -c:v libx264`, 支持的编码器请使用`ffmpeg -codecs`查看.
        audio_encoder: str, default='aac',
            音频编码器, 封装参数`ffmpeg -c:a aac`, 支持的编码器请使用`ffmpeg -codecs`查看.
        crf: int, default=23,
            m3u8文件的视频压缩质量(Constant Rate Factor), 封装参数`ffmpeg -crf 23`,
             取值范围[0, 51], 推荐选择范围[17, 28], 注意crf值越小, 视频质量越高, 转换时间越长.
        preset: Preset, default='veryfast',
            编码速度与压缩比, 封装参数`ffmpeg -preset veryfast`.
        bitrate: int, default=128,
            m3u8文件的音频的比特率, 单位为kbit/s. 封装参数`ffmpeg -b:a 128k`.
        audio_channels: int, default=2,
            m3u8文件的音频的声道数, 封装参数`ffmpeg -ac 2`.
        log_level: LogLevel, default='error',
            设置使用的日志记录级别, 封装参数`ffmpeg -loglevel error`.
        m3u8_format: str, default='hls',
            输出文件的封装格式, 封装参数`ffmpeg -f hls`, 支持的封装格式请使用`ffmpeg -formats`查看.
        hls_time: int, default=2,
            HLS视频流片段的时长, 封装参数`ffmpeg -f hls -hls_time 2`, 仅在输出文件的封装格式为HLS时有效.
        hls_playlist_type: HLSPlaylistType, default='vod',
            HLS视频播放列表的类型, 封装参数`ffmpeg -f hls -hls_playlist_type vod`,
             仅在输出文件的封装格式为HLS时有效.
        hls_segment_filename: str, default='stream',
            HLS视频流片段的文件名, 默认格式是'm3u8_directory/stream_%d.ts',
             封装参数`ffmpeg -f hls -hls_segment_filename 'm3u8_directory/stream_%d.ts'`,  # noqa: E501
             仅在输出文件的封装格式为HLS时有效.

    Return:
        m3u8文件夹的父文件夹的绝对路径.
    """
    cmd = 'ffmpeg'
    cmd += ' -loglevel {}'.format(log_level)
    cmd += ' -i {}'.format(mp4_filepath)
    cmd += ' -c:v {}'.format(video_encoder)
    cmd += ' -crf {}'.format(crf)
    cmd += ' -preset {}'.format(preset)
    cmd += ' -c:a {}'.format(audio_encoder)
    cmd += ' -b:a {}k'.format(bitrate)
    cmd += ' -ac {}'.format(audio_channels)
    cmd += ' -f {}'.format(m3u8_format)
    if m3u8_format == 'hls':
        hls_segment_filename = os.path.join(m3u8_directory,
                                            hls_segment_filename)

        cmd += ' -hls_time {}'.format(hls_time)
        cmd += ' -hls_playlist_type {}'.format(hls_playlist_type)
        cmd += ' -hls_segment_filename "{}_%d.ts"'.format(hls_segment_filename)

    cmd += ' {}'.format(os.path.join(m3u8_directory,
                                     Path(m3u8_directory).name + '.m3u8'))

    # 创建用于保存m3u8的文件夹.
    os.makedirs(Path(m3u8_directory).absolute(), exist_ok=True)

    try:
        logger.info('视频文件正在转换中...')
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError:
        logger.error('没有找到ffmpeg命令或视频文件不存在!')
        sys.exit(127)

    return Path(m3u8_directory).parent.absolute()
