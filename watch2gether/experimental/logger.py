import logging

from logging import Formatter
from logging import StreamHandler
from typing import Optional


class Logger(logging.Logger):
    """日志记录器.

    Attributes:
        name: str, default=None,
            日志记录器的名称.
    """
    def __init__(self, name: Optional[str] = None):
        super().__init__(name)

        formatter = Formatter(fmt='[%(levelname)s] %(asctime)s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)

        # 添加处理器.
        self.addHandler(stream_handler)
