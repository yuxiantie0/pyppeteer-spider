# pyppeteer-spider 管理系统

一个基于 Flask 的 Cookie 池管理系统，支持多站点 Cookie 管理、自动轮换和失效检测。系统包含 Web 界面和 API 接口，可以方便地进行 Cookie 的增删改查操作。

## 功能特点

- 多站点 Cookie 管理
- Cookie 使用次数统计和限制
- 自动轮换算法（优先使用使用次数少的 Cookie）
- 每日使用次数自动重置
- 支持 Cookie 有效性标记
- 集成 pyppeteer 实现网页内容抓取
- Web 界面管理（Bootstrap 5 响应式设计）
- RESTful API 接口
- 完整的日志系统
- 数据库迁移支持
- 多环境配置支持
- Docker 部署支持

## 系统要求

### 本地开发环境
- Python 3.7+
- Chrome/Chromium 浏览器（用于 pyppeteer）

### Docker 环境
- Docker 19.03+
- Docker Compose 1.27+

## 安装和部署

### 方式一：本地开发环境

1. 克隆项目并进入项目目录：
```bash
git clone https://github.com/yuxiantie0/pyppeteer-spider.git
cd pyppeteer-spider
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 初始化数据库：
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. 启动应用：
```bash
# 设置环境（可选，默认为development）
# Windows
set FLASK_ENV=development
# Linux/Mac
export FLASK_ENV=development

python app.py
```

### 方式二：Docker 部署

1. 克隆项目并进入项目目录：
```bash
git clone https://github.com/yuxiantie0/pyppeteer-spider.git
cd pyppeteer-spider
```

2. 使用 Docker Compose 构建和启动：
```bash
# 构建并在前台运行（可以看到日志输出）
docker-compose up --build

# 或者在后台运行
docker-compose up -d
```

3. 查看容器日志：
```bash
docker-compose logs -f
```

4. 停止服务：
```bash
docker-compose down
```

## 项目结构

```
.
├── app.py                 # 主应用文件
├── models.py             # 数据模型
├── tasks.py             # 定时任务
├── requirements.txt     # 项目依赖
├── config/             # 配置目录
│   ├── config.py      # 环境配置
│   └── logging.py     # 日志配置
├── routes/            # 路由目录
│   ├── website.py    # 网站管理路由
│   ├── cookie.py     # Cookie管理路由
│   └── spider.py     # 爬虫相关路由
├── static/           # 静态文件目录
│   ├── css/         # CSS样式文件
│   └── js/          # JavaScript文件
├── migrations/       # 数据库迁移文件
├── utils/           # 工具目录
│   └── spider.py    # 爬虫工具类
├── instance/        # 实例目录
│   ├── logs/        # 日志文件
│   ├── cookie_pool.db
│   └── secret_key
├── Dockerfile       # Docker 构建文件
├── docker-compose.yml # Docker Compose 配置
└── .dockerignore    # Docker 忽略文件
```

## Web 界面

系统提供了现代化的响应式Web界面，主要包括：

- `/websites` - 网站管理列表
- `/website/add` - 添加网站
- `/website/edit/<id>` - 编辑网站
- `/cookies` - Cookie 管理列表
- `/cookie/add` - 添加 Cookie
- `/cookie/edit/<id>` - 编辑 Cookie

## API 接口

### 获取 Cookie

- 接口：`GET /api/getcookie`
- 参数：
  - `site`: 站点标识符（必需）
  - `account`: 账号（可选）
  - `num`: 需要获取的 Cookie 数量（可选，默认1）
- 返回示例：
```json
[
    {
        "domain": ".example.com",
        "name": "sessionid",
        "value": "abc123",
        "expirationDate": 1740898356
    }
]
```

### 标记 Cookie 失效

- 接口：`POST /api/expirecookie`
- 参数：
  - `cookie`: Cookie 值（必需）
- 返回示例：
```json
{
    "status": "success",
    "message": "Cookie expired successfully"
}
```

### 获取网页内容

- 接口：`POST /fetch`
- 参数：
```json
{
    "url": "https://example.com",
    "cookie": [{"name": "sessionid", "value": "abc123", ...}],
    "proxy": "http://proxy:port",  // 可选
    "ua": "user-agent-string"      // 可选
}
```
- 返回示例：
```json
{
    "status": "success",
    "data": {
        "content": "网页内容",
        "cookie": ["更新后的Cookie列表"],
        "ua": "使用的User-Agent"
    }
}
```

## 配置系统

系统支持多环境配置，配置文件位于 `config/config.py`：

### 环境配置

- `development`: 开发环境（默认）
  - DEBUG 模式开启
  - SQLite 数据库
  - 详细日志记录
- `testing`: 测试环境
  - 测试数据库
  - 禁用 CSRF
  - 中等级别日志
- `production`: 生产环境
  - 关闭调试模式
  - 支持自定义数据库 URL
  - 启用安全选项
  - 最小化日志记录

### 日志系统

系统使用分级日志系统（`config/logging.py`）：

- `app.log`: 应用日志，记录一般操作信息
- `error.log`: 错误日志，记录警告和错误
- 日志文件自动轮转（1MB/文件，保留10个备份）
- 不同模块使用不同日志级别

### 主要配置项

- `COOKIE_DAILY_LIMIT`: Cookie 每日使用次数限制（默认 1000）
- `BROWSER_CONFIG`: 浏览器配置
  - `headless`: 是否使用无头模式
  - `window_size`: 窗口大小
  - `disable_infobars`: 是否禁用信息栏

## 数据库迁移

系统使用 Flask-Migrate (Alembic) 进行数据库迁移管理：

```bash
# 创建新的迁移
flask db migrate -m "迁移说明"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade
```

## 定时任务

系统包含以下定时任务：

- 每日凌晨 00:00 自动重置所有 Cookie 的每日使用次数
- 定时任务在应用启动时自动初始化，应用关闭时自动清理

## 开发说明

1. 代码风格遵循 PEP 8
2. 使用 Blueprint 组织路由
3. 使用 SQLAlchemy ORM 操作数据库
4. 完整的异常处理和日志记录
5. 模块化设计，便于扩展
6. 支持数据库迁移
7. 多环境配置支持

## 注意事项

1. 本系统仅用于开发测试环境，生产环境使用需要额外配置
2. 使用前请确保已安装 Chrome/Chromium 浏览器（本地开发环境）
3. 建议定期备份数据库文件
4. 请合理设置 Cookie 使用限制，避免对目标站点造成压力
5. 生产环境部署前请修改 SECRET_KEY
6. 建议启用 HTTPS 以保护 Cookie 数据安全

### Docker 部署注意事项

1. 确保 Docker 和 Docker Compose 已正确安装
2. 首次运行时会自动创建必要的目录和数据库
3. instance 目录已配置为 volume，数据将持久化保存
4. 可以通过修改 docker-compose.yml 自定义端口映射
5. 生产环境部署时建议配置反向代理（如 Nginx）
6. 可以通过环境变量覆盖默认配置

## 开源协议

本项目采用 MIT 开源协议。详细信息请查看 [LICENSE](LICENSE) 文件。

MIT 协议是一个宽松的协议，基本上允许任何人任何用途，包括商业用途。使用本项目代码时，请保留版权信息。 