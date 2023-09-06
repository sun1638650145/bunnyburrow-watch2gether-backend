# 一起看电影(backend) 🎦

[![build](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/build.yml/badge.svg)](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/build.yml) [![package](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/package.yml/badge.svg)](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/package.yml) [![codecov](https://codecov.io/gh/sun1638650145/bunnyburrow-watch2gether-backend/branch/master/graph/badge.svg?token=2OCJQLENZ5)](https://codecov.io/gh/sun1638650145/bunnyburrow-watch2gether-backend)

一起看电影是[Bunnyburrow Software Project(兔窝镇软件计划)](https://github.com/sun1638650145/bunnyburrow)的第3个组件, 你可以使用它创建流媒体服务并和朋友们一起看. 

## 安装

仅需要`Python`环境, 在发布页下载最新的稳定版`whl`文件即可.

```shell
# 安装插件.
pip install https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/releases/download/v0.1b0/watch2gether-0.1b0-py3-none-any.whl
# 强烈推荐安装到虚拟环境, 并添加环境变量到shell.
echo alias w2g-cli=/path/to/bin/w2g-cli >> .zshrc
```

## 使用方法

一起看电影(backend)目前提供2种灵活的使用方法.

### 1. 使用`w2g-cli`命令行工具 💻

这种方式适合大多数的人, 下面的`shell`脚本展示了一个标准的使用流程.

```shell
# 将视频从mp4格式转换成m3u8格式.
w2g-cli convert ./我们亲爱的Steve.mp4 ./我们亲爱的Steve/
# 监听所有主机地址, 启动流媒体和WebSocket服务.
w2g-cli launch --host 0.0.0.0 ./我们亲爱的Steve/
```

同时, 如果你第一次启动可以考虑更简化的`one`命令, `one`命令将在当前目录下自动处理并生成`m3u8`格式视频.

```shell
# 自动处理mp4视频并监听所有主机地址, 启动流媒体服务和WebSocket服务.
w2g-cli one --host 0.0.0.0 ./我们亲爱的Steve.mp4
```

### 2. 在Python 🐍 脚本中使用

一起看电影(backend)的后端目前提供了3个服务, 包括将视频从`mp4`格式转换成`m3u8`, 创建流媒体服务以及`WebSocket`服务器. 一起看电影采用前后端分离的设计模式, 这使得前端可以灵活接入多种类型的客户端. 下面的`python`脚本提供了一个标准的开发模版.

```python
import watch2gether as w2g
import uvicorn

# 将mp4视频转换为流媒体视频.
m3u8_dir = w2g.convert_mp4_to_m3u8('./我们亲爱的Steve.mp4', './我们亲爱的Steve/')
# 设置流媒体视频文件夹的路径.
w2g.streaming.video_directory = m3u8_dir
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
- **m3u8_format**: 字符串, 默认为`'hls'`, 输出文件的封装格式, 封装参数`ffmpeg -f hls`, 支持的封装格式请使用`ffmpeg -formats`查看.
- **hls_time**: 整数, 默认为`2`, HLS视频流片段的时长, 封装参数`ffmpeg -f hls -hls_time 2`, 仅在输出文件的封装格式为HLS时有效.
- **hls_playlist_type**: `HLSPlaylistType`字符串, 默认为`'vod'`, HLS视频播放列表的类型, 封装参数`ffmpeg -f hls -hls_playlist_type vod`, 仅在输出文件的封装格式为HLS时有效.
- **hls_segment_filename**: 字符串, 默认为`'stream'`, HLS视频流片段的文件名, 默认格式是`'m3u8_directory/stream_%d.ts'`, 封装参数`ffmpeg -f hls -hls_segment_filename 'm3u8_directory/stream_%d.ts'`, 仅在输出文件的封装格式为HLS时有效.

##### 返回

`m3u8`文件夹的绝对路径.

#### streaming.video_directory

视频文件夹路径.

```python
streaming.video_directory = '/path/to/video_directory/'
```

#### *(GET)* /video/{video_name}/

重定向视频流媒体.

##### 参数

- **video_name**: 字符串, 视频名称(路径参数), 用于访问播放的流媒体视频.

##### 返回

HTTP重定向到`/file/{video_name}.m3u8`.

#### *(GET)* /file/{file_name}

创建流媒体(点播)服务.

##### 参数

- **request**: `Request`实例, 一个Request请求(系统维护, 不需要手动传参).
- **file_name**: 字符串, `m3u8`文件名称(路径参数), 用于访问播放的流媒体视频的`m3u8`索引.

##### 返回

`ts`文件视频流.

##### 异常

**HTTPException 404**: 如果文件不存在, 则向客户端返回`404`错误.

#### *(WEBSOCKET)* /ws/

创建`WebSocket`服务器.

##### 参数

- `websocket`: `WebSocket`实例, 一个`websocket`连接(系统维护, 不需要手动传参).
