from uvicorn import run

from watch2gether import app
from watch2gether import streaming


def launch_command(video_dir: str,
                   host: str,
                   port: int):
    """启动服务命令, 用于启动流媒体服务和WebSocket服务.

    Example:
        ```shell
        w2g-cli launch ./flower/
        ```

    Args:
        video_dir: str,
            流媒体视频文件夹路径.
        host: str,
            使用的主机地址.
        port: int,
            绑定的端口号.
    """
    # 通过修改全局变量传递流媒体视频文件夹路径给流媒体服务.
    streaming.video_directory = video_dir

    run(app, host=host, port=port, log_level='error')
