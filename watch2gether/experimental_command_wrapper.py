from logging import Formatter

from watch2gether import __version__
from watch2gether import convert_mp4_to_m3u8
from watch2gether import experimental_logger as logger


# 命令行工具对日志格式进行自定义.
logger.stream_handler.setFormatter(Formatter(fmt='%(message)s'))


def convert_command(mp4_filepath: str, m3u8_directory: str):
    """转换视频格式命令, 若需要复杂功能请使用脚本模式.

    Example:
        ```shell
        w2g-cli convert ./flower.mp4 ./flower/
        ```
    Args:
        mp4_filepath: str,
            mp4文件的路径.
        m3u8_directory: str,
            m3u8文件夹的路径.
    """
    convert_mp4_to_m3u8(mp4_filepath, m3u8_directory)


def help_command():
    """帮助命令, 用于获取帮助信息.

    Example:
        ```shell
        w2g-cli help
        ```
    """
    help_msg = f"""一起看电影命令行工具 {__version__}

Bunnyburrow Software Project(兔窝镇软件计划)
Copyright 2023 Steve R. Sun. All rights reserved.
--------------------------------------------------
使用方法:
  w2g-cli convert
    将视频从mp4格式转换成m3u8格式.
  w2g-cli help
    获取帮助信息.
  w2g-cli version
    查看命令行工具版本.
"""
    logger.info(help_msg)


def version_command():
    """查看版本命令, 用于查看命令行工具版本.

    Example:
        ```shell
        w2g-cli version
        ```
    """
    logger.info(f'一起看电影命令行工具 {__version__}')
