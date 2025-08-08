import os
import sys

from pathlib import Path
from typing import Union
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote
from urllib.request import urlretrieve

import m3u8

from watch2gether import logger


def download_m3u8(url: str, m3u8_directory: Union[str, os.PathLike]) -> Path:
    """解析并下载指定URL的m3u8流媒体视频文件到本地.

    Args:
        url: str,
            m3u8流媒体视频的URL.
        m3u8_directory: str or os.PathLike,
            m3u8文件夹的保存路径.

    Returns:
        m3u8文件夹的绝对路径.
    """
    # 将URL转换成百分号编码.
    url = quote(url, safe='/:')

    # 创建用于保存m3u8的文件夹.
    os.makedirs(Path(m3u8_directory).absolute(), exist_ok=True)

    try:
        playlist = m3u8.load(uri=url)

        # 保存m3u8播放列表文件.
        playlist.dump(filename=os.path.join(m3u8_directory, unquote(Path(url).stem) + '.m3u8'))  # noqa: E501

        for segment in playlist.segments:
            segment_url = playlist.base_uri + segment.uri
            # 下载对应的ts分片文件.
            urlretrieve(url=segment_url, filename=os.path.join(m3u8_directory, segment.uri))  # noqa: E501
    except HTTPError:
        logger.error('没有找到流媒体视频文件, 请检查你输入的URL!')
        sys.exit(1)
    except URLError:
        logger.error('请检查你的网络连接!')
        sys.exit(1)

    return Path(m3u8_directory).absolute()
