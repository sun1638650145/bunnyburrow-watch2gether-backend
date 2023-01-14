from typing import Generator

import m3u8
import uvicorn

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from watch2gether import __version__ as w2g_version

app = FastAPI(version=w2g_version)


@app.get('/video/{video_name}')
def create_streaming(video_name: str) -> StreamingResponse:
    """创建流媒体服务.

    Args:
        video_name: str,
            视频名称(路径参数), 用于访问播放的流媒体视频.

    Return:
        m3u8视频流响应.
    """
    def _video_streamer() -> Generator:
        # 解析m3u8文件, 加载播放列表.
        playlist = m3u8.load(uri=f'./{video_name}/playlist.m3u8')
        # 读取HLS视频流片段.
        for segment in playlist.segments:
            yield open(segment.absolute_uri, 'rb').read()

    return StreamingResponse(content=_video_streamer(),
                             media_type='application/x-mpegURL')


def launch_streaming(host: str = '127.0.0.1',
                     port: int = 8000):
    """启动流媒体服务.

    Args:
        host: str, default='127.0.0.1',
            主机地址.
        port: int, default=8000,
            端口号.
    """
    uvicorn.run(app, host=host, port=port)
