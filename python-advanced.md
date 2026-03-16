# Python 开发圣经——高级用法篇

> 目标读者：具备其他编程语言经验的开发者  
> Python 版本：3.11+  
> 更新时间：2025

## 目录

1. [文件操作](#1-文件操作)
2. [网络请求](#2-网络请求)
3. [多线程与多进程](#3-多线程与多进程)
4. [数据库操作](#4-数据库操作)
5. [异步编程](#5-异步编程)

---

## 1. 文件操作

### 1.1 文件读写基础

```python
# 读取文件
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()  # 一次性读取全部
    # 或者逐行读取
    # for line in f:
    #     print(line.strip())

# 写入文件
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("第二行内容")

# 追加模式
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("新的日志条目\n")
```

### 1.2 文件路径处理

```python
import os
from pathlib import Path

# Path 对象（推荐方式）
p = Path("example.txt")

# 路径拼接
base = Path("/home/user")
config = base / "config" / "settings.json"

# 路径操作
print(config.exists())  # 检查是否存在
print(config.is_file())  # 是否为文件
print(config.is_dir())  # 是否为目录
print(config.name)  # 文件名
print(config.stem)  # 不带扩展名的文件名
print(config.suffix)  # 扩展名
print(config.parent)  # 父目录
print(config.resolve())  # 绝对路径

# 创建目录
Path("new_dir").mkdir(exist_ok=True)
Path("a/b/c").mkdir(parents=True, exist_ok=True)

# 列出目录内容
for item in Path(".").iterdir():
    print(item.name)

# 递归列出文件
for file in Path(".").rglob("*.py"):
    print(file)
```

### 1.3 上下文管理器

```python
# 自定义上下文管理器
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        # 返回 True 抑制异常
        return False

# 使用
with FileManager("test.txt", "w") as f:
    f.write("Hello")

# 使用 contextlib
from contextlib import contextmanager

@contextmanager
def managed_file(filename, mode):
    f = open(filename, mode, encoding="utf-8")
    try:
        yield f
    finally:
        f.close()

with managed_file("test.txt", "r") as f:
    content = f.read()
```

### 1.4 JSON 处理

```python
import json

# 读取 JSON
with open("config.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 写入 JSON
config = {"host": "localhost", "port": 8080, "debug": True}
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# JSON 字符串
json_str = '{"name": "Alice", "age": 25}'
data = json.loads(json_str)
back_to_str = json.dumps(data)

# 中文处理
data = {"姓名": "张三", "年龄": 30}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
```

### 1.5 CSV 处理

```python
import csv

# 读取 CSV
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)  # 读取表头
    for row in reader:
        print(row)

# 写入 CSV
with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "年龄", "城市"])
    writer.writerows([
        ["张三", 25, "北京"],
        ["李四", 30, "上海"],
    ])

# 使用字典读写
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["姓名"], row["年龄"])
```

### 1.6 二进制文件

```python
# 读取二进制文件
with open("image.png", "rb") as f:
    data = f.read()

# 写入二进制文件
with open("copy.png", "wb") as f:
    f.write(data)

# 使用 struct 处理二进制结构
import struct

# 打包数据
data = struct.pack("I", 100)  # 无符号整数
data = struct.pack("3i", 1, 2, 3)  # 3个整数
data = struct.pack("10s", b"hello")  # 10字节字符串

# 解包数据
value = struct.unpack("I", data)[0]
a, b, c = struct.unpack("3i", data)
```

---

## 2. 网络请求

### 2.1 requests 库

```python
import requests

# GET 请求
response = requests.get("https://api.example.com/data")
print(response.status_code)
print(response.json())  # 解析 JSON
print(response.text)  # 原始文本
print(response.headers)  # 响应头

# 带参数
params = {"page": 1, "limit": 10}
response = requests.get("https://api.example.com/items", params=params)

# POST 请求
data = {"username": "alice", "password": "secret"}
response = requests.post("https://api.example.com/login", json=data)

# 请求头
headers = {"Authorization": "Bearer token123"}
response = requests.get("https://api.example.com/protected", headers=headers)

# 超时设置
response = requests.get("https://api.example.com/data", timeout=10)

# 会话保持
session = requests.Session()
session.headers.update({"User-Agent": "MyApp/1.0"})
response = session.get("https://api.example.com/data")
```

### 2.2 异步 HTTP 请求

```python
import aiohttp
import asyncio

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        # GET 请求
        async with session.get("https://api.example.com/data") as response:
            data = await response.json()
            print(data)
        
        # POST 请求
        async with session.post(
            "https://api.example.com/login",
            json={"username": "alice", "password": "secret"}
        ) as response:
            result = await response.json()
            print(result)

# 多个请求并发
async def fetch_multiple(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await r.json() for r in responses]

# 运行
asyncio.run(fetch_data())
```

### 2.3 WebSocket

```python
import websockets
import asyncio

async def websocket_client():
    uri = "ws://echo.websocket.org"
    async with websockets.connect(uri) as websocket:
        # 发送消息
        await websocket.send("Hello")
        
        # 接收消息
        message = await websocket.recv()
        print(f"Received: {message}")

asyncio.run(websocket_client())

# 服务端
async def echo_server(websocket):
    async for message in websocket:
        await websocket.send(f"Echo: {message}")

async def main():
    async with websockets.serve(echo_server, "localhost", 8765):
        await asyncio.Future()  # 永久运行

asyncio.run(main())
```

### 2.4 FTP 操作

```python
from ftplib import FTP

# 连接 FTP
ftp = FTP("ftp.example.com")
ftp.login("username", "password")

# 列出文件
ftp.retrlines("LIST")

# 下载文件
with open("local.txt", "wb") as f:
    ftp.retrbinary("RETR remote.txt", f.write)

# 上传文件
with open("local.txt", "rb") as f:
    ftp.storbinary("STOR upload.txt", f)

ftp.quit()
```

---

## 3. 多线程与多进程

### 3.1 线程基础

```python
import threading
import time

def worker(n):
    """工作线程函数"""
    print(f"线程 {n} 开始")
    time.sleep(1)
    print(f"线程 {n} 结束")

# 创建线程
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

print("所有线程完成")

# 带返回值的线程
from queue import Queue

def worker_with_result(n, queue):
    result = n * 2
    queue.put(result)

queue = Queue()
threads = []
for i in range(3):
    t = threading.Thread(target=worker_with_result, args=(i, queue))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

while not queue.empty():
    print(queue.get())
```

### 3.2 线程安全与同步

```python
import threading
from threading import Lock, RLock, Semaphore, Condition

# Lock - 互斥锁
lock = Lock()
counter = 0

def increment():
    global counter
    with lock:
        counter += 1

# RLock - 可重入锁（同一线程可多次获取）
rlock = RLock()

# Semaphore - 信号量
semaphore = Semaphore(3)  # 最多3个并发

# Condition - 条件变量
condition = Condition()

def producer(items):
    with condition:
        while len(items) >= 5:
            condition.wait()
        items.append(1)
        condition.notify_all()

def consumer(items):
    with condition:
        while not items:
            condition.wait()
        items.pop()
        condition.notify_all()
```

### 3.3 线程池

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

# 使用线程池
def task(n):
    time.sleep(1)
    return n * n

with ThreadPoolExecutor(max_workers=4) as executor:
    # 提交多个任务
    futures = [executor.submit(task, i) for i in range(10)]
    
    # 等待结果
    for future in as_completed(futures):
        print(f"Result: {future.result()}")

# 使用 map
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(task, range(10))
    print(list(results))
```

### 3.4 进程基础

```python
import multiprocessing
from multiprocessing import Process, Queue, Pipe

def worker(name):
    print(f"进程 {name} 开始工作")
    print(f"进程 {name} 结束工作")

# 创建进程
if __name__ == "__main__":
    processes = []
    for i in range(3):
        p = Process(target=worker, args=(i,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()

    print("所有进程完成")
```

### 3.5 进程间通信

```python
from multiprocessing import Process, Queue, Pipe, Manager

# Queue - 队列通信
def producer(q):
    for i in range(5):
        q.put(i)
    q.put(None)  # 发送结束信号

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"消费: {item}")

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

# Pipe - 管道通信
def sender(conn):
    conn.send("Hello")
    conn.close()

def receiver(conn):
    msg = conn.recv()
    print(f"收到: {msg}")
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p1 = Process(target=sender, args=(child_conn,))
    p2 = Process(target=receiver, args=(parent_conn,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```

### 3.6 进程池

```python
from concurrent.futures import ProcessPoolExecutor
import os

def task(n):
    print(f"进程 {os.getpid()} 处理 {n}")
    return n * n

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        # 提交任务
        future = executor.submit(task, 10)
        print(f"结果: {future.result()}")
        
        # map
        results = executor.map(task, range(10))
        print(list(results))
```

### 3.7 GIL 与性能选择

```python
# CPU 密集型任务使用多进程
# IO 密集型任务使用多线程

# 示例：CPU 密集型
from concurrent.futures import ProcessPoolExecutor
import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

with ProcessPoolExecutor() as executor:
    primes = list(executor.map(is_prime, range(100000)))

# 示例：IO 密集型
import threading
import requests

def fetch_url(url):
    return requests.get(url).status_code

urls = ["https://example.com"] * 10
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_url, urls))
```

---

## 4. 数据库操作

### 4.1 SQLite

```python
import sqlite3

# 连接数据库
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# 创建表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# 插入数据
cursor.execute(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    ("Alice", "alice@example.com", 25)
)
conn.commit()

# 批量插入
users = [
    ("Bob", "bob@example.com", 30),
    ("Charlie", "charlie@example.com", 35),
]
cursor.executemany(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    users
)
conn.commit()

# 查询数据
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 条件查询
cursor.execute("SELECT * FROM users WHERE age > ?", (28,))
for row in cursor.fetchall():
    print(row)

# 更新数据
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (26, "Alice"))
conn.commit()

# 删除数据
cursor.execute("DELETE FROM users WHERE name = ?", ("Bob",))
conn.commit()

# 关闭连接
conn.close()

# 使用上下文管理器
with sqlite3.connect("example.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())
```

### 4.2 MySQL

```python
# 安装: pip install pymysql
import pymysql
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="password",
        database="test",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        yield conn
    finally:
        conn.close()

# 查询
with get_connection() as conn:
    with conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE age > %s"
        cursor.execute(sql, (25,))
        result = cursor.fetchall()
        for row in result:
            print(row)

# 插入
with get_connection() as conn:
    with conn.cursor() as cursor:
        sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
        cursor.execute(sql, ("Alice", "alice@example.com", 25))
    conn.commit()

# 批量操作
with get_connection() as conn:
    with conn.cursor() as cursor:
        sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
        data = [
            ("Bob", "bob@example.com", 30),
            ("Charlie", "charlie@example.com", 35),
        ]
        cursor.executemany(sql, data)
    conn.commit()
```

### 4.3 PostgreSQL

```python
# 安装: pip install psycopg2-binary
import psycopg2
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="password",
        database="test"
    )
    try:
        yield conn
    finally:
        conn.close()

# 使用 psycopg2.extras 实现批量插入
from psycopg2 import extras

with get_connection() as conn:
    with conn.cursor() as cursor:
        # 批量插入
        data = [
            ("Alice", "alice@example.com", 25),
            ("Bob", "bob@example.com", 30),
        ]
        extras.execute_values(
            cursor,
            "INSERT INTO users (name, email, age) VALUES %s",
            data
        )
    conn.commit()
```

### 4.4 SQLAlchemy ORM

```python
# 安装: pip install sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# 创建引擎
engine = create_engine(
    "sqlite:///example.db",
    echo=True  # 打印 SQL 语句
)

# 创建基类
Base = declarative_base()

# 定义模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

# 创建表
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 插入数据
user = User(name="Alice", email="alice@example.com", age=25)
session.add(user)
session.commit()

# 批量插入
users = [
    User(name="Bob", email="bob@example.com", age=30),
    User(name="Charlie", email="charlie@example.com", age=35),
]
session.add_all(users)
session.commit()

# 查询
user = session.query(User).filter_by(name="Alice").first()
print(user)

# 条件查询
users = session.query(User).filter(User.age > 25).all()

# 排序
users = session.query(User).order_by(User.age.desc()).all()

# 分页
users = session.query(User).limit(10).offset(0).all()

# 更新
session.query(User).filter_by(name="Alice").update({"age": 26})
session.commit()

# 删除
session.query(User).filter_by(name="Bob").delete()
session.commit()

# 关闭会话
session.close()
```

### 4.5 Redis 操作

```python
# 安装: pip install redis
import redis
from redis import Redis

# 连接 Redis
r = Redis(
    host="localhost",
    port=6379,
    db=0,
    password=None,
    decode_responses=True  # 自动解码为字符串
)

# 字符串操作
r.set("name", "Alice")
print(r.get("name"))
r.setex("temp_key", 60, "value")  # 设置过期时间
r.incr("counter")  # 原子递增
r.decr("counter")  # 原子递减

# 哈希操作
r.hset("user:1", "name", "Alice")
r.hset("user:1", "age", "25")
print(r.hgetall("user:1"))
print(r.hget("user:1", "name"))
r.hincrby("user:1", "age", 1)  # 原子递增

# 列表操作
r.lpush("queue", "task1")
r.lpush("queue", "task2")
print(r.lrange("queue", 0, -1))
r.rpop("queue")

# 集合操作
r.sadd("tags", "python", "redis", "database")
print(r.smembers("tags"))
print(r.sismember("tags", "python"))

# 有序集合
r.zadd("leaderboard", {"Alice": 100, "Bob": 80, "Charlie": 90})
print(r.zrevrange("leaderboard", 0, 2, withscores=True))

# 键操作
print(r.keys("*"))
print(r.exists("name"))
r.expire("name", 60)  # 设置过期时间
r.delete("name")

# 事务
pipe = r.pipeline()
pipe.set("key1", "value1")
pipe.get("key1")
pipe.incr("counter")
result = pipe.execute()

# 发布订阅
pubsub = r.pubsub()
pubsub.subscribe("channel1")

# 发布消息
r.publish("channel1", "Hello, subscribers!")

# 遍历消息
for message in pubsub.listen():
    if message["type"] == "message":
        print(message["data"])
```

---

## 5. 异步编程

### 5.1 async/await 基础

```python
import asyncio

async def main():
    print("开始")
    await asyncio.sleep(1)  # 模拟 IO 操作
    print("结束")

# 运行协程
asyncio.run(main())

# 多个协程并发运行
async def task(name, delay):
    print(f"{name} 开始")
    await asyncio.sleep(delay)
    print(f"{name} 结束")
    return name

async def main():
    # 并发执行
    results = await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3),
    )
    print(f"结果: {results}")

asyncio.run(main())
```

### 5.2 异步生成器

```python
# 异步生成器
async def async_range(start, stop):
    for i in range(start, stop):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for i in async_range(0, 10):
        print(i)

asyncio.run(main())

# 异步列表推导式
async def main():
    result = [x async for x in async_range(0, 10) if x % 2 == 0]
    print(result)

asyncio.run(main())
```

### 5.3 异步上下文管理器

```python
class AsyncConnection:
    async def __aenter__(self):
        await asyncio.sleep(0.1)  # 模拟连接
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0.1)  # 模拟关闭
    
    async def fetch(self, query):
        await asyncio.sleep(0.1)
        return f"Result: {query}"

async def main():
    async with AsyncConnection() as conn:
        result = await conn.fetch("SELECT * FROM users")
        print(result)

asyncio.run(main())

# 使用 contextlib
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_connection():
    conn = AsyncConnection()
    await conn.__aenter__()
    try:
        yield conn
    finally:
        await conn.__aexit__(None, None, None)
```

### 5.4 异步文件操作

```python
import aiofiles

# 异步写入
async def write_file():
    async with aiofiles.open("test.txt", "w") as f:
        await f.write("Hello, async!")

# 异步读取
async def read_file():
    async with aiofiles.open("test.txt", "r") as f:
        content = await f.read()
        print(content)

asyncio.run(write_file())
asyncio.run(read_file())
```

### 5.5 异步数据库操作

```python
# 安装: pip install aiomysql aiosqlite
import asyncio
import aiosqlite

async def main():
    async with aiosqlite.connect("test.db") as db:
        # 创建表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """)
        await db.commit()
        
        # 插入
        await db.execute(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            ("Alice", 25)
        )
        await db.commit()
        
        # 查询
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                print(row)

asyncio.run(main())

# aiomysql 示例
import aiomysql

async def main():
    pool = await aiomysql.create_pool(
        host="localhost",
        user="root",
        password="password",
        db="test"
    )
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM users")
            rows = await cursor.fetchall()
            print(rows)
    
    pool.close()
    await pool.wait_closed()

asyncio.run(main())
```

### 5.6 asyncio 并发控制

```python
import asyncio
from asyncio import Semaphore

# 信号量控制并发数
semaphore = Semaphore(3)

async def limited_task(n):
    async with semaphore:
        print(f"任务 {n} 开始")
        await asyncio.sleep(1)
        print(f"任务 {n} 结束")

async def main():
    tasks = [limited_task(i) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())

# 限流器
from asyncio import RateLimiter

async def limited_request(url):
    async with rate_limiter:
        # 模拟请求
        await asyncio.sleep(0.1)
        print(f"请求: {url}")

rate_limiter = RateLimiter(1, period=1)  # 每秒1次
```

---

## 6. 实战示例

### 6.1 批量下载文件

```python
import aiohttp
import asyncio
import aiofiles
from pathlib import Path

async def download_file(session, url, filepath):
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.read()
            async with aiofiles.open(filepath, "wb") as f:
                await f.write(content)
            print(f"下载完成: {filepath}")

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_file(session, url, f"downloads/{url.split('/')[-1]}")
            for url in urls
        ]
        await asyncio.gather(*tasks)

# 创建下载目录
Path("downloads").mkdir(exist_ok=True)

urls = [
    "https://example.com/file1.txt",
    "https://example.com/file2.txt",
]

asyncio.run(main(urls))
```

### 6.2 带缓存的异步爬虫

```python
import asyncio
import aiohttp
from functools import lru_cache
import json

class AsyncCrawler:
    def __init__(self):
        self.session = None
        self.cache = {}
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def fetch(self, url):
        # 检查缓存
        if url in self.cache:
            print(f"从缓存读取: {url}")
            return self.cache[url]
        
        async with self.session.get(url) as response:
            data = await response.text()
            self.cache[url] = data
            return data

async def main():
    urls = ["https://example.com"] * 5
    
    async with AsyncCrawler() as crawler:
        results = await asyncio.gather(*[crawler.fetch(url) for url in urls])
        print(f"获取 {len(results)} 个结果")

asyncio.run(main())
```

---

## 下一步学习

完成本篇学习后，建议继续学习：

1. **Python 工程化** - 包管理、模块化、测试、CI/CD
2. **Python 服务端框架** - Flask、Django、FastAPI
3. **Python 最佳实践** - 代码规范、性能优化、安全

---

*持续更新中……*