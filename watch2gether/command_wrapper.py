import os

from logging import Formatter
from pathlib import Path
from typing import List, Optional, Union

from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from watch2gether import __version__
from watch2gether import app
from watch2gether import convert_mp4_to_m3u8
from watch2gether import download_m3u8
from watch2gether import logger
from watch2gether import streaming


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


def download_command(url: str, m3u8_directory: str, max_workers: str):
    """流媒体视频下载命令.

    Example:
        ```shell
        w2g-cli download https://www.example.com/video.m3u8 ./video/
        ```

    Args:
        url: str,
            m3u8流媒体视频的URL.
        m3u8_directory: str,
            m3u8文件夹的保存路径.
        max_workers: str,
            下载时使用的线程数.
    """
    download_m3u8(url, m3u8_directory, int(max_workers), info=True)


def help_command():
    """帮助命令, 用于获取帮助信息.

    Example:
        ```shell
        w2g-cli help
        ```
    """
    help_msg = f"""一起看电影命令行工具 {__version__}

Bunnyburrow Software Project(兔窝镇软件计划)
Copyright 2023-2025 Steve R. Sun. All rights reserved.
--------------------------------------------------
使用方法:
  w2g-cli convert mp4_filepath m3u8_directory
    将视频从mp4格式转换成m3u8格式.
    参数:
      mp4_filepath: mp4文件的路径.
      m3u8_directory: m3u8文件夹的路径.
  w2g-cli download [-w MAX_WORKERS] url m3u8_directory
    解析并下载指定URL的m3u8流媒体视频文件到本地.
    参数:
      url: m3u8流媒体视频的URL.
      m3u8_directory: m3u8文件夹的保存路径.
    可选参数:
      -w, --max_workers: 下载时使用的线程数, 默认为8.
  w2g-cli help
    获取帮助信息.
  w2g-cli launch [--host] [--port] [--origins] [--log_filepath]
                 [--ssl_key_filepath] [--ssl_cert_filepath] videos_directory
    启动流媒体和WebSocket服务.
    参数:
      videos_directory: 全部流媒体视频的文件夹.
    可选参数:
      --host: 使用的主机地址, 默认为127.0.0.1.
      --port: 绑定的端口号, 默认为8000.
      --origins: CORS(跨域资源共享)允许的源列表, 默认为空.
      --log_filepath: 日志文件的路径, 默认将日志输出到终端.
      --ssl_key_filepath: SSL私钥文件的路径, 默认不启用SSL协议.
      --ssl_cert_filepath: SSL证书文件的路径, 默认不启用SSL协议.
  w2g-cli one [--host] [--port] [--origins] [--log_filepath]
              [--ssl_key_filepath] [--ssl_cert_filepath] mp4_filepath
    自动转换视频格式并启动流媒体和WebSocket服务.
    参数:
      mp4_filepath: mp4文件的路径.
    可选参数:
      --host: 使用的主机地址, 默认为127.0.0.1.
      --port: 绑定的端口号, 默认为8000.
      --origins: CORS(跨域资源共享)允许的源列表, 默认为空.
      --log_filepath: 日志文件的路径, 默认将日志输出到终端.
      --ssl_key_filepath: SSL私钥文件的路径, 默认不启用SSL协议.
      --ssl_cert_filepath: SSL证书文件的路径, 默认不启用SSL协议.
  w2g-cli version
    查看命令行工具版本.
"""
    logger.info(help_msg)


def launch_command(host: str,
                   port: str,
                   origins: List[str],
                   log_filepath: Optional[str],
                   ssl_key_filepath: Optional[str],
                   ssl_cert_filepath: Optional[str],
                   videos_directory: Union[str, os.PathLike]):
    """服务启动命令, 用于启动流媒体和WebSocket服务.

    Example:
        ```shell
        w2g-cli launch ./video/
        ```

    Args:
        host: str,
            使用的主机地址.
        port: str,
            绑定的端口号.
        origins: list of str,
            CORS(跨域资源共享)允许的源列表.
        log_filepath: str,
            日志文件的路径.
        ssl_key_filepath: str,
            SSL私钥文件的路径.
        ssl_cert_filepath: str,
            SSL证书文件的路径.
        videos_directory: str or os.PathLike,
            全部流媒体视频的文件夹.
    """
    # 设置CORS(跨域资源共享).
    if origins:
        app.add_middleware(
            middleware_class=CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
    # 设置将日志保存到文件.
    if log_filepath:
        logger.add_file_handler(log_filepath)
        logger.removeHandler(logger.stream_handler)
    # 设置流媒体视频的资源文件夹.
    streaming.videos_directory = videos_directory

    if ssl_key_filepath and ssl_cert_filepath:
        protocol, ws_protocol = 'https', 'wss'
    else:
        protocol, ws_protocol = 'http', 'ws'
        logger.warning('未启用SSL协议, 服务运行在非加密模式下!')

    logger.info(f'流媒体服务: 成功启动在 {protocol}://{host}:{port}/video/')
    logger.info(f'WebSocket服务: 成功启动在 {ws_protocol}://{host}:{port}/ws/')

    run(app,
        host=host,
        port=int(port),
        log_level='error',
        ssl_keyfile=ssl_key_filepath,
        ssl_certfile=ssl_cert_filepath)


def one_command(host: str,
                port: str,
                origins: List[str],
                log_filepath: Optional[str],
                ssl_key_filepath: Optional[str],
                ssl_cert_filepath: Optional[str],
                mp4_filepath: str):
    """自动转换视频格式并启动流媒体和WebSocket服务.

    Example:
        ```shell
        w2g-cli one ./flower.mp4
        ```

    Args:
        host: str,
            使用的主机地址.
        port: str,
            绑定的端口号.
        origins: list of str,
            CORS(跨域资源共享)允许的源列表.
        log_filepath: str,
            日志文件的路径.
        ssl_key_filepath: str,
            SSL私钥文件的路径.
        ssl_cert_filepath: str,
            SSL证书文件的路径.
        mp4_filepath: str,
            mp4文件的路径.
    """
    # 设置将日志保存到文件.
    if log_filepath:
        logger.add_file_handler(log_filepath)
        logger.removeHandler(logger.stream_handler)

    videos_directory = convert_mp4_to_m3u8(mp4_filepath,
                                           Path(mp4_filepath).stem)
    # 调用服务启动命令, 实现代码复用.
    launch_command(host,
                   port,
                   origins,
                   None,  # 避免再创建一个相同的logger.
                   ssl_key_filepath,
                   ssl_cert_filepath,
                   videos_directory)


def version_command():
    """查看版本命令, 用于查看命令行工具版本.

    Example:
        ```shell
        w2g-cli version
        ```
    """
    logger.info(f'一起看电影命令行工具 {__version__}')
