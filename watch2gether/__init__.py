"""一起看电影.

Bunnyburrow Software Project(兔窝镇软件计划)
Copyright 2023 Steve R. Sun. All rights reserved.
"""
__version__ = '0.1b2'

import logging
# 设置系统logger.
logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()

from fastapi import FastAPI

from watch2gether.experimental.logger import Logger
# 设置新系统logger.
experimental_logger = Logger('watch2gether')

from watch2gether.core import convert_mp4_to_m3u8
from watch2gether.core import streaming
from watch2gether.core import websocket

from watch2gether.experimental.core import streaming as experimental_streaming

app = FastAPI(version=__version__)
# 导入路由.
app.include_router(streaming.router)
app.include_router(websocket.router)
app.include_router(experimental_streaming.router)
