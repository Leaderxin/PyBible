# Python 开发圣经

> 目标读者：具备其他编程语言经验的开发者  
> Python 版本：3.11+

本系列文档旨在帮助开发者快速入门并成为一个中高级 Python 开发者，适应市场主流 Python 开发工作。

## 文档目录

### 📚 基础入门

| 文档 | 描述 | 适合阶段 |
|------|------|----------|
| [Python 基础入门篇](python-basics.md) | 语法、数据类型、控制流、函数、错误处理 | 入门 |
| [函数式编程与面向对象篇](python-oop-fp.md) | 函数式编程、OOP 高级特性、设计模式 | 入门~进阶 |

### 🚀 高级进阶

| 文档 | 描述 | 适合阶段 |
|------|------|----------|
| [Python 高级用法篇](python-advanced.md) | 文件 IO、网络请求、多线程、数据库、异步编程 | 进阶 |
| [Python 工程化进阶篇](python-engineering.md) | 包管理、模块化、测试、日志、中间件、CI/CD | 进阶 |

### 🌐 框架实战

| 文档 | 描述 | 适合阶段 |
|------|------|----------|
| [Python 服务端框架篇](python-frameworks.md) | Flask、Django、FastAPI 详解 | 进阶~实战 |

### ✨ 最佳实践

| 文档 | 描述 | 适合阶段 |
|------|------|----------|
| [Python 最佳实践与资源篇](python-best-practices.md) | 代码规范、性能优化、安全、调试、资源汇总 | 实战 |

---

## 学习路径建议

```
阶段一：基础入门（1-2个月）
├── python-basics.md (2周)
│   ├── Python 简介与开发环境
│   ├── 基础语法
│   ├── 数据类型
│   ├── 控制流
│   └── 函数与错误处理
│
└── python-oop-fp.md (2周)
    ├── 函数式编程
    ├── 面向对象基础
    ├── 面向对象高级特性
    └── 设计模式

阶段二：高级进阶（2-3个月）
├── python-advanced.md (2周)
│   ├── 文件操作
│   ├── 网络请求
│   ├── 多线程与多进程
│   ├── 数据库操作
│   └── 异步编程
│
└── python-engineering.md (2周)
    ├── 包管理
    ├── 模块化管理
    ├── 测试
    ├── 日志与监控
    ├── 配置管理
    └── 常用中间件

阶段三：框架实战（3-6个月）
└── python-frameworks.md (4周)
    ├── Flask 轻量级框架
    ├── Django 全栈框架
    ├── FastAPI 现代高性能框架
    ├── RESTful API 设计
    ├── 认证与授权
    └── 部署与运维

阶段四：最佳实践（持续）
└── python-best-practices.md (持续学习)
    ├── 代码规范
    ├── 性能优化
    ├── 安全最佳实践
    ├── 调试技巧
    ├── 常用库推荐
    ├── 学习资源
    └── 职业发展建议
```

---

## 快速开始

### 环境配置

```bash
# 使用 conda (推荐)
conda create -n myproject python=3.11
conda activate myproject
```

### 第一个程序

```python
# hello.py
def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("Python Developer"))
```

运行：

```bash
python hello.py
# Output: Hello, Python Developer!
```

---

## 核心概念速查

### 数据类型

| 类型 | 示例 | 描述 |
|------|------|------|
| `int` | `42` | 整数 |
| `float` | `3.14` | 浮点数 |
| `str` | `"hello"` | 字符串 |
| `bool` | `True/False` | 布尔值 |
| `list` | `[1, 2, 3]` | 列表 |
| `tuple` | `(1, 2, 3)` | 元组 |
| `dict` | `{"a": 1}` | 字典 |
| `set` | `{1, 2, 3}` | 集合 |

### 常用语法糖

```python
# 列表推导式
squares = [x**2 for x in range(10)]

# 字典推导式
d = {k: v for k, v in items}

# 生成器
gen = (x**2 for x in range(10))

# 解包
a, b, *rest = [1, 2, 3, 4, 5]

# f-string
name = "Alice"
print(f"Hello, {name}!")

# 合并字典 (Python 3.9+)
d1 | d2

# match-case (Python 3.10+)
match value:
    case 1:
        print("one")
    case _:
        print("other")
```

---

## 常用命令

### pip/conda

```bash
# pip
pip install package
pip install package==1.0.0
pip install -r requirements.txt
pip freeze > requirements.txt

# conda
conda install package
conda create -n myenv python=3.11
conda activate myenv
conda env export > environment.yml
```

### 测试

```bash
pytest
pytest tests/
pytest --cov=src
```

### 代码检查

```bash
ruff check src/
ruff format src/
mypy src/
black src/
```

---

## 贡献指南

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

---

## 许可证

MIT License

---

*持续更新中……如有错误欢迎指正！*