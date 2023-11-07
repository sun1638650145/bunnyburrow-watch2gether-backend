import argparse
import sys

from typing import List

from watch2gether.experimental_command_wrapper import (
    version_command
)


def parse_args(args: List[str]) -> argparse.Namespace:
    """解析命令行参数.

    Args:
        args: list of str,
            命令行参数组成的字符串列表.

    Return:
        (解析后)参数组成的容器.
    """
    parser = argparse.ArgumentParser(usage='w2g-cli {version}',
                                     add_help=False,
                                     exit_on_error=False)
    subparsers = parser.add_subparsers(dest='command')

    if len(args) < 2:  # 没有参数.
        sys.exit(2)
    else:
        args = args[1:]

        # 查看版本命令.
        subparsers.add_parser('version',
                              usage='w2g-cli version',
                              description='查看命令行工具版本.')

        return parser.parse_args(args)


def run():
    """启动命令行工具."""
    try:
        args = parse_args(sys.argv)

        if args.command == 'version':
            version_command()
    except argparse.ArgumentError:
        sys.exit(2)
