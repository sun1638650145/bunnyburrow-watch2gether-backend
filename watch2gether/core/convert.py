import os
import subprocess

from pathlib import Path
from typing import Literal, Union

from watch2gether import logger

Preset = Literal['ultrafast', 'superfast', 'veryfast', 'faster',
                 'fast', 'medium', 'slow', 'slower', 'veryslow']
HLSPlaylistType = Literal['event', 'vod']


def convert_mp4_to_m3u8(mp4_filepath: Union[str, os.PathLike],
                        m3u8_filepath: Union[str, os.PathLike],
                        video_encoder: str = 'libx264',
                        audio_encoder: str = 'aac',
                        crf: int = 23,
                        preset: Preset = 'veryfast',
                        bitrate: int = 128,
                        audio_channels: int = 2,
                        m3u8_format: str = 'hls',
                        hls_time: int = 4,
                        hls_playlist_type: HLSPlaylistType = 'event'):
    """将视频从mp4格式转换成m3u8, 以满足对流媒体的支持;
    如不了解`ffmpeg`的使用, 建议使用默认参数.

    Args:
        mp4_filepath: str or os.PathLike,
            mp4文件的路径, 封装参数`ffmpeg -i input.mp4`.
        m3u8_filepath: str or os.PathLike,
            m3u8文件的路径, 封装参数`ffmpeg output.m3u8`.
        video_encoder: str, default='libx264',
            视频编码器, 封装参数`ffmpeg -c:v libx264`, 支持的编码器请使用`ffmpeg -codecs`查看.
        audio_encoder: str, default='aac',
            音频编码器, 封装参数`ffmpeg -c:a aac`, 支持的编码器请使用`ffmpeg -codecs`查看.
        crf: int, default=23,
            m3u8文件的视频压缩质量(Constant Rate Factor), 封装参数`ffmpeg -crf 23`,
            取值范围[0, 51], 推荐选择范围[17, 28], 注意crf值越小, 视频质量越高, 转换时间越长.
        preset: {'ultrafast', 'superfast', 'veryfast', 'faster',
                 'fast', 'medium', 'slow', 'slower', 'veryslow'},
                  default='veryfast', 编码速度与压缩比, 封装参数`ffmpeg -preset veryfast`.
        bitrate: int, default=128,
            m3u8文件的音频的比特率, 单位为kbit/s. 封装参数`ffmpeg -b:a 128k`.
        audio_channels: int, default=2,
            m3u8文件的音频的声道数, 封装参数`ffmpeg -ac 2`.
        m3u8_format: str, default='hls',
            输出文件的封装格式, 封装参数`ffmpeg -f hls`, 支持的封装格式请使用`ffmpeg -formats`查看.
        hls_time: int, default=4,
            HLS视频流片段的时长, 封装参数`ffmpeg -f hls -hls_time 4`, 仅在输出文件的封装格式为HLS时有效.
        hls_playlist_type: {'event', 'vod'}, default='event',
            HLS视频播放列表的类型, 封装参数`ffmpeg -f hls -hls_playlist_type event`,
             仅在输出文件的封装格式为HLS时有效.
    """
    cmd = 'ffmpeg'
    cmd += ' -i {}'.format(mp4_filepath)
    cmd += ' -c:v {}'.format(video_encoder)
    cmd += ' -crf {}'.format(crf)
    cmd += ' -preset {}'.format(preset)
    cmd += ' -c:a {}'.format(audio_encoder)
    cmd += ' -b:a {}k'.format(bitrate)
    cmd += ' -ac {}'.format(audio_channels)
    cmd += ' -f {}'.format(m3u8_format)
    if m3u8_format == 'hls':
        cmd += ' -hls_time {}'.format(hls_time)
        cmd += ' -hls_playlist_type {}'.format(hls_playlist_type)
    cmd += ' {}'.format(m3u8_filepath)

    # 创建用于保存m3u8的文件夹.
    os.makedirs(Path(m3u8_filepath).absolute().parent, exist_ok=True)

    try:
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError:
        logger.error('没有找到ffmpeg命令, 请安装ffmpeg后重试.')
