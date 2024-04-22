# Blackboard RSS

This is a web server that scrapes Blackboard for grades and announcements and provides an RSS feed for them.

## API

- `GET /rss/grades`: Get the grades in Atom format.
- `GET /rss/announcements`: Get the announcements in Atom format.

## Usage

### Docker

1. Create a folder lets say `blackboard-rss` and create a `config.yaml` file in it. The file should look like this:  
    ```yaml
    username: "your_username"
    password: "your_password"
    ```
2. Create a `docker-compose.yml` file in the same folder:  
    ```yaml
    services:
      bb-rss:
        image: geniucker/blackboard-rss:latest
        environment:
          - TZ=Asia/Shanghai
        ports:
          - "5000:5000"
        volumes:
          - ./config.yaml:/app/config.yaml
    ```
3. Run `docker-compose up -d` in the folder.

### Binary

1. Download the latest release from the [releases page](https://github.com/ZJUIntl-share/blackboard-rss/releases).
2. Unzip the archive and create a `config.yaml` file in the same folder. The file should look like this:  
  ```yaml
  username: "your_username"
  password: "your_password"
  ```
3. Run the binary.

## Credits

- [zjuintl_assistant](https://github.com/ZJUIntl-share/zjuintl_assistant)
