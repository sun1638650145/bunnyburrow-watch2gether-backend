import os

from pathlib import Path
from typing import List, Literal, Union

from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from watch2gether import __version__
from watch2gether import app
from watch2gether import convert_mp4_to_m3u8, streaming
from watch2gether import logger

Mode = Literal['error', 'info']


def convert_command(mp4_file: str,
                    m3u8_dir: str):
    """视频格式转换命令, 简化ffmpeg的使用,
    复杂功能请使用Python脚本模式.

    Example:
        ```shell
        w2g-cli convert ./flower.mp4 ./flower/
        ```

    Args:
        mp4_file: str,
            mp4文件的路径.
        m3u8_dir: str,
            m3u8文件夹的路径.
    """
    convert_mp4_to_m3u8(mp4_file, m3u8_dir)


def help_command(level: Mode):
    """帮助命令, 用于查看帮助信息.

    Example:
        ```shell
        w2g-cli help
        ```
    """
    _help_msg = f"""一起看电影命令行工具 {__version__}

Bunnyburrow Software Project(兔窝镇软件计划)
Copyright 2023 Steve R. Sun. All rights reserved.
--------------------------------------------------
usage:
  w2g-cli convert mp4_file m3u8_dir
    将视频从mp4格式转换成m3u8格式.
  w2g-cli help
    获取帮助信息.
  w2g-cli launch [--host] [--port] [--origins] streaming_video
    启动流媒体服务和WebSocket服务.
    options:
      --host: 使用的主机地址, 默认为127.0.0.1.
      --port: 绑定的端口号, 默认为8000.
      --origins: CORS(跨域资源共享)允许的源列表, 默认为空.
  w2g-cli one [--host] [--port] [--origins] mp4_file
    自动处理mp4视频并启动流媒体服务和WebSocket服务.
    options:
      --host: 使用的主机地址, 默认为127.0.0.1.
      --port: 绑定的端口号, 默认为8000.
      --origins: CORS(跨域资源共享)允许的源列表, 默认为空.
  w2g-cli version
    查看命令行工具版本.
"""

    if level == 'error':
        logger.error(_help_msg)
    else:
        logger.info(_help_msg)


def launch_command(videos_dir: Union[str, os.PathLike],
                   host: str,
                   port: int,
                   origins: List[str]):
    """启动服务命令, 用于启动流媒体服务和WebSocket服务.

    Example:
        ```shell
        w2g-cli launch ./flower/
        ```

    Args:
        videos_dir: str or os.PathLike,
            流媒体视频文件夹路径.
        host: str,
            使用的主机地址.
        port: int,
            绑定的端口号.
        origins: list of str,
            CORS(跨域资源共享)允许的源列表.
    """
    # 添加CORS(跨域资源共享)中间件.
    if origins:
        app.add_middleware(
            middleware_class=CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )

    # 通过修改全局变量传递流媒体视频文件夹路径给流媒体服务.
    streaming.videos_directory = videos_dir

    logger.info(f'流媒体服务: 成功启动在 http://{host}:{port}/video/')
    logger.info(f'WebSocket服务: 成功启动在 ws://{host}:{port}/ws/')

    run(app, host=host, port=port, log_level='error')


def one_command(mp4_file: str,
                host: str,
                port: int,
                origins: List[str]):
    """自动处理mp4视频并启动流媒体服务和WebSocket服务.

    Example:
        ```shell
        w2g-cli one ./flower.mp4
        ```

    Args:
        mp4_file: str,
            mp4文件的路径.
        host: str,
            使用的主机地址.
        port: int,
            绑定的端口号.
        origins: list of str,
            CORS(跨域资源共享)允许的源列表.
    """
    videos_dir = convert_mp4_to_m3u8(mp4_file,
                                     Path(mp4_file).stem)  # 默认使用文件名作为m3u8文件名.
    # 调用launch_command实现代码复用.
    launch_command(videos_dir.parent, host, port, origins)


def version_command():
    """查看版本命令.

    Example:
        ```shell
        w2g-cli version
        ```
    """
    logger.info('一起看电影命令行工具 ' + __version__)
