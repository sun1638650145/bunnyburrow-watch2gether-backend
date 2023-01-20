import os

from pathlib import Path
from typing import Union

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from uvicorn import run

from watch2gether import __version__ as w2g_version

app = FastAPI(version=w2g_version)
video_directory = Path()  # 视频文件夹路径.


@app.get('/video/{video_name}/')
def redirect_streaming_wrapper(video_name: str) -> RedirectResponse:
    """重定向视频流媒体.

    Args:
        video_name: str,
            视频名称(路径参数), 用于访问播放的流媒体视频.
    """
    return RedirectResponse(url=f'/file/{video_name}.m3u8',
                            status_code=301)


@app.get('/file/{file_name}')
def create_vod_streaming(file_name: str) -> FileResponse:
    """创建流媒体(点播)服务.

    Args:
        file_name: str,
            m3u8文件名称(路径参数), 用于访问播放的流媒体视频的m3u8索引.

    Return:
        ts文件视频流.
    """
    return FileResponse(path=os.path.join(Path(video_directory), file_name))


def launch_streaming(video_dir: Union[str, os.PathLike],
                     host: str = '127.0.0.1',
                     port: int = 8000):
    """启动流媒体服务.

    Args:
        video_dir: str or os.PathLike,
            流媒体视频文件夹路径.
        host: str, default='127.0.0.1',
            主机地址.
        port: int, default=8000,
            端口号.
    """
    # 通过修改全局变量传递视频文件夹路径给流媒体媒体服务.
    global video_directory
    video_directory = video_dir

    run(app, host=host, port=port)
