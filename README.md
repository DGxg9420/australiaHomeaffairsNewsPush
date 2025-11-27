# australiaHomeaffairsNewsPush

澳大利亚移民局官方消息采集推送工具

## 项目简介

本项目旨在自动抓取澳大利亚内政部移民局官网的最新新闻，并将其翻译成中文。通过定时执行，可以及时获取重要的移民政策更新、系统维护通知等信息。

## 功能特点

- 自动抓取澳大利亚移民局最新新闻
- 利用有道翻译 API 实现中英文翻译
- 智能识别新闻更新，避免重复推送
- 支持 HTML 内容解析与处理

## 安装依赖

```bash
pip install -r requirements.txt
```

或者使用 uv:

```bash
uv sync
```

## 配置说明

在 `config.toml` 文件中配置你的有道翻译 API 密钥：

```toml
# 有道文本翻译API Key
APP_KEY = 'your_app_key'
APP_SECRET = 'your_app_secret'
```

## 使用方法

运行主程序：

```bash
python main.py
```

程序会自动检查是否有新的新闻发布，如果有，则会获取并翻译标题和内容。

## 项目结构

```
.
├── utils/
│   ├── getNews.py       # 新闻抓取模块
│   ├── translator.py     # 翻译模块
│   ├── xmlParser.py      # HTML 解析模块
│   ├── AuthV3Util.py     # 有道 API 认证工具
│   ├── AuthV4Util.py     # 有道 API 认证工具 v4 版本
│   └── WebSocketUtil.py  # WebSocket 工具
├── main.py              # 主程序入口
├── config.toml          # 配置文件
└── pyproject.toml       # 项目依赖配置
```

## 依赖项

- Python >= 3.11
- beautifulsoup4 >= 4.14.2
- requests >= 2.32.5
- websocket >= 0.2.1

## 工作原理

1. `getNews.py` 从澳大利亚移民局网站获取最新的新闻列表
2. 检查是否为新发布的新闻（通过计算新闻内容的哈希值）
3. 如果是新新闻，则调用 `translator.py` 使用有道翻译 API 进行翻译
4. `xmlParser.py` 处理新闻正文中的 HTML 内容并翻译其中的文本

## 注意事项

- 请确保配置正确的有道翻译 API 密钥
- 程序会在本地保存上一次获取的新闻 ID，以避免重复推送
- 建议设置合理的执行频率，避免对目标网站造成过大压力