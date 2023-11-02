import logging

from logging import Formatter
from logging import FileHandler, StreamHandler


class Logger(logging.Logger):
    """日志记录器."""
    def __init__(self,
                 name: str,
                 show_on_console: bool = True,
                 save_to_file: bool = False):
        """初始化日志记录器.

        Args:
            name: str,
                日志记录器的名称.
            show_on_console: bool, default=True,
                是否将日志记录在终端显示.
            save_to_file: bool, default=False,
                是否将日志记录保存到文件.
        """
        super().__init__(name)

        formatter = Formatter(fmt='[%(levelname)s] %(asctime)s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

        if show_on_console:
            stream_handler = StreamHandler()
            stream_handler.setFormatter(formatter)
            # 添加处理器.
            self.addHandler(stream_handler)

        if save_to_file:
            file_handler = FileHandler(filename=name + '.log',
                                       encoding='UTF-8')
            file_handler.setFormatter(formatter)
            # 添加处理器.
            self.addHandler(file_handler)
