import logging
import os

from logging import Formatter
from logging import FileHandler, StreamHandler
from typing import Optional, Union


class Logger(logging.Logger):
    """日志记录器.

    Attributes:
        formatter: Formatter,
            日志格式器.
        file_handler: FileHandler, default=None,
            文件处理器(默认没有添加, 需要手动添加), 将日志保存到文件.
        stream_handler: StreamHandler,
            数据流处理器, 将日志输出到终端.
    """
    def __init__(self, name: str):
        """初始化日志记录器.

        Args:
            name: str,
                日志记录器的名称.
        """
        super().__init__(name)

        self.formatter = Formatter(fmt='[%(levelname)s] %(asctime)s %(message)s',  # noqa: E501
                                   datefmt='%Y-%m-%d %H:%M:%S')

        self.file_handler: Optional[FileHandler] = None
        # 添加数据流处理器.
        self.stream_handler = StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
        self.addHandler(self.stream_handler)

    def add_file_handler(self, filepath: Union[str, os.PathLike]):
        """添加文件处理器.

        Args:
            filepath: str or os.PathLike,
                日志文件的路径.
        """
        self.file_handler = FileHandler(filename=filepath, encoding='UTF-8')
        self.file_handler.setFormatter(self.formatter)
        self.addHandler(self.file_handler)
