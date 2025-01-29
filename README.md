# 一起看电影(backend) 🎦

[![build](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/build.yml/badge.svg)](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/build.yml) [![package](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/package.yml/badge.svg)](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/actions/workflows/package.yml) [![codecov](https://codecov.io/gh/sun1638650145/bunnyburrow-watch2gether-backend/branch/master/graph/badge.svg?token=2OCJQLENZ5)](https://codecov.io/gh/sun1638650145/bunnyburrow-watch2gether-backend)

<b>一起看电影</b>是[Bunnyburrow Software Project(兔窝镇软件计划)](https://github.com/sun1638650145/bunnyburrow)的第3个项目, 旨在帮助你搭建流媒体服务, 与朋友们共享观影时光. 🍿🎥

<b>一起看电影(backend)</b>作为服务器端子项目,  为系统提供核心支持. 你可以自由选择适合自己的客户端, 当前支持一下两种:

* [Web客户端](https://github.com/sun1638650145/bunnyburrow-watch2gether-web)
* [iOS客户端](https://github.com/sun1638650145/bunnyburrow-watch2gether-app)

此外, 你可以根据[WebSockets协议](https://github.com/sun1638650145/bunnyburrow-watch2gether-backend/blob/master/docs/websockets.md)自行开发客户端, 以满足个性化需求.


## 快速启动 🚀

<b>一起看电影(backend)</b>目前提供2种灵活的使用方法, 这里介绍更适合大多数用户的`w2g-cli`命令行工具. 你可以使用`help`命令查看详细信息.

以下的`shell`脚本展示了一个标准的使用启动流程:

```shell
# 将视频从mp4格式转换成m3u8格式.
w2g-cli convert ./我们亲爱的Steve.mp4 ./我们亲爱的Steve/

# 监听所有主机地址并绑定在80端口, 启动流媒体和WebSocket服务.
w2g-cli launch --host 0.0.0.0 --port 80 ./
```

如果启动成功, 你将看到如下的提示信息:

```
未启用SSL协议, 服务运行在非加密模式下!
流媒体服务: 成功启动在 http://0.0.0.0:80/video/
WebSocket服务: 成功启动在 ws://0.0.0.0:80/ws/
```

> [!caution]
>
> 该命令仅启动后端服务, 请根据你的需求选择客户端进行访问.
