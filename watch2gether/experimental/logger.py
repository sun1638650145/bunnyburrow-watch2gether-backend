import logging

from logging import Formatter
from logging import FileHandler, StreamHandler


class Logger(logging.Logger):
    """日志记录器.

    Attributes:
        file_handler: FileHandler,
            文件处理器(默认没有添加需要手动添加), 将日志保存到文件.
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

        formatter = Formatter(fmt='[%(levelname)s] %(asctime)s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

        self.file_handler = FileHandler(filename=name + '.log', encoding='UTF-8')  # noqa: E501
        self.file_handler.setFormatter(formatter)
        self.stream_handler = StreamHandler()
        self.stream_handler.setFormatter(formatter)

        # 添加处理器.
        self.addHandler(self.stream_handler)
