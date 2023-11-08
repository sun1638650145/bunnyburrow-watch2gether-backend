from logging import Formatter

from watch2gether import __version__
from watch2gether import experimental_logger as logger


# 命令行工具对日志格式进行自定义.
logger.stream_handler.setFormatter(Formatter(fmt='%(message)s'))


def help_command():
    """"""
    help_msg = f"""一起看电影命令行工具 {__version__}

Bunnyburrow Software Project(兔窝镇软件计划)
Copyright 2023 Steve R. Sun. All rights reserved.
--------------------------------------------------
使用方法:
  w2g-cli help
    获取帮助信息.
  w2g-cli version
    查看命令行工具版本.
"""
    logger.info(help_msg)


def version_command():
    """查看版本命令.

    Example:
        ```shell
        w2g-cli version
        ```
    """
    logger.info(f'一起看电影命令行工具 {__version__}')
