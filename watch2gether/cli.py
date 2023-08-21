import argparse
import sys
from typing import List

from watch2gether.command_wrapper import (
    convert_command,
    help_command,
    launch_command,
    one_command,
    version_command
)


def _parse_args(args: List[str]) -> argparse.Namespace:
    """解析命令行参数.

    Args:
        args: list of str,
            命令行的参数.

    Return:
        命令行解析后的参数Namespace字典.
    """
    try:
        parser = argparse.ArgumentParser(usage='w2g-cli {convert, help, launch, one, version}',  # noqa: E501
                                         add_help=False,
                                         exit_on_error=False)
    except TypeError:
        # 处理Python 3.8的兼容性问题.
        parser = argparse.ArgumentParser(usage='w2g-cli {convert, help, launch, one, version}',  # noqa: E501
                                         add_help=False)

    subparsers = parser.add_subparsers(dest='command')

    if len(args) < 2:  # 没有参数.
        help_command('error')
        sys.exit(2)
    else:
        args = args[1:]
        # 视频格式转换命令.
        parser_convert = subparsers.add_parser('convert',
                                               usage='w2g-cli convert mp4_file m3u8_dir',  # noqa: E501
                                               description='将视频从mp4格式转换成m3u8格式.')  # noqa: E501
        parser_convert.add_argument('mp4_file',
                                    help='mp4文件的路径.')
        parser_convert.add_argument('m3u8_dir',
                                    help='m3u8文件夹的路径.')

        # 帮助命令.
        subparsers.add_parser('help',
                              usage='w2g-cli help',
                              description='获取帮助信息.')

        # 启动服务命令.
        parser_launch = subparsers.add_parser('launch',
                                              usage='w2g-cli launch [--host] [--port] [--origins] video_dir',  # noqa: E501
                                              description='启动流媒体服务和WebSocket服务.')  # noqa: E501
        parser_launch.add_argument('streaming_video',
                                   help='流媒体视频文件夹路径.')
        parser_launch.add_argument('--host',
                                   default='127.0.0.1',
                                   help='使用的主机地址, 默认为127.0.0.1.')
        parser_launch.add_argument('--port',
                                   default=8000,
                                   help='绑定的端口号, 默认为8000.')
        parser_launch.add_argument('--origins',
                                   nargs='+',
                                   default=[],
                                   help='CORS(跨域资源共享)允许的源列表, 默认为空.')

        # one命令.
        parser_one = subparsers.add_parser('one',
                                           usage='w2g-cli one [--host] [--port] [--origins] mp4_file',  # noqa: E501
                                           description='自动处理mp4视频并启动流媒体服务和WebSocket服务.')  # noqa: E501
        parser_one.add_argument('mp4_file',
                                help='mp4文件的路径.')
        parser_one.add_argument('--host',
                                default='127.0.0.1',
                                help='使用的主机地址, 默认为127.0.0.1.')
        parser_one.add_argument('--port',
                                default=8000,
                                help='绑定的端口号, 默认为8000.')
        parser_one.add_argument('--origins',
                                nargs='+',
                                default=[],
                                help='CORS(跨域资源共享)允许的源列表, 默认为空.')

        # 查看版本命令.
        subparsers.add_parser('version',
                              usage='w2g-cli version',
                              description='查看命令行工具版本.')

        return parser.parse_args(args)


def run():
    """启动命令行工具."""
    try:
        meta_data = _parse_args(sys.argv)

        if meta_data.command == 'convert':
            convert_command(meta_data.mp4_file, meta_data.m3u8_dir)
        elif meta_data.command == 'help':
            help_command('info')
        elif meta_data.command == 'launch':
            launch_command(meta_data.streaming_video,
                           meta_data.host,
                           meta_data.port,
                           meta_data.origins)
        elif meta_data.command == 'one':
            one_command(meta_data.mp4_file,
                        meta_data.host,
                        meta_data.port,
                        meta_data.origins)
        elif meta_data.command == 'version':
            version_command()
    except argparse.ArgumentError:
        help_command('error')
        sys.exit(2)
