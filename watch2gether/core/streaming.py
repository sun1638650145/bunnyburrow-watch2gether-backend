import os

from pathlib import Path

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import FileResponse, RedirectResponse

from watch2gether import logger
from watch2gether.core import get_current_time

router = APIRouter()
video_directory = Path()  # 视频文件夹路径.


@router.get('/video/{video_name}/')
async def redirect_streaming_wrapper(video_name: str) -> RedirectResponse:
    """重定向视频流媒体.

    Args:
        video_name: str,
            视频名称(路径参数), 用于访问播放的流媒体视频.

    Return:
        HTTP重定向到`/file/{video_name}.m3u8`.
    """
    return RedirectResponse(url=f'/file/{video_name}.m3u8',
                            status_code=301)


@router.get('/file/{file_name}')
async def create_vod_streaming(request: Request,
                               file_name: str) -> FileResponse:
    """创建流媒体(点播)服务.

    Args:
        request: Request,
            一个Request请求.
        file_name: str,
            m3u8文件名称(路径参数), 用于访问播放的流媒体视频的m3u8索引.

    Return:
        ts文件视频流.
    """
    # TODO(Steve): 通过修改全局变量传递视频文件夹路径给流媒体媒体服务, 耦合较高.
    file_path = os.path.join(Path(video_directory), file_name)
    response = FileResponse(file_path)

    logger.info(f'{get_current_time()}: '
                f'客户端({request.client.host}:{request.client.port})\n'
                f'请求文件: {file_path}\t响应状态码: {response.status_code}.')

    return response
