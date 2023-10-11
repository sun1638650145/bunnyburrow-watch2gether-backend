from datetime import datetime

from watch2gether.core.convert import convert_mp4_to_m3u8
from watch2gether.core.websockets import websocket


def get_current_time() -> str:
    """获取当前时间."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
