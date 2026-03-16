# Python 开发圣经 - 基础入门篇

> 目标读者：具备其他编程语言经验的开发者  
> Python 版本：3.11+  
> 更新时间：2025

## 目录

1. [Python 简介与开发环境](#1-python-简介与开发环境)
2. [基础语法](#2-基础语法)
3. [数据类型](#3-数据类型)
4. [控制流](#4-控制流)
5. [函数](#5-函数)
6. [错误处理](#6-错误处理)

---

## 1. Python 简介与开发环境

### 1.1 Python 哲学

Python 遵循 "Zen of Python" 哲学，通过以下命令查看：

```python
import this
```

核心原则：
- **简洁优于复杂**：Python 语法简洁明了
- **显式优于隐式**：清晰表达意图
- **组合优于继承**：优先使用函数组合
- **TIOBE 排名**：长期位居前三

### 1.2 开发环境配置

#### 使用 conda（推荐）

```bash
# 安装 Anaconda 或 Miniconda
# 下载地址：https://www.anaconda.com/download

# 创建环境
conda create -n myproject python=3.11

# 激活环境
conda activate myproject

# 安装依赖
conda install requests flask
# 或使用 pip
pip install requests flask

# 导出环境
conda env export > environment.yml

# 从文件创建环境
conda env create -f environment.yml
```

### 1.3 IDE 配置

推荐使用 **VS Code** 或 **PyCharm**：

#### VS Code 配置 (`.vscode/settings.json`)

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.conda/envs/myproject/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

#### 必装插件

- **Pylance**：类型检查和智能提示
- **Black**：代码格式化
- **Ruff**：快速 linter（比 pylint 快 10-100 倍）
- **Python Test Explorer**：单元测试

---

## 2. 基础语法

### 2.1 注释

```python
# 单行注释

"""
多行字符串
常用于文档字符串
"""

def foo():
    """
    函数的文档字符串
    可以使用 reStructuredText 格式
    """
    pass
```

### 2.2 变量与常量

Python 是动态类型语言，变量无需声明类型：

```python
# 变量声明
name = "Alice"          # 字符串
age = 25                # 整数
height = 1.75           # 浮点数
is_student = True       # 布尔值

# 常量约定（全大写）
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# 多变量赋值
x, y, z = 1, 2, 3
a = b = c = 0          # 链式赋值
```

### 2.3 标识符命名规则

- 区分大小写：`name` 和 `Name` 是不同变量
- 允许字母、数字、下划线，但不能以数字开头
- 不能使用 Python 关键字
- 建议使用 **snake_case**（小写加下划线）

```python
# 常用命名约定
user_name = "alice"           # 变量/函数
class UserProfile:            # 类名用 PascalCase
MAX_RETRY_COUNT = 3           # 常量全大写
_private_method(self):        # 单下划线前缀：内部使用
__init__(self):               # 双下划线前缀：名称重整
__all__ = ["func1", "func2"]  # 导出列表
```

### 2.4 运算符

#### 算术运算符

```python
# 基本运算
a, b = 10, 3
print(a + b)   # 13  - 加法
print(a - b)   # 7   - 减法
print(a * b)   # 30  - 乘法
print(a / b)   # 3.333... - 浮点除法
print(a // b)  # 3   - 整数除法（向下取整）
print(a % b)   # 1   - 取余
print(a ** b)  # 1000 - 幂运算
print(-a)      # -10 - 负数
```

#### 比较运算符

```python
# 返回布尔值
print(10 > 3)    # True
print(10 == 3)   # False
print(10 != 3)   # True
print(10 <= 3)   # False

# 链式比较（Python 特有）
x = 5
print(1 < x < 10)    # True（等价于 1 < x and x < 10）
print(1 < x < 3)     # False
```

#### 逻辑运算符

```python
# and/or/not（短路求值）
print(True and False)   # False
print(True or False)    # True
print(not True)         # False

# 短路行为
result = compute_expensive() and fallback()  # 前面为 False 则不执行后面
```

> ⚠️ 注意：Python 使用 `and/or/not`，不是 `&&/||/!`

#### 位运算符

```python
# 按位操作
print(5 & 3)    # 1  (0101 & 0011 = 0001)
print(5 | 3)    # 7  (0101 | 0011 = 0111)
print(5 ^ 3)    # 6  (0101 ^ 0011 = 0110)
print(~5)       # -6 (按位取反)
print(5 << 2)   # 20 (左移 2 位)
print(5 >> 2)   # 1  (右移 2 位)
```

#### 身份运算符与成员运算符

```python
# 身份运算符：检查是否为同一对象
a = [1, 2, 3]
b = a
c = [1, 2, 3]
print(a is b)      # True - 同一对象
print(a is c)      # False - 不同对象（值相同）
print(a is not c)  # True

# 成员运算符
print(1 in [1, 2, 3])      # True
print(1 not in [1, 2, 3])  # False
print("key" in {"key": 1}) # True（检查键）
```

### 2.5 缩进与代码块

Python 使用 **缩进** 定义代码块，而非花括号：

```python
# 正确示例
if age >= 18:
    print("成年人")
    if age >= 65:
        print("老年人")
else:
    print("未成年人")

# 常见错误：缩进不一致
if True:
    print("A")
  print("B")  # ❌ 缩进不一致
```

> 💡 建议：使用 4 个空格缩进，配置编辑器自动转换 Tab 为空格

---

## 3. 数据类型

### 3.1 数值类型

```python
# 整数（int）- 任意精度
n = 10_000_000    # Python 3.6+ 支持下划线分隔符
print(10**100)    # 可以处理任意大的整数

# 浮点数（float）
pi = 3.14159
print(f"π ≈ {pi:.2f}")   # 格式化输出：3.14

# 复数（complex）
z = 3 + 4j
print(z.real)  # 3.0
print(z.imag)  # 4.0

# 类型转换
int(3.7)    # 3（截断）
float(3)    # 3.0
complex(3)  # (3+0j)
```

### 3.2 字符串（str）

```python
# 创建字符串
s1 = '单引号'
s2 = "双引号"
s3 = '''多行字符串'''
s4 = "Hello " "World"  # 相邻字符串自动拼接

# 原始字符串（r-string）
path = r"C:\Users\Name\n"  # 不转义
print(path)  # C:\Users\Name\n

# f-string（格式化字符串）- Python 3.6+
name = "Alice"
age = 25
print(f"{name} is {age} years old")
print(f"Age in 10 years: {age + 10}")
print(f"Pi: {3.14159:.2f}")  # 格式化

# 常用方法
s = "Hello, World!"
print(s.lower())           # hello, world!
print(s.upper())           # HELLO, WORLD!
print(s.split(","))        # ['Hello', ' World!']
print(s.replace("World", "Python"))  # Hello, Python!
print(s.strip())           # 去除首尾空白
print(s.startswith("Hello"))  # True
print(s.endswith("!"))        # True

# 字符串索引与切片
s = "Python"
print(s[0])      # P（正向索引）
print(s[-1])      # n（负数索引）
print(s[0:3])     # Pyt（[start:end)，不含 end）
print(s[::2])     # Pto（步长为 2）
print(s[::-1])    # nohtyP（反转）
```

### 3.3 列表（list）

```python
# 创建列表
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# 列表操作
fruits.append("orange")      # 末尾添加
fruits.insert(1, "mango")    # 指定位置插入
fruits.remove("banana")      # 移除第一个匹配项
popped = fruits.pop()        # 弹出并返回最后一个元素
fruits.clear()               # 清空列表

# 列表推导式
squares = [x**2 for x in range(10)]
even_numbers = [x for x in range(20) if x % 2 == 0]

# 切片操作
numbers = [0, 1, 2, 3, 4, 5]
print(numbers[1:4])    # [1, 2, 3]
print(numbers[::2])    # [0, 2, 4]
print(numbers[::-1])   # [5, 4, 3, 2, 1, 0]
```

### 3.4 元组（tuple）

```python
# 创建元组（不可变）
point = (10, 20)
single = (42,)        # 注意：单元素元组需要逗号
empty = ()

# 元组解包
x, y = point         # x=10, y=20
a, *b, c = [1, 2, 3, 4, 5]  # a=1, b=[2,3,4], c=5

# 命名元组（更易读）
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
print(p.x, p.y)      # 10 20
```

> 💡 元组相比列表的优势：性能更好、可用作字典键、表示固定数据结构

### 3.5 字典（dict）

```python
# 创建字典
person = {
    "name": "Alice",
    "age": 25,
    "city": "Beijing"
}

# 访问与修改
print(person["name"])        # Alice
print(person.get("gender", "Unknown"))  # Unknown（默认值）
person["age"] = 26           # 修改
person["email"] = "a@b.com"  # 添加新键

# 常用方法
print(person.keys())         # dict_keys(['name', 'age', 'city'])
print(person.values())       # dict_values(['Alice', 26, 'Beijing'])
print(person.items())       # dict_items([('name','Alice'), ...])

# 字典推导式
squares = {x: x**2 for x in range(5)}

# 合并字典（Python 3.9+）
d1 = {"a": 1}
d2 = {"b": 2}
merged = d1 | d2              # {"a": 1, "b": 2}
d1 |= d2                     # 就地合并
```

### 3.6 集合（set）

```python
# 创建集合
fruits = {"apple", "banana", "cherry"}
numbers = set([1, 2, 3, 2, 1])  # {1, 2, 3} - 自动去重

# 集合操作
fruits.add("orange")
fruits.remove("banana")
fruits.discard("mango")    # 移除（不存在不报错）

# 集合运算
a = {1, 2, 3}
b = {2, 3, 4}
print(a | b)    # {1, 2, 3, 4} - 并集
print(a & b)    # {2, 3} - 交集
print(a - b)    # {1} - 差集
print(a ^ b)    # {1, 4} - 对称差集

# 集合推导式
squares = {x**2 for x in range(5)}
```

### 3.7 数据类型转换

```python
# 常见类型转换
str(123)       # "123"
int("123")     # 123
float("3.14")  # 3.14
list("abc")    # ['a', 'b', 'c']
set([1, 2, 2]) # {1, 2}
tuple([1,2])   # (1, 2)

# 进制转换
bin(10)        # '0b1010'
oct(10)        # '0o12'
hex(10)        # '0xa'
int("1010", 2) # 10（二进制转十进制）
```

---

## 4. 控制流

### 4.1 条件语句

```python
# if-elif-else
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"

# 简写形式（三元运算符）
status = "成年" if age >= 18 else "未成年"

# 多个条件
if age >= 18 and is_student:
    print("学生票")
```

### 4.2 循环

#### for 循环

```python
# 遍历范围
for i in range(5):           # 0, 1, 2, 3, 4
for i in range(1, 6):        # 1, 2, 3, 4, 5
for i in range(0, 10, 2):   # 0, 2, 4, 6, 8

# 遍历列表
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# 遍历字典
person = {"name": "Alice", "age": 25}
for key in person:
    print(f"{key}: {person[key]}")
for key, value in person.items():
    print(f"{key}: {value}")

# enumerate - 获取索引
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# zip - 并行遍历
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age}")
```

#### while 循环

```python
count = 0
while count < 5:
    print(count)
    count += 1

# while-else（循环正常结束执行 else）
while count < 3:
    print(count)
    count += 1
else:
    print("Loop completed")
```

### 4.3 循环控制

```python
# break - 跳出循环
for i in range(10):
    if i == 5:
        break
    print(i)  # 0, 1, 2, 3, 4

# continue - 跳过本次循环
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0, 1, 3, 4

# pass - 占位符（什么都不做）
for i in range(5):
    pass  # TODO: 实现逻辑
```

### 4.4 匹配表达式（match）- Python 3.10+

```python
# 类似 switch-case（更强大）
def http_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return "Unknown"

# 支持模式匹配
def describe_point(point):
    match point:
        case (0, 0):
            return "Origin"
        case (x, 0):
            return f"X-axis at {x}"
        case (0, y):
            return f"Y-axis at {y}"
        case (x, y):
            return f"Point at ({x}, {y})"

# 匹配字典
def get_config(config):
    match config:
        case {"host": host, "port": port}:
            return f"{host}:{port}"
        case {"host": host}:
            return f"{host}:80"
        case _:
            return "Default"
```

---

## 5. 函数

### 5.1 函数定义与调用

```python
# 基本函数
def greet(name):
    """问候函数"""
    return f"Hello, {name}!"

# 调用函数
message = greet("Alice")

# 多返回值（实际返回元组）
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

min_val, max_val, total = get_stats([1, 2, 3, 4, 5])
```

### 5.2 参数类型

```python
# 位置参数
def func(a, b, c):
    print(a, b, c)

func(1, 2, 3)

# 关键字参数
func(a=1, b=2, c=3)
func(1, b=2, c=3)  # 混合使用

# 默认参数
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")           # Hello, Alice!
greet("Bob", "Hi")       # Hi, Bob!

# ⚠️ 默认参数陷阱（重要！）

## 5.2.1 为什么会出问题？

在 Python 中，**默认参数在函数定义时只会被评估一次**，而不是每次调用时重新创建。这意味着可变对象（如列表、字典）作为默认参数会被所有调用共享。

```python
# ❌ 错误写法 - 可变默认参数
def append_to(element, to=[]):
    to.append(element)
    return to

# 调用1
result1 = append_to(1)
print(result1)  # 输出: [1]

# 调用2 - 预期返回 [2]，实际返回 [1, 2]！
result2 = append_to(2)
print(result2)  # 输出: [1, 2]

# 调用3 - 继续累积！
result3 = append_to(3)
print(result3)  # 输出: [1, 2, 3]
```

**内存分析图：**

```
函数定义时
    ↓
创建空列表 to = []  ←─────┐
    ↓                     │
调用 append_to(1)         │
    ↓                     │
to.append(1) → to=[1] ────┼── 共享同一个列表对象
    ↓                     │
调用 append_to(2)         │
    ↓                     │
to.append(2) → to=[1,2] ──┘
```

## 5.2.2 哪些类型会出问题？

所有**可变对象**都可能遇到这个问题：

```python
# ❌ 列表作为默认参数
def add_item(item, items=[]):
    items.append(item)
    return items

# ❌ 字典作为默认参数
def set_config(key, value, config={}):
    config[key] = value
    return config

# ❌ 集合作为默认参数
def add_tag(tag, tags=set()):
    tags.add(tag)
    return tags
```

## 5.2.3 正确做法

使用 `None` 作为哨兵值，在函数内部创建新对象：

```python
# ✅ 正确做法
def append_to(element, to=None):
    if to is None:
        to = []  # 每次调用时创建新列表
    to.append(element)
    return to

# 测试
print(append_to(1))  # [1]
print(append_to(2))  # [2] - 独立的新列表
print(append_to(3))  # [3] - 独立的新列表

# ✅ 字典的正确写法
def set_config(key, value, config=None):
    if config is None:
        config = {}  # 每次调用时创建新字典
    config[key] = value
    return config

# ✅ 带默认值的安全模式
def process_items(items=None):
    if items is None:
        items = []  # 创建新列表
    # 处理 items...
    return items
```

## 5.2.4 总结

| 写法 | 行为 | 结果 |
|------|------|------|
| `to=[]` | 列表在定义时创建，所有调用共享 | ❌ 状态污染 |
| `to=None` | 每次调用时创建新对象 | ✅ 独立状态 |

> 💡 **记住**：永远不要使用可变对象（`list`、`dict`、`set` 等）作为默认参数，除非你**有意**要共享状态。
```

### 5.3 *args 和 **kwargs

```python
# *args - 可变位置参数
def sum_all(*args):
    print(args)           # 元组 (1, 2, 3, 4)
    return sum(args)

sum_all(1, 2, 3, 4)

# **kwargs - 可变关键字参数
def print_info(**kwargs):
    print(kwargs)         # 字典 {'name': 'Alice', 'age': 25}

print_info(name="Alice", age=25)

# 组合使用
def func(pos, *args, **kwargs):
    print(pos)       # 位置参数
    print(args)      # 额外的位置参数
    print(kwargs)    # 关键字参数
```

### 5.4 函数注解（类型提示）

```python
# 类型注解 - Python 3.5+
def greet(name: str) -> str:
    return f"Hello, {name}!"

# 复杂类型
from typing import List, Dict, Optional, Union

def process_data(
    data: List[int],
    config: Optional[Dict[str, str]] = None
) -> Union[int, str]:
    """处理数据并返回结果"""
    if not data:
        return "No data"
    return sum(data)

# Python 3.9+ 可直接使用内置类型注解
def greet(name: list[str]) -> dict[str, int]:
    return {name[0]: len(name)}
```

### 5.5 特殊函数

#### lambda 函数（匿名函数）

```python
# 基本语法
square = lambda x: x ** 2
add = lambda x, y: x + y

# 使用场景：短函数、回调、排序
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_nums = sorted(numbers, key=lambda x: -x)  # 降序

# 高阶函数
result = map(lambda x: x * 2, [1, 2, 3])  # [2, 4, 6]
result = filter(lambda x: x > 2, [1, 2, 3])  # [3]
result = reduce(lambda x, y: x + y, [1, 2, 3])  # 6
```

#### 闭包

```python
# 闭包：记住外层函数的变量
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

times2 = make_multiplier(2)
times3 = make_multiplier(3)
print(times2(5))  # 10
print(times3(5))  # 15

# 使用 nonlocal 在嵌套函数中修改外层变量
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

### 5.6 装饰器

```python
# 简单装饰器
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()

# 装饰器工厂（带参数）
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet():
    print("Hello!")

# 使用 functools.wraps 保留原函数信息

## 为什么需要 functools.wraps？

当使用装饰器时，装饰器返回的 `wrapper` 函数会**替换**原函数。这意味着：

- `wrapper.__name__` 不再是原函数名
- `wrapper.__doc__` 不再是原函数的文档字符串
- 其他元数据（如 `__module__`、`__annotations__`）也会丢失

这会导致：
- 调试困难：栈跟踪中显示 `wrapper` 而不是实际函数名
- 文档混乱：`help(add)` 显示的是 wrapper 的信息
- 类型检查失效：静态分析工具无法正确识别函数签名

## 不使用 functools.wraps 的问题演示

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def add(a, b):
    """Add two numbers"""
    return a + b

print(add.__name__)      # 输出: wrapper （应该是 add）
print(add.__doc__)       # 输出: None （应该是 "Add two numbers"）
help(add)                # 显示的是 wrapper 的信息，不是 add 的
```

## 使用 functools.wraps 解决问题

```python
import functools

def logged(func):
    @functools.wraps(func)  # 复制原函数的元数据到 wrapper
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logged
def add(a, b):
    """Add two numbers"""
    return a + b

print(add.__name__)      # 输出: add ✅
print(add.__doc__)       # 输出: Add two numbers ✅
help(add)                # 正确显示 add 的信息 ✅
```

## functools.wraps 复制的属性

`functools.wraps` 会自动复制以下属性到 wrapper 函数：
- `__name__` - 函数名
- `__qualname__` - 限定名称
- `__doc__` / `__notes__` - 文档字符串
- `__module__` - 模块名
- `__annotations__` - 类型注解
- `__dict__` - 字典属性
- `__wrapped__` - 指向原函数（用于反向追溯）

```python
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    """This is a slow function"""
    import time
    time.sleep(1)
    return "Done"

print(slow_function.__name__)  # slow_function
print(slow_function.__doc__)   # This is a slow function
print(slow_function.__wrapped__)  # 指向原函数
```

> 💡 **最佳实践**：**始终**在装饰器的 wrapper 中使用 `@functools.wraps(func)`，除非有特殊原因不需要保留原函数信息。
```

---

## 6. 错误处理

### 6.1 异常捕获

```python
# 基本 try-except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# 捕获多个异常
try:
    data = int(input())
except (ValueError, TypeError):
    print("Invalid input")

# 捕获异常对象
try:
    risky_operation()
except Exception as e:
    print(f"Error: {e}")
    print(type(e).__name__)

# else 和 finally
try:
    f = open("file.txt")
except FileNotFoundError:
    print("File not found")
else:
    print("File opened successfully")
    f.close()
finally:
    print("Cleanup")
```

### 6.2 抛出异常

```python
# 抛出异常
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return True

# 自定义异常
class CustomError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

raise CustomError("Something went wrong", code=500)
```

### 6.3 上下文管理器

```python
# 使用 with 语句
with open("file.txt", "r") as f:
    content = f.read()
# 文件自动关闭

# 自定义上下文管理器
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        print(f"Elapsed: {self.end - self.start:.2f}s")

with Timer() as t:
    # 执行代码
    pass

# 使用 contextlib
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Acquiring resource")
    yield "resource"
    print("Releasing resource")

with managed_resource() as r:
    print(f"Using {r}")
```

---

## 7. 常用内置函数

### 7.1 类型相关

```python
type(10)           # <class 'int'>
isinstance(10, int)  # True（更推荐）
len("hello")       # 5
id(obj)            # 对象内存地址
callable(func)     # 是否可调用
```

### 7.2 迭代相关

```python
list(range(10))        # [0, 1, 2, ..., 9]
enumerate(["a","b"])   # [(0, 'a'), (1, 'b')]
zip([1,2], [3,4])      # [(1,3), (2,4)]
reversed([1,2,3])      # 反向迭代器
sorted([3,1,2])        # [1,2,3]
any([False, True])    # True
all([True, True])     # True
next(iter)             # 获取下一个元素
```

### 7.3 转换与操作

```python
list("abc")      # ['a', 'b', 'c']
dict([('a',1),('b',2)])  # {'a': 1, 'b': 2}
set([1,2,2])     # {1, 2}
tuple([1,2])    # (1, 2)
hex(255)        # '0xff'
oct(8)          # '0o10'
bin(5)          # '0b101'
ord('a')        # 97
chr(97)         # 'a'
round(3.7)      # 4
abs(-5)         # 5
pow(2, 3)       # 8
divmod(10, 3)   # (3, 1)
```

### 7.4 对象操作

```python
getattr(obj, 'attr', default)  # 获取属性
setattr(obj, 'attr', value)    # 设置属性
hasattr(obj, 'attr')           # 检查属性
vars(obj)                      # 对象的 __dict__
dir(obj)                       # 所有属性和方法
help(obj.method)               # 帮助文档
```

### 7.5 函数式编程

```python
map(lambda x: x*2, [1,2,3])     # 映射
filter(lambda x: x>2, [1,2,3])  # 过滤
from functools import reduce
reduce(lambda x,y: x+y, [1,2,3])  # 累积
```

---

## 8. 实战示例

### 8.1 猜数字游戏

```python
import random

def guess_number():
    target = random.randint(1, 100)
    attempts = 0
    max_attempts = 7
    
    print("我已经想好了一个 1-100 的数字，你有 7 次机会猜测！")
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"请输入你的猜测 ({max_attempts - attempts} 次机会): "))
        except ValueError:
            print("请输入有效的数字！")
            continue
            
        attempts += 1
        
        if guess == target:
            print(f"🎉 恭喜你，猜对了！数字就是 {target}")
            return True
        elif guess < target:
            print("太小了！")
        else:
            print("太大了！")
    
    print(f"游戏结束！正确答案是 {target}")
    return False

if __name__ == "__main__":
    guess_number()
```

### 8.2 成绩统计程序

```python
from typing import List, Dict

def analyze_grades(scores: Dict[str, int]) -> Dict[str, float]:
    """分析成绩并返回统计信息"""
    if not scores:
        return {"average": 0, "max": 0, "min": 0, "count": 0}
    
    values = list(scores.values())
    return {
        "average": sum(values) / len(values),
        "max": max(values),
        "min": min(values),
        "count": len(values),
        "pass_count": sum(1 for v in values if v >= 60),
        "fail_count": sum(1 for v in values if v < 60)
    }

def main():
    grades = {
        "Alice": 85,
        "Bob": 72,
        "Charlie": 58,
        "Diana": 90,
        "Eve": 65
    }
    
    stats = analyze_grages(grades)
    
    print("=" * 30)
    print("成绩统计分析")
    print("=" * 30)
    print(f"总人数: {stats['count']}")
    print(f"平均分: {stats['average']:.2f}")
    print(f"最高分: {stats['max']}")
    print(f"最低分: {stats['min']}")
    print(f"及格人数: {stats['pass_count']}")
    print(f"不及格人数: {stats['fail_count']}")

if __name__ == "__main__":
    main()
```

---

## 下一步学习

完成本篇学习后，建议继续学习：

1. **函数式编程与面向对象** - 深入理解 Python 的函数式特性与 OOP
2. **Python 高级用法** - 文件 IO、网络、多线程、数据库
3. **Python 工程化** - 包管理、模块化、中间件
4. **Python 服务端框架** - Flask、Django、FastAPI

---

*持续更新中...*