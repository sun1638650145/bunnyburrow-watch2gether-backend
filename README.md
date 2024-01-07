# 一起看电影(backend) 🎦

[![build](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/build.yml/badge.svg)](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/build.yml) [![package](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/package.yml/badge.svg)](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/package.yml) [![codecov](https://codecov.io/gh/sun1638650145/bunnyburrow-watch2gether-backend/branch/master/graph/badge.svg?token=2OCJQLENZ5)](https://codecov.io/gh/sun1638650145/bunnyburrow-watch2gether-backend)

一起看电影是[Bunnyburrow Software Project(兔窝镇软件计划)](https://github.com/sun1638650145/bunnyburrow)的第3个组件, 使用它创建流媒体服务, 并与朋友们同步观看影片. 

该项目采用了前后端分离的设计模式. 因此, 这里只介绍其后端服务器部分. 你可以通过此后端启动流媒体服务和WebSocket服务. 至于前端部分, 只需要遵循文档中定义的[WebSockets API](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/blob/master/docs/websockets.md)即可, 无论它的展现形式是Web客户端还是移动App. 目前提供了一个标准的[Web客户端](https://github.com/sun1638650145/bunnyburrow-watch2gether-web).

## 使用指南 🧭

一起看电影(backend)目前提供2种灵活的使用方法. 限于篇幅, 以下仅展示快速上手的步骤, 具体参数和详细信息请参考[官方文档](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/tree/master/docs).

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

一起看电影(backend)的后端目前提供了3项服务, 包括将视频从`mp4`格式转换成`m3u8`格式, 创建流媒体服务以及`WebSocket`服务. 采用前后端分离的设计模式使得后端可以灵活接入多种类型的客户端. 下面的`python`脚本提供了一个标准的开发模版.

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
