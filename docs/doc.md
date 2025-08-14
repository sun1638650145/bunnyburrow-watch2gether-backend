# 一起看电影(backend) 🎦

[![build](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/build.yml/badge.svg)](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/build.yml) [![package](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/package.yml/badge.svg)](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/package.yml) [![codecov](https://codecov.io/gh/sun1638650145/bunnyburrow-watch2gether-backend/branch/master/graph/badge.svg?token=2OCJQLENZ5)](https://codecov.io/gh/sun1638650145/bunnyburrow-watch2gether-backend)

<b>一起看电影</b>是[Bunnyburrow Software Project(兔窝镇软件计划)](https://github.com/sun1638650145/bunnyburrow)的第3个项目, 旨在帮助你搭建流媒体服务, 与朋友们共享观影时光. 🍿🎥

<b>一起看电影(backend)</b>作为服务器端子项目,  为系统提供核心支持. 你可以自由选择适合自己的客户端, 当前支持一下两种:

* [Web客户端](https://github.com/sun1638650145/bunnyburrow-watch2gether-web)
* [iOS客户端](https://github.com/sun1638650145/bunnyburrow-watch2gether-app)

此外, 你可以根据[WebSockets协议](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/blob/master/docs/websockets.md)自行开发客户端, 以满足个性化需求.

## 安装

仅需要`Python`环境, 在[发布页](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/releases)下载最新的稳定版`whl`文件即可.

```shell
# 安装插件.
pip install watch2gether-0.1b2-py3-none-any.whl
# 强烈推荐安装到虚拟环境, 并创建符号链接.
ln -s /path/to/bin/w2g-cli /usr/local/bin/w2g-cli
```

## 使用方法

<b>一起看电影(backend)</b>目前提供2种灵活的使用方法.

### 1. 使用`w2g-cli`命令行工具 💻

这种方式适合大多数的人, 下面的`shell`脚本展示了一个标准的使用流程.

```shell
# 将视频从mp4格式转换成m3u8格式.
w2g-cli convert ./我们亲爱的Steve.mp4 ./我们亲爱的Steve/

# 监听所有主机地址, 启动流媒体和WebSocket服务.
w2g-cli launch --host 0.0.0.0 ./
```

同时, 如果你第一次启动可以考虑更简化的`one`命令, `one`命令只需要提供一个`mp4`视频即可自动启动服务.

```shell
# 监听所有主机地址并绑定在80端口, 自动转换视频格式并启动流媒体和WebSocket服务.
w2g-cli one --host 0.0.0.0 --port 80 ./我们亲爱的Steve.mp4
```

更多详细信息请使用`help`命令获取.

### 2. 在Python 🐍 脚本中使用

一起看电影(backend)的后端目前提供了3个服务, 包括将视频从`mp4`格式转换成`m3u8`格式, 创建流媒体服务以及`WebSocket`服务. 一起看电影采用前后端分离的设计模式, 这使得后端可以灵活接入多种类型的客户端. 下面的`python`脚本提供了一个标准的开发模版.

```python
import watch2gether as w2g
import uvicorn

# 将视频从mp4格式转换成m3u8格式, 并设置全部流媒体视频的文件夹.
w2g.streaming.videos_directory = w2g.convert_mp4_to_m3u8('./我们亲爱的Steve.mp4',
                                                         './我们亲爱的Steve/')
# 启动流媒体服务和WebSocket服务.
uvicorn.run(app=w2g.app,
            host='0.0.0.0',
            port=80)
```

下面将详细介绍每个函数和API的功能.

#### convert_mp4_to_m3u8

将视频从`mp4`格式转换成`m3u8`格式, 以满足对流媒体的支持.

##### 警告 ⚠️

此函数依赖`ffmpeg`命令, 需安装`ffmpeg`, 同时如不了解`ffmpeg`的使用, 建议使用默认参数.

```python
convert_mp4_to_m3u8(mp4_filepath,
                    m3u8_directory,
                    video_encoder='libx264',
                    audio_encoder='aac',
                    crf=23,
                    preset='veryfast',
                    bitrate=128,
                    audio_channels=2,
                    log_level='error',
                    m3u8_format='hls',
                    hls_time=2,
                    hls_playlist_type='vod',
                    hls_segment_filename='stream')
```

##### 参数

- **mp4_filepath**: 字符串或路径, `mp4`文件的路径, 封装参数`ffmpeg -i input.mp4`.
- **m3u8_directory**: 字符串或路径, `m3u8`文件夹的路径, 封装参数`ffmpeg output.m3u8`.
- **video_encoder**: 字符串, 默认为`'libx264'`, 视频编码器, 封装参数`ffmpeg -c:v libx264`, 支持的编码器请使用`ffmpeg -codecs`查看.
- **audio_encoder**: 字符串, 默认为`'aac'`, 音频编码器, 封装参数`ffmpeg -c:a aac`, 支持的编码器请使用`ffmpeg -codecs`查看.
- **crf**: 整数, 默认为`23`, `m3u8`文件的视频压缩质量(Constant Rate Factor), 封装参数`ffmpeg -crf 23`, 取值范围[0, 51], 推荐选择范围[17, 28], 注意crf值越小, 视频质量越高, 转换时间越长.
- **preset**: `Preset`字符串, 默认为`'veryfast'`, 编码速度与压缩比, 封装参数`ffmpeg -preset veryfast`.
- **bitrate**: 整数, 默认为`128`, `m3u8`文件的音频的比特率, 单位为kbit/s. 封装参数`ffmpeg -b:a 128k`.
- **audio_channels**: 整数, 默认为`2`, `m3u8`文件的音频的声道数, 封装参数`ffmpeg -ac 2`.
- **log_level**: `LogLevel`字符串, 默认为`'error'`, 设置使用的日志记录级别, 封装参数`ffmpeg -loglevel error`.
- **m3u8_format**: 字符串, 默认为`'hls'`, 输出文件的封装格式, 封装参数`ffmpeg -f hls`, 支持的封装格式请使用`ffmpeg -formats`查看.
- **hls_time**: 整数, 默认为`2`, HLS视频流片段的时长, 封装参数`ffmpeg -f hls -hls_time 2`, 仅在输出文件的封装格式为HLS时有效.
- **hls_playlist_type**: `HLSPlaylistType`字符串, 默认为`'vod'`, HLS视频播放列表的类型, 封装参数`ffmpeg -f hls -hls_playlist_type vod`, 仅在输出文件的封装格式为HLS时有效.
- **hls_segment_filename**: 字符串, 默认为`'stream'`, HLS视频流片段的文件名, 默认格式是`'m3u8_directory/stream_%d.ts'`, 封装参数`ffmpeg -f hls -hls_segment_filename 'm3u8_directory/stream_%d.ts'`, 仅在输出文件的封装格式为HLS时有效.

##### 返回

`m3u8`文件夹的父文件夹的绝对路径.

#### download_m3u8
解析并下载指定URL的m3u8流媒体视频文件到本地.

```python
download_m3u8(url, m3u8_directory, max_workers=8, info=False)
```

##### 参数

* **url**: 字符串, `m3u8`流媒体视频的URL.
* **m3u8_directory**: 字符串或路径, `m3u8`文件夹的保存路径.
* **max_workers**: 整数, 默认为`8`, 下载时使用的线程数.
* **info**: 布尔类型, 默认为`False`, 是否显示详细的下载进度信息.

##### 返回

`m3u8`文件夹的绝对路径.

#### streaming.videos_directory

全部流媒体视频的文件夹.

```python
streaming.videos_directory = '/path/to/videos_directory/'
```

#### *(GET)* /video/{video_name}/

重定向视频流媒体.

##### 参数

- **video_name**: 字符串, 视频名称(路径参数), 用于访问播放的流媒体视频.

##### 返回

HTTP重定向到`/videos/{video_name}/{video_name}.m3u8`.

#### *(GET)* /videos/{video_directory}/{file_name}

创建流媒体(点播)服务.

##### 参数

- **request**: `Request`实例, 当前的`Request`请求.
- **video_directory**: 字符串, 流媒体视频`m3u8`索引文件和`ts`文件所处的文件夹(路径参数), 一般和视频同名.
- **file_name**: 字符串, 请求的文件名(路径参数), 一般只需要请求`视频名.m3u8`即可.

##### 返回

自动顺序返回流媒体视频流.

##### 异常

**HTTPException 404**: 如果文件不存在, 则向客户端返回`404`错误.

#### *(WEBSOCKET)* /ws/{client_id}/

创建`WebSocket`服务.

##### 参数

- `client_id`: 整数, `WebSocket`客户端ID.

- `websocket`: `WebSocket`, `WebSocket`实例.

## 部署建议 ⚙️

尽管本项目可以通过`w2g-cli`命令行工具启动服务, 但在生产环境中, 我们<b>强烈建议</b>使用`nginx`作为反向代理服务器来部署应用.

### nginx配置示例

```nginx
worker_processes auto; # 根据CPU核心数量定义工作进程的数量.

events {
    worker_connections 1024; # 单个工作进程的最大未完成异步I/O操作数.
}

http {
    # 配置HTTP服务器监听80端口.
    server {
        listen 80;
        server_name localhost;
        
        location / {
            return 301 https://$host$request_uri; # 将HTTP请求重定向到对应的HTTPS地址(记得包含主机头字段和请求参数的原始URI).
        }
    }
    
    # 配置HTTPS服务器监听443端口.
    server {
        listen 443 ssl; # 启用SSL/TLS加密.
        server_name localhost;
        
        ssl_certificate /path/to/your.pem;     # SSL证书文件的路径.
        ssl_certificate_key /path/to/your.key; # SSL私钥文件的路径.
        
        location / {
            proxy_pass http://127.0.0.1:8000/;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # 记录请求经过的代理服务器链路信息以及获取真实客户端IP.
        }
        
        # WebSocket代理.
        location /ws/ {
            proxy_pass http://127.0.0.1:8000/ws/;   # 使用http而不使用ws.
            proxy_http_version 1.1;                 # 将连接从HTTP/1.1转换为WebSocket.
            proxy_set_header Connection "upgrade";  # 设置hop-by-hop字段Connection为"upgrade", 告知后端服务器升级协议.
            proxy_set_header Upgrade $http_upgrade; # 将hop-by-hop字段Upgrate传递给后端服务器.
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

