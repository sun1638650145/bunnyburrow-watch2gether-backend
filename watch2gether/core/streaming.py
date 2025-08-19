import os

from pathlib import Path

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse

from watch2gether import logger


router = APIRouter()
videos_directory = Path()  # 全部流媒体视频的文件夹.


@router.get('/video/{video_name}/')
async def redirect_streaming_wrapper(video_name: str) -> RedirectResponse:
    """重定向视频流媒体.

    Args:
        video_name: str,
            视频名称(路径参数), 用于访问播放的流媒体视频.

    Return:
        HTTP重定向到`/videos/{video_name}/{video_name}.m3u8`.
    """
    return RedirectResponse(url=f'/videos/{video_name}/{video_name}.m3u8',
                            status_code=301)


@router.get('/videos/')
async def get_video_directories_endpoint(request: Request,
                                         sort: bool = False) -> JSONResponse:
    """获取流媒体视频目录.

    Args:
        request: Request,
            当前的`Request`请求.
        sort: Bool, default=False,
            是否对返回的数据进行排序.

    Return:
        返回包含流媒体视频目录的JSON响应.
    """
    video_directories = []

    for item in Path(videos_directory).iterdir():
        # 确认该项是目录, 并且目录中包含同名m3u8文件.
        if item.is_dir() and (item / f'{item.name}.m3u8').exists():
            video_directories.append(item.name)

    if sort:
        video_directories.sort()

    logger.info(f'客户端({request.client.host}:{request.client.port})\n'
                f'获取流媒体视频目录成功, 响应状态码: 200.')

    return JSONResponse(content={'videos': video_directories})


@router.get('/videos/{video_directory}/{file_name}')
async def create_vod_streaming_endpoint(request: Request,
                                        video_directory: str,
                                        file_name: str) -> FileResponse:
    """创建流媒体(点播)服务.

    Args:
        request: Request,
            当前的`Request`请求.
        video_directory: str,
            流媒体视频m3u8索引文件和ts文件所处的文件夹(路径参数),
            一般和视频同名.
        file_name: str,
            请求的文件名(路径参数), 一般只需要请求`视频名.m3u8`即可.

    Return:
        自动顺序返回流媒体视频流.

    Raises:
        HTTPException 404: 如果文件不存在, 则向客户端返回`404`错误.
    """
    # TODO(Steve): 通过修改全局变量传递流媒体视频文件夹路径, 耦合较高.
    file_path = os.path.join(videos_directory, video_directory, file_name)

    if os.path.exists(file_path):
        logger.info(f'客户端({request.client.host}:{request.client.port})\n'
                    f'请求文件:{file_path} 响应状态码: 200.')

        return FileResponse(file_path)
    else:
        logger.warning(f'客户端({request.client.host}:{request.client.port})\n'
                       f'请求不存在文件:{file_path} 响应状态码: 404.')

        raise HTTPException(status_code=404)
