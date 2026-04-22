from typing import Optional

from starlette.requests import HTTPConnection


def get_client_address(connection: HTTPConnection) -> str:
    """获取客户端的地址.

    Args:
        connection: HTTPConnection,
            HTTP连接对象实例, 例如`Request`或`WebSocket`.

    Return:
        `host:port`格式的客户端地址; 如果无法获取则返回'unknown'.
    """
    host = _get_client_host(connection)
    port = _get_client_port(connection)

    if host is None or port is None:
        return 'unknown'
    else:
        return f'{host}:{port}'


def _get_client_host(connection: HTTPConnection) -> Optional[str]:
    """获取客户端的主机地址.
    优先从请求头`X-Forwarded-For`中获取客户端的真实IP地址.

    Args:
        connection: HTTPConnection,
            HTTP连接对象实例, 例如`Request`或`WebSocket`.

    Return:
        客户端的主机地址.
    """
    client = connection.client
    x_forwarded_for = connection.headers.get('x-forwarded-for')

    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    elif client is not None:
        return client.host
    else:
        return None


def _get_client_port(connection: HTTPConnection) -> Optional[int]:
    """获取客户端的端口号.

    Args:
        connection: HTTPConnection,
            HTTP连接对象实例, 例如`Request`或`WebSocket`.

    Return:
        客户端的端口号.
    """
    client = connection.client

    if client is not None:
        return client.port
    else:
        return None
