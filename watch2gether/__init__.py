"""一起看电影.

Bunnyburrow Software Project(兔窝镇软件计划)
Copyright 2023-2024 Steve R. Sun. All rights reserved.
"""
__version__ = '0.1b2'

from fastapi import FastAPI

from watch2gether.logger import Logger
# 设置系统logger.
logger = Logger('watch2gether')

from watch2gether.core import convert_mp4_to_m3u8
from watch2gether.core import streaming
from watch2gether.core import websocket

app = FastAPI(version=__version__)
# 导入路由.
app.include_router(streaming.router)
app.include_router(websocket.router)
