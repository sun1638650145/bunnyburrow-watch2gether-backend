import os
import sys

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, Optional, Tuple, Union
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

import m3u8

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from m3u8 import M3U8, Segment

from watch2gether import logger


KeyIVPair = Tuple[bytes, bytes]


def download_key_iv(playlist: M3U8, info: bool = False) -> Optional[KeyIVPair]:
    """下载密钥和初始化向量(IV).

    Args:
        playlist: M3U8,
            m3u8播放列表.
        info: bool, default=False,
            是否显示下载密钥和初始化向量(IV)的信息.

    Returns:
        密钥和初始化向量(IV), 当m3u8播放列表没有密钥信息时则返回None.
    """
    if key_object := playlist.keys[0]:
        key = urlopen(key_object.uri).read()
        iv = bytes.fromhex(key_object.iv[2:])  # 去掉十六进制字符串前导`0x`.

        if info:
            print('密钥和初始化向量(IV)下载成功:)')

        return key, iv
    else:
        return None


def download_for_segment(segment: Segment,
                         segment_filename: Union[str, os.PathLike],
                         key_iv_pair: Optional[KeyIVPair] = None,
                         headers: Optional[Dict] = None):
    """下载一个分片文件到本地,
    提供密钥和初始化向量(IV)时会对文件进行AES-128-CBC解密.

    Args:
        segment: Segment,
            要下载的单个分片文件.
        segment_filename: str or os.PathLike,
            分片文件的保存路径.
        key_iv_pair: KeyIVPair, default=None,
            密钥和初始化向量(IV).
        headers: Dict, default=None,
            HTTP标头.
    """
    # 构造HTTP标头, 模拟浏览器请求避免`403`错误.
    if headers is None:
        headers = {
            'Referer': segment.absolute_uri,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 '  # noqa: E501
                          'Safari/605.1.15'
        }
    request = Request(url=segment.absolute_uri, headers=headers)

    # 打开对应的分片数据到内存中.
    with urlopen(url=request) as response:
        data = response.read()

    # 对分片文件进行解密.
    if key_iv_pair and (key := key_iv_pair[0]) and (iv := key_iv_pair[1]):
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        # 对数据进行解密.
        data = decryptor.update(data) + decryptor.finalize()

        # 解密后删除密钥.
        segment.key = None

    # 保存分片文件.
    with open(segment_filename, 'wb') as fp:
        fp.write(data)

    # 重命名为使用相对路径的分片文件.
    segment.uri = Path(segment_filename).name


def download_m3u8(url: str,
                  m3u8_directory: Union[str, os.PathLike],
                  max_workers: int = 8,
                  info: bool = False) -> Path:
    """解析并下载指定URL的m3u8流媒体视频文件到本地.

    Args:
        url: str,
            m3u8流媒体视频的URL.
        m3u8_directory: str or os.PathLike,
            m3u8文件夹的保存路径.
        max_workers: int, default=8,
            下载时使用的线程数.
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

        # 检测是否使用了变体流(Variant Stream)技术.
        if playlist.is_variant:
            if info:
                print('检测到变体流(Variant Stream), 将下载最高画质的流媒体视频...')  # noqa: E501

            url = max(playlist.playlists, key=lambda p: p.stream_info.bandwidth).absolute_uri  # noqa: E501
            playlist = m3u8.load(uri=url)

        # 尝试下载密钥和初始化向量(IV), 可能返回值为None.
        key_iv = download_key_iv(playlist, info)

        total_segments = len(playlist.segments)
        idx_padding_width = len(str(total_segments))  # 显示下载进度占位宽度.

        # 使用线程池并行下载分片.
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for idx, segment in enumerate(playlist.segments):
                # 获取分片文件的扩展名.
                suffix = Path(urlparse(url=segment.uri).path).suffix

                futures.append(
                    executor.submit(download_for_segment,
                                    segment=segment,
                                    segment_filename=os.path.join(m3u8_directory, f'stream_{idx}{suffix}'),  # noqa: E501
                                    key_iv_pair=key_iv)
                )

            if info:
                for idx, future in enumerate(futures):
                    future.result()

                    precent = int(idx / total_segments * 100)
                    print(f'\r{precent:>3}%|{"█" * (precent // 10) + " " * (10 - precent // 10)}|'  # noqa: E501
                          f' {idx + 1:>{idx_padding_width}}/{total_segments}'
                          f' 下载分片: stream_{idx}{suffix}', end='')

        # 保存m3u8播放列表文件.
        playlist.dump(filename=os.path.join(m3u8_directory, Path(m3u8_directory).stem + '.m3u8'))  # noqa: E501

        if info:
            end_padding = ' ' * len(f'stream_{total_segments - 1}{suffix}')  # noqa: E501 使用最后一个分片文件长度清除进度显示的残留字符.
            print(f'\r100%|██████████| {total_segments}/{total_segments} 下载完成:){end_padding}')  # noqa: E501
    except HTTPError:
        logger.error('没有找到流媒体视频文件, 请检查你输入的URL!')
        sys.exit(1)
    except URLError:
        logger.error('请检查你的网络连接!')
        sys.exit(1)

    return Path(m3u8_directory).absolute()
