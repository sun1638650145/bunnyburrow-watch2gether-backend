import argparse
import sys
from typing import List

from watch2gether.command_wrapper import launch_command


def _parse_args(args: List[str]) -> argparse.Namespace:
    """解析命令行参数.

    Args:
        args: list of str,
            命令行的参数.

    Return:
        命令行解析后的参数Namespace字典.
    """
    parser = argparse.ArgumentParser(usage='w2g-cli {launch}',
                                     add_help=False,
                                     exit_on_error=False)
    subparsers = parser.add_subparsers(dest='command')

    if len(args) < 2:  # 没有参数.
        sys.exit(2)
    else:
        args = args[1:]
        # 启动服务命令.
        parser_launch = subparsers.add_parser('launch',
                                              usage='w2g-cli launch [--host] [--port] video_dir',  # noqa: E501
                                              description='启动流媒体服务和WebSocket服务.')  # noqa: E501
        parser_launch.add_argument('video_dir',
                                   help='流媒体视频文件夹路径.')
        parser_launch.add_argument('--host',
                                   default='127.0.0.1',
                                   help='使用的主机地址, 默认为127.0.0.1.')
        parser_launch.add_argument('--port',
                                   default=8000,
                                   help='绑定的端口号, 默认为8000.')

        return parser.parse_args(args)


def run():
    """启动命令行工具."""
    try:
        meta_data = _parse_args(sys.argv)

        if meta_data.command == 'launch':
            launch_command(meta_data.video_dir,
                           meta_data.host,
                           meta_data.port)
    except argparse.ArgumentError:
        sys.exit(2)
