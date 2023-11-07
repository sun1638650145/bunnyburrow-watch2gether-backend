from logging import Formatter

from watch2gether import __version__
from watch2gether import experimental_logger as logger

# 针对命令行模式对日志记录器进行自定义.
logger.removeHandler(logger.file_handler)
logger.stream_handler.setFormatter(Formatter(fmt='%(message)s'))


def version_command():
    """查看版本命令.

    Example:
        ```shell
        w2g-cli version
        ```
    """
    logger.info(f'一起看电影命令行工具 {__version__}')
