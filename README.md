# ZJUIntl RSS

这是一个将 Blackboard 的成绩和 Announcement 转换为 RSS (Atom) 订阅的服务端程序。搭配 Feeder 等软件可以实现 Blackboard 成绩和 Announcement 的推送。

## API

- `GET /rss/grades`: 获取成绩
- `GET /rss/announcements`: 获取公告
- `GET /rss/myzjunotices`: 获取 myZJU 通知

## 部署

### Docker

1. 创建一个文件夹，比如 `zjuintl-rss`，并在其中创建一个 `config.yaml` 文件。文件内容如下：
    ```yaml
    username: "your_username"
    password: "your_password"
    ```
2. 在同一文件夹中创建一个 `docker-compose.yml` 文件：
    ```yaml
    services:
      zjuintl-rss:
        image: geniucker/zjuintl-rss:latest
        environment:
          - TZ=Asia/Shanghai
        ports:
          - "5000:5000"
        volumes:
          - ./config.yaml:/app/config.yaml
    ```
3. 在文件夹中运行 `docker-compose up -d`。

### 二进制部署

1. 下载最新的 [release](https://github.com/ZJUIntl-share/ZJUIntl-RSS/releases)。
2. 解压缩文件并在同一文件夹中创建一个 `config.yaml` 文件。文件内容如下：
  ```yaml
  username: "your_username"
  password: "your_password"
  ```
3. 运行二进制文件。

## 说明

- 若使用 Docker 部署，请务必先创建 `config.yaml` 文件，然后再运行 Docker 容器。
- 由于获取 Announcement 需要多次请求，因此 `GET /rss/announcements` 接口可能会比较慢。

## 感谢

- [zjuintl_assistant](https://github.com/ZJUIntl-share/zjuintl_assistant)
