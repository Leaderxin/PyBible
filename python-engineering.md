# Python 开发圣经——工程化进阶篇

> 目标读者：具备其他编程语言经验的开发者  
> Python 版本：3.11+  
> 更新时间：2025

## 目录

1. [包管理](#1-包管理)
2. [模块化管理与项目结构](#2-模块化管理与项目结构)
3. [虚拟环境](#3-虚拟环境)
4. [测试](#4-测试)
5. [日志与监控](#5-日志与监控)
6. [配置管理](#6-配置管理)
7. [常用中间件](#7-常用中间件)

---

## 1. 包管理

### 1.1 pip 基础

```bash
# 基础命令
pip install package_name          # 安装包
pip install package==1.0.0       # 安装指定版本
pip install package>=1.0.0         # 安装最小版本
pip uninstall package             # 卸载
pip list                          # 列出已安装包
pip show package                  # 显示包信息
pip freeze                        # 导出依赖列表
pip freeze > requirements.txt      # 保存依赖

# 常用选项
pip install -r requirements.txt   # 从文件安装
pip install -U package            # 升级包
pip install --upgrade pip         # 升级 pip
```

### 1.2 conda（推荐）

```bash
# 创建环境
conda create -n myproject python=3.11

# 激活环境
conda activate myproject

# 安装依赖
conda install requests flask sqlalchemy
# 或使用 pip
pip install requests flask sqlalchemy

# 安装开发依赖
conda install pytest black
# 或使用 pip
pip install pytest black

# 导出环境
conda env export > environment.yml

# 从文件创建环境
conda env create -f environment.yml

# 运行脚本
python script.py

# 导出 requirements.txt
pip freeze > requirements.txt
```

### 1.3 poetry

```bash
# 安装 poetry
pip install poetry

# 初始化项目
poetry new myproject
cd myproject

# 添加依赖
poetry add requests
poetry add pytest --group dev

# 安装依赖
poetry install

# 导出 requirements
poetry export -f requirements.txt --output requirements.txt
```

### 1.4 requirements.txt 规范

```text
# 固定版本（推荐用于生产）
requests==2.31.0
flask==3.0.0
sqlalchemy==2.0.23

# 最小版本要求
django>=4.2,<5.0
redis>=4.5.0

# 使用环境标记
pyyaml>=6.0  # 所有环境
pytest>=7.0  # 仅开发环境

# 使用 Extras
celery[redis]>=5.0
httpx[http2]>=0.24
```

### 1.5 pyproject.toml（现代标准）

```toml
[project]
name = "myproject"
version = "1.0.0"
description = "My Awesome Project"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
dependencies = [
    "flask>=3.0.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "ruff>=0.1.0",
]
redis = ["redis>=4.5.0"]

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

---

## 2. 模块化管理与项目结构

### 2.1 模块结构

```
myproject/
├── src/
│   └── myproject/          # 主包
│       ├── __init__.py
│       ├── core/            # 核心模块
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── database.py
│       ├── models/          # 数据模型
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/        # 业务逻辑
│       │   ├── __init__.py
│       │   └── user_service.py
│       ├── api/             # API 接口
│       │   ├── __init__.py
│       │   └── routes.py
│       └── utils/           # 工具函数
│           ├── __init__.py
│           └── helpers.py
├── tests/                   # 测试
│   ├── __init__.py
│   ├── test_user.py
│   └── test_api.py
├── pyproject.toml
├── README.md
└── .gitignore
```

### 2.2 __init__.py 规范

```python
# src/myproject/__init__.py
"""
MyProject - A Python project template
"""

__version__ = "1.0.0"

# 导出主要接口
from myproject.core.config import Settings
from myproject.models.user import User

__all__ = ["Settings", "User", "__version__"]
```

### 2.3 相对导入与绝对导入

```python
# 绝对导入（推荐）
from myproject.core.config import Settings
from myproject.services.user_service import UserService

# 相对导入（包内使用）
# 在 myproject/services/user_service.py 中
from ..core.config import Settings
from ..models.user import User
```

### 2.4 包安装模式

```bash
# 开发模式安装（推荐）
pip install -e .

# 构建分发包
pip build
pip install dist/myproject-1.0.0-py3-none-any.whl
```

---

## 3. 虚拟环境（使用 conda）

```bash
# 创建环境
conda create -n myenv python=3.11

# 激活环境
conda activate myenv

# 列出环境
conda env list

# 删除环境
conda env remove -n myenv
```

---

## 4. 测试

### 4.1 pytest 基础

```python
# tests/test_example.py
import pytest

def test_basic():
    assert 1 + 1 == 2

def test_list():
    numbers = [1, 2, 3]
    assert len(numbers) == 3
    assert 1 in numbers

def test_dict():
    data = {"name": "Alice", "age": 25}
    assert data["name"] == "Alice"
    assert "age" in data

# 使用 pytest.fixture
@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 25}

def test_with_fixture(sample_data):
    assert sample_data["name"] == "Alice"

# 参数化测试
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### 4.2 pytest 配置

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",           # 详细输出
    "--strict-markers",  # 严格标记
    "--tb=short",   # 简短的回溯
    "--disable-warnings",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### 4.3 mock 与 patch

```python
# tests/test_mock.py
from unittest.mock import Mock, patch, MagicMock
import pytest

def test_mock():
    mock = Mock()
    mock.method.return_value = "result"
    
    assert mock.method() == "result"
    mock.method.assert_called_once()

def test_patch():
    with patch("module.ClassName") as mock_class:
        mock_class.return_value.method.return_value = "mocked"
        # 测试代码
        pass

# patch 对象属性
class TestExample:
    @patch("os.path.exists", return_value=True)
    def test_file_exists(self, mock_exists):
        import os
        assert os.path.exists("fake.txt")

# AsyncMock
import asyncio
from unittest.mock import AsyncMock

async def test_async():
    mock = AsyncMock()
    mock.coroutine.return_value = "result"
    result = await mock()
    assert result == "result"
```

### 4.4 测试覆盖率

```bash
# 安装 coverage
pip install coverage

# 运行测试并生成报告
coverage run -m pytest
coverage report
coverage html  # 生成 HTML 报告
coverage xml   # 生成 XML 报告
```

---

## 5. 日志与监控

### 5.1 logging 模块

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")

# 高级配置
def setup_logging():
    # 创建 logger
    logger = logging.getLogger("myapp")
    logger.setLevel(logging.DEBUG)
    
    # 文件处理器
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_format)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
```

### 5.2 结构化日志

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

# 使用
handler = logging.FileHandler("app.json")
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("json_logger")
logger.addHandler(handler)
logger.info("Application started")
```

### 5.3 日志轮转

```python
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# 按大小轮转
handler = RotatingFileHandler(
    "app.log",
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5  # 保留5个备份
)

# 按时间轮转
handler = TimedRotatingFileHandler(
    "app.log",
    when="midnight",  # 每天
    interval=1,
    backupCount=30  # 保留30天
)
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(message)s")
)
```

---

## 6. 配置管理

### 6.1 环境变量

```python
import os
from pathlib import Path

# 读取环境变量
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")

# 读取 .env 文件
# 安装: pip install python-dotenv
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()  # 加载 .env
load_dotenv(".env.production")  # 指定文件

# 使用
API_KEY = os.getenv("API_KEY")
```

### 6.2 Pydantic 配置

```python
# config.py
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    APP_NAME: str = "MyApp"
    DEBUG: bool = False
    SECRET_KEY: str = Field(default="dev-secret-key")
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///app.db"
    DB_POOL_SIZE: int = 10
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API 配置
    API_KEY: Optional[str] = None
    API_RATE_LIMIT: int = 100
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True  # 大小写敏感

# 使用
settings = Settings()
print(settings.DATABASE_URL)
```

### 6.3 YAML 配置

```yaml
# config.yaml
app:
  name: MyApp
  debug: true
  secret_key: "your-secret-key"

database:
  host: localhost
  port: 5432
  name: myapp_db
  user: postgres
  password: password

redis:
  host: localhost
  port: 6379
  db: 0

logging:
  level: INFO
  file: app.log
```

```python
# 读取 YAML
import yaml
from pathlib import Path

def load_config():
    config_path = Path("config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()
print(config["app"]["name"])
```

---

## 7. 常用中间件

### 7.1 Redis 缓存

```python
# 安装: pip install redis
import redis
import json
from functools import wraps

# 连接
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# 简单缓存装饰器
def cache(ttl=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 尝试获取缓存
            cached = r.get(key)
            if cached:
                return json.loads(cached)
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 存入缓存
            r.setex(key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache(ttl=60)
def get_user(user_id):
    # 模拟数据库查询
    return {"id": user_id, "name": f"User {user_id}"}
```

### 7.2 Redis 分布式锁

```python
import redis
import time
import uuid

class Lock:
    def __init__(self, name, timeout=10):
        self.name = f"lock:{name}"
        self.timeout = timeout
        self.token = str(uuid.uuid4())
        self.redis = redis.Redis(decode_responses=True)
    
    def acquire(self, wait=True, retry_interval=0.1):
        while True:
            if self.redis.set(self.name, self.token, nx=True, ex=self.timeout):
                return True
            if not wait:
                return False
            time.sleep(retry_interval)
    
    def release(self):
        if self.redis.get(self.name) == self.token:
            self.redis.delete(self.name)
            return True
        return False
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, *args):
        self.release()

# 使用
with Lock("resource"):
    # 临界区代码
    pass
```

### 7.3 Celery 任务队列

```python
# 安装: pip install celery redis
from celery import Celery
from celery.schedules import crontab

# 创建应用
app = Celery(
    "myapp",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# 配置
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_routes={
        "tasks.email.*": {"queue": "email"},
        "tasks.report.*": {"queue": "report"},
    },
    beat_schedule={
        "daily-report": {
            "task": "tasks.report.daily",
            "schedule": crontab(hour=9, minute=0),
        },
    },
)

# 定义任务
@app.task
def send_email(to, subject, body):
    # 发送邮件逻辑
    print(f"发送邮件到 {to}")
    return {"status": "sent", "to": to}

@app.task
def process_data(data):
    # 处理数据
    result = data * 2
    return result

# 定时任务
@app.task
def daily_report():
    # 生成每日报告
    pass

# 运行 worker
# celery -A tasks worker --loglevel=info

# 运行 beat
# celery -A tasks beat --loglevel=info
```

### 7.4 RabbitMQ 消息队列

```python
# 安装: pip install pika
import pika
import json

# 连接
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672)
)
channel = connection.channel()

# 声明队列
channel.queue_declare(queue="task_queue", durable=True)

# 生产者
def publish_message(message):
    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # 持久化
        )
    )

# 消费者
def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"收到消息: {message}")
    # 处理消息
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

print("等待消息...")
channel.start_consuming()
```

---

## 8. CI/CD

### 8.1 GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install uv
        uses: astral-sh/setup-uv@v4
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest
      
      - name: Run linter
        run: ruff check src/
      
      - name: Build
        run: pip build
```

### 8.2 GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.11-slim
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest
    - ruff check src/

build:
  stage: build
  image: python:3.11-slim
  script:
    - pip install build
    - python -m build
  artifacts:
    paths:
      - dist/
```

---

## 9. 性能优化

### 9.1 性能分析

```python
# cProfile
import cProfile
import pstats
import io

def profile_function(func, *args, **kwargs):
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = func(*args, **kwargs)
    
    profiler.disable()
    
    # 输出统计
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    ps.print_stats(20)
    print(s.getvalue())
    
    return result

# 使用
profile_function(my_function)

# 使用装饰器
def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return profile_function(func, *args, **kwargs)
    return wrapper
```

### 9.2 常用优化技巧

```python
# 1. 使用局部变量
def example():
    local_list = []  # 比全局变量快
    for i in range(1000):
        local_list.append(i)
    return local_list

# 2. 使用生成器代替列表
def gen():
    for i in range(1000):
        yield i

# 3. 使用集合进行成员检查
# 列表 O(n)，集合 O(1)
allowed = {"a", "b", "c"}
if "a" in allowed:  # 快速

# 4. 使用 map/filter 代替列表推导（在某些情况下）
result = list(map(str, range(1000)))  # 更快

# 5. 避免频繁字符串拼接
# 不好
s = ""
for i in range(1000):
    s += str(i)

# 好
parts = []
for i in range(1000):
    parts.append(str(i))
s = "".join(parts)

# 6. 使用 __slots__ 减少内存
class Point:
    __slots__ = ["x", "y"]
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

---

## 10. 实战示例

### 10.1 完整项目配置

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── models/
│       ├── services/
│       └── api/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
├── docs/
├── scripts/
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

```toml
# pyproject.toml
[project]
name = "myproject"
version = "0.1.0"
description = "My Awesome Project"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn>=0.27.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.5.0",
    "redis>=5.0.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.1.0",
    "black>=23.0.0",
    "mypy>=1.8.0",
]

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

---

## 下一步学习

完成本篇学习后，建议继续学习：

1. **Python 服务端框架** - Flask、Django、FastAPI
2. **Python 最佳实践** - 代码规范、性能优化、安全

---

*持续更新中……*