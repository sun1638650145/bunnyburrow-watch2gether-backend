import os
import sys

from pathlib import Path
from typing import Union
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote
from urllib.request import urlretrieve

import m3u8

from watch2gether import logger


def download_m3u8(url: str,
                  m3u8_directory: Union[str, os.PathLike],
                  info: bool = False) -> Path:
    """解析并下载指定URL的m3u8流媒体视频文件到本地.

    Args:
        url: str,
            m3u8流媒体视频的URL.
        m3u8_directory: str or os.PathLike,
            m3u8文件夹的保存路径.
        info: bool, default=False,
            是否显示详细的下载进度信息.

    Returns:
        m3u8文件夹的绝对路径.
    """
    # 将URL转换成百分号编码.
    url = quote(url, safe='&/:=?')

    # 创建用于保存m3u8的文件夹.
    os.makedirs(Path(m3u8_directory).absolute(), exist_ok=True)

    try:
        playlist = m3u8.load(uri=url)

        # 保存m3u8播放列表文件.
        playlist.dump(filename=os.path.join(m3u8_directory, unquote(Path(url).stem) + '.m3u8'))  # noqa: E501

        total_segments = len(playlist.segments)
        idx_padding_width = len(str(total_segments))  # 显示下载进度占位宽度.

        for idx, segment in enumerate(playlist.segments, start=1):
            if info:
                precent = int(idx / total_segments * 100)

                print(f'\r{precent:>3}%|{"█" * (precent // 10) + " " * (10 - precent // 10)}|'  # noqa: E501
                      f' {idx:>{idx_padding_width}}/{total_segments}'
                      f' 正在下载分片: {segment.uri}', end='')

            segment_url = playlist.base_uri + segment.uri
            # 下载对应的ts分片文件.
            urlretrieve(url=segment_url, filename=os.path.join(m3u8_directory, segment.uri))  # noqa: E501

        if info:
            print(f'\r100%|██████████| {total_segments}/{total_segments} 下载完成:)')  # noqa: E501

    except HTTPError:
        logger.error('没有找到流媒体视频文件, 请检查你输入的URL!')
        sys.exit(1)
    except URLError:
        logger.error('请检查你的网络连接!')
        sys.exit(1)

    return Path(m3u8_directory).absolute()
