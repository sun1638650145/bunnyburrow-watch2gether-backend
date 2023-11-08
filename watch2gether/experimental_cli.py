import argparse
import sys

from typing import IO, List, Optional

from watch2gether.experimental_command_wrapper import (
    help_command,
    version_command
)


class ArgumentParser(argparse.ArgumentParser):
    """命令行参数解析器(本地化错误消息)."""
    def error(self, message: str):
        """输出使用方法和错误消息.

        Args:
            message: str
                错误消息.
        """
        message = message.replace('unrecognized arguments', '未识别的参数')

        self.print_usage()
        sys.stderr.write(f'错误: {message}\n')
        sys.exit(2)

    def print_usage(self, file: Optional[IO[str]] = None):
        """输出使用方法.

        Args:
            file: 继承父类参数.
        """
        sys.stdout.write(f'使用方法: {self.usage}\n')


def parse_args(args: List[str]) -> argparse.Namespace:
    """解析命令行参数.

    Args:
        args: list of str,
            命令行参数组成的字符串列表.

    Return:
        (解析后)参数组成的容器.
    """
    parser = ArgumentParser(usage='w2g-cli {version}',
                            add_help=False,
                            exit_on_error=False)
    subparsers = parser.add_subparsers(dest='command')

    if len(args) < 2:  # 没有参数.
        help_command()
        sys.exit(2)
    else:
        args = args[1:]

        # 帮助命令.
        subparsers.add_parser('help',
                              usage='w2g-cli help',
                              add_help=False,
                              description='获取帮助信息.')

        # 查看版本命令.
        subparsers.add_parser('version',
                              usage='w2g-cli version',
                              add_help=False,
                              description='查看命令行工具版本.')

        return parser.parse_args(args)


def run():
    """启动命令行工具."""
    try:
        args = parse_args(sys.argv)

        if args.command == 'help':
            help_command()
        elif args.command == 'version':
            version_command()
    except argparse.ArgumentError:
        help_command()
        sys.exit(2)
