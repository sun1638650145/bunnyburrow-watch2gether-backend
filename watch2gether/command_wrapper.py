from uvicorn import run

from watch2gether import __version__
from watch2gether import app
from watch2gether import convert_mp4_to_m3u8, streaming
from watch2gether import logger


def convert_command(mp4_filepath: str,
                    m3u8_filepath: str):
    """视频格式转换命令, 简化ffmpeg的使用,
    复杂功能请使用Python脚本模式.

    Example:
        ```shell
        w2g-cli convert ./flower.mp4 ./flower/flower.m3u8
        ```

    Args:
        mp4_filepath: str,
            mp4文件的路径.
        m3u8_filepath: str,
            m3u8文件的路径.
    """
    convert_mp4_to_m3u8(mp4_filepath, m3u8_filepath)


def launch_command(video_dir: str,
                   host: str,
                   port: int):
    """启动服务命令, 用于启动流媒体服务和WebSocket服务.

    Example:
        ```shell
        w2g-cli launch ./flower/
        ```

    Args:
        video_dir: str,
            流媒体视频文件夹路径.
        host: str,
            使用的主机地址.
        port: int,
            绑定的端口号.
    """
    # 通过修改全局变量传递流媒体视频文件夹路径给流媒体服务.
    streaming.video_directory = video_dir

    run(app, host=host, port=port, log_level='error')


def version_command():
    """查看版本命令.

    Example:
        ```shell
        w2g-cli version
        ```
    """
    logger.info('一起看电影命令行工具 ' + __version__)
