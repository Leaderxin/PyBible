# Python 开发圣经 - 函数式编程与面向对象篇

> 目标读者：具备其他编程语言经验的开发者  
> Python 版本：3.11+  
> 更新时间：2025

## 目录

1. [函数式编程](#1-函数式编程)
2. [面向对象编程基础](#2-面向对象编程基础)
3. [面向对象高级特性](#3-面向对象高级特性)
4. [设计模式](#4-设计模式)

---

## 1. 函数式编程

### 1.1 函数式编程概述

函数式编程的核心思想：
- **不可变性**：避免修改共享状态
- **一等公民**：函数可以像变量一样传递
- **声明式**：描述"做什么"而非"怎么做"
- **无副作用**：函数不修改外部状态

```python
# 函数式 vs 命令式
# 命令式
def sum_even(numbers):
    total = 0
    for n in numbers:
        if n % 2 == 0:
            total += n
    return total

# 函数式
def sum_even_fp(numbers):
    return sum(filter(lambda x: x % 2 == 0, numbers))

# 或使用列表推导式
def sum_even_lc(numbers):
    return sum(x for x in numbers if x % 2 == 0)
```

### 1.2 高阶函数

```python
# 高阶函数：接受函数作为参数或返回函数

# 1. 接受函数作为参数
def apply_operation(nums, operation):
    return [operation(n) for n in nums]

result = apply_operation([1, 2, 3], lambda x: x ** 2)
print(result)  # [1, 4, 9]

# 2. 返回函数（工厂函数）
def make_multiplier(factor):
    def multiplier(x):
        return x * factor
    return multiplier

double = make_multiplier(2)
print(double(5))  # 10

# 3. 组合函数
def compose(f, g):
    return lambda x: f(g(x))

add_one = lambda x: x + 1
square = lambda x: x ** 2
f = compose(square, add_one)
print(f(3))  # (3+1)^2 = 16
```

### 1.3 内置高阶函数

#### map - 映射

```python
# map(function, iterable)
numbers = [1, 2, 3, 4, 5]

# 使用 map
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# 多个可迭代对象
a = [1, 2, 3]
b = [10, 20, 30]
result = list(map(lambda x, y: x + y, a, b))
print(result)  # [11, 22, 33]
```

#### filter - 过滤

```python
# filter(function, iterable)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 过滤偶数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# 过滤非空字符串
strings = ["", "hello", "", "world", ""]
non_empty = list(filter(None, strings))  # 移除 falsy 值
print(non_empty)  # ['hello', 'world']
```

#### reduce - 累积

```python
# reduce(function, iterable, initial)
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# 求和
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15

# 阶乘
factorial = reduce(lambda x, y: x * y, range(1, 6))
print(factorial)  # 120

# 带初始值
total_with_init = reduce(lambda x, y: x + y, numbers, 100)
print(total_with_init)  # 115 (100 + 15)
```

#### sorted 与 key

```python
# sorted(iterable, key, reverse)
students = [
    {"name": "Alice", "age": 25, "score": 85},
    {"name": "Bob", "age": 22, "score": 90},
    {"name": "Charlie", "age": 28, "score": 78}
]

# 按年龄排序
by_age = sorted(students, key=lambda x: x["age"])
print(by_age)

# 按分数降序排序
by_score = sorted(students, key=lambda x: x["score"], reverse=True)
print(by_score)

# 多级排序
by_score_age = sorted(students, key=lambda x: (-x["score"], x["age"]))
print(by_score_age)
```

### 1.4 匿名函数与闭包

```python
# 匿名函数 (lambda)
square = lambda x: x ** 2
add = lambda x, y: x + y
print(square(5))  # 25
print(add(3, 4))  # 7

# 闭包 - 记住外层函数的变量
def makeadder(n):
    return lambda x: x + n

add5 = makeadder(5)
add10 = makeadder(10)
print(add5(3))   # 8
print(add10(3))  # 13

# 闭包捕获可变对象
def make_counter():
    count = [0]  # 使用列表捕获
    def counter():
        count[0] += 1
        return count[0]
    return counter

c = make_counter()
print(c())  # 1
print(c())  # 2

# nonlocal 关键字
def make_counter2():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter
```

### 1.5 函数组合与柯里化

```python
# 函数组合
def compose(*functions):
    def composed(x):
        result = x
        for f in reversed(functions):
            result = f(result)
        return result
    return composed

# 示例
f = compose(
    lambda x: x + 1,
    lambda x: x * 2,
    lambda x: x - 3
)
print(f(5))  # ((5-3)*2)+1 = 5

# 柯里化
def curry(func):
    """将多参数函数转换为单参数函数链"""
    def curried(*args):
        if len(args) >= func.__code__.co_argcount:
            return func(*args)
        return lambda *args2: curried(*(args + args2))
    return curried

@curry
def add(a, b, c):
    return a + b + c

print(add(1)(2)(3))    # 6
print(add(1, 2)(3))    # 6
print(add(1)(2, 3))    # 6
```

### 1.6 偏函数

```python
# partial - 创建偏函数
from functools import partial

def power(base, exponent):
    return base ** exponent

# 创建一个平方函数
square = partial(power, exponent=2)
print(square(5))  # 25

# 创建一个立方函数
cube = partial(power, exponent=3)
print(cube(2))  # 8

# 带多个固定参数
def greet(greeting, name, punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

say_hello = partial(greet, "Hello")
print(say_hello("Alice"))  # Hello, Alice!
print(say_hello("Bob", "?"))  # Hello, Bob?
```

### 1.7 迭代器与生成器

```python
# 迭代器协议
class Counter:
    def __init__(self, max):
        self.current = 0
        self.max = max
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.max:
            raise StopIteration
        result = self.current
        self.current += 1
        return result

for i in Counter(5):
    print(i)  # 0, 1, 2, 3, 4

# 生成器 - 使用 yield
def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count += 1

gen = count_up_to(5)
print(next(gen))  # 1
print(next(gen))  # 2

for i in count_up_to(3):
    print(i)  # 1, 2, 3

# 生成器表达式
gen = (x ** 2 for x in range(5))
print(list(gen))  # [0, 1, 4, 9, 16]

# 无限生成器
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for i in range(10):
    print(next(fib))  # 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

### 1.8 函数式工具

```python
# itertools 模块
from itertools import count, cycle, repeat, islice, chain, groupby

# count - 无限计数器
for i in islice(count(10), 5):
    print(i)  # 10, 11, 12, 13, 14

# cycle - 无限循环
counter = 0
for item in islice(cycle(['A', 'B', 'C']), 7):
    print(item)  # A, B, C, A, B, C, A

# repeat - 重复
result = list(repeat(5, 3))  # [5, 5, 5]

# chain - 连接多个迭代器
result = list(chain([1, 2], [3, 4], [5]))  # [1, 2, 3, 4, 5]

# groupby - 分组
data = [("apple", "fruit"), ("banana", "fruit"), ("carrot", "vegetable")]
for key, group in groupby(data, key=lambda x: x[1]):
    print(f"{key}: {list(group)}")

# functools 模块
from functools import lru_cache, reduce, partial, wraps

# 记忆化缓存
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(100))  # 快速计算
```

---

## 2. 面向对象编程基础

### 2.1 类与对象

```python
# 定义类
class Person:
    """人员类"""
    
    # 类属性（所有实例共享）
    species = "Homo sapiens"
    
    # 初始化方法
    def __init__(self, name: str, age: int):
        # 实例属性
        self.name = name
        self.age = age
        self._private = "私有属性"  # 约定为私有
    
    # 实例方法
    def greet(self):
        return f"Hello, I'm {self.name}"
    
    # 特殊方法：字符串表示
    def __str__(self):
        return f"Person({self.name}, {self.age})"
    
    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age})"

# 创建实例
person = Person("Alice", 25)
print(person.name)      # Alice
print(person.greet())   # Hello, I'm Alice
print(person)           # Person(Alice, 25)
```

### 2.2 属性与方法

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    # 计算属性（只读）
    @property
    def area(self):
        return self.width * self.height
    
    @property
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    # setter 属性
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
    
    # 实例方法
    def scale(self, factor):
        self.width *= factor
        self.height *= factor

rect = Rectangle(10, 5)
print(rect.area)      # 50
rect.scale(2)
print(rect.area)      # 200
rect.width = 15       # 使用 setter 验证
```

### 2.3 继承与多态

```python
# 基类
class Animal:
    def __init__(self, name: str):
        self.name = name
    
    def speak(self):
        raise NotImplementedError("Subclass must implement speak")
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"

# 子类
class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

# 多态
def make_speak(animals: list[Animal]):
    for animal in animals:
        print(f"{animal.name}: {animal.speak()}")

animals = [Dog("Buddy"), Cat("Whiskers"), Dog("Max")]
make_speak(animals)
```

### 2.4 多重继承与 MRO

```python
# 多重继承
class Flyable:
    def fly(self):
        return "Flying!"

class Swimmable:
    def swim(self):
        return "Swimming!"

class Duck(Animal, Flyable, Swimmable):
    def speak(self):
        return "Quack!"

duck = Duck("Donald")
print(duck.fly())     # Flying!
print(duck.swim())    # Swimming!

# 方法解析顺序 (MRO)
print(Duck.__mro__)
# (<class 'Duck'>, <class 'Animal'>, <class 'Flyable'>, 
#  <class 'Swimmable'>, <class 'object'>)

# super() - 调用父类方法
class EnhancedDog(Dog):
    def speak(self):
        parent_sound = super().speak()  # 调用父类
        return f"{parent_sound} Also barks!"
```

### 2.5 特殊方法（魔术方法）

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # 算术运算
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)
    
    # 比较运算
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)
    
    # 一元运算
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __abs__(self):
        return (self.x**2 + self.y**2) ** 0.5
    
    # 其他
    def __len__(self):
        return 2
    
    def __getitem__(self, index):
        return [self.x, self.y][index]
    
    def __call__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)     # (4, 6)
print(v1 * 3)      # (3, 6)
print(3 * v1)      # (3, 6)
print(abs(v1))     # 2.236...
print(v1())        # (1, 2)
```

---

## 3. 面向对象高级特性

### 3.1 抽象基类 (ABC)

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    # 可以有具体方法
    def describe(self):
        return f"A {self.__class__.__name__} with area {self.area():.2f}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# 不能直接实例化抽象类
# shape = Shape()  # TypeError!

rect = Rectangle(10, 5)
print(rect.describe())  # A Rectangle with area 50.00
```

### 3.2 协议（Protocol）- 静态duck typing

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None:
        ...

class Circle:
    def draw(self):
        print("Drawing circle")

class Square:
    def draw(self):
        print("Drawing square")

def render(drawable: Drawable):
    drawable.draw()

render(Circle())  # 运行时检查通过
render(Square())  # 运行时检查通过

# 类型检查（mypy）
# class NotDrawable:
#     pass
# render(NotDrawable())  # 运行时检查失败
```

### 3.3 数据类（dataclass）

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Person:
    name: str
    age: int
    email: str = ""  # 带默认值的字段
    hobbies: List[str] = field(default_factory=list)
    
    # 初始化后的处理
    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")

# 使用
person = Person("Alice", 25, "alice@example.com", ["reading", "coding"])
print(person)  # Person(name='Alice', age=25, ...)

# 比较
p1 = Person("Alice", 25)
p2 = Person("Alice", 25)
print(p1 == p2)  # True（自动生成 __eq__）

# 不可变数据类
@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
# p.x = 3  # FrozenInstanceError
```

### 3.4 命名元组

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int
    
    def distance_from_origin(self):
        return (self.x**2 + self.y**2) ** 0.5

p = Point(3, 4)
print(p.x, p.y)           # 3 4
print(p.distance_from_origin())  # 5.0

# 可用于类型提示
points: list[Point] = [Point(1, 2), Point(3, 4)]
```

### 3.5 枚举

```python
from enum import Enum, IntEnum, Flag, auto

# 基本枚举
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# 整数枚举
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# 标志枚举（可组合）
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

# 使用
read_write = Permission.READ | Permission.WRITE
print(Permission.READ in read_write)  # True
print(Permission.EXECUTE in read_write)  # False

# 迭代
for color in Color:
    print(color.name, color.value)
```

### 3.6 类型别名与泛型

```python
from typing import TypeVar, Generic, List, Dict, Optional, Union

# 类型变量
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# 泛型类
class Stack(Generic[T]):
    def __init__(self):
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()
    
    def peek(self) -> Optional[T]:
        return self._items[-1] if self._items else None

# 使用
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(int_stack.pop())  # 2

# 泛型函数
def first(items: List[T]) -> Optional[T]:
    return items[0] if items else None

# 约束类型变量
def max_of(a: T, b: T) -> T:
    """要求 T 支持比较运算"""
    return a if a > b else b
```

### 3.7 描述器（Descriptor）

```python
# 描述器协议
class Descriptor:
    def __get__(self, obj, objtype=None):
        return f"Getting from {obj}"
    
    def __set__(self, obj, value):
        print(f"Setting {value} to {obj}")
    
    def __delete__(self, obj):
        print(f"Deleting from {obj}")

class MyClass:
    attr = Descriptor()

# 使用
obj = MyClass()
print(obj.attr)  # Getting from obj
obj.attr = 42    # Setting 42 to obj
del obj.attr     # Deleting from obj

# 实际应用：属性验证
class Range:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        return getattr(obj, f"_{self.name}")
    
    def __set__(self, obj, value):
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"{self.name} must be between {self.min_val} and {self.max_val}")
        setattr(obj, f"_{self.name}", value)

class Temperature:
    celsius = Range(-273.15, 1000)
    fahrenheit = Range(-459.67, 1832)
    
    def __init__(self, celsius):
        self.celsius = celsius
```

### 3.8 元类

```python
# 元类 - 类的类
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        # 可以修改或增强类定义
        namespace['created_by'] = 'Meta'
        return super().__new__(mcs, name, bases, namespace)
    
    def __call__(cls, *args, **kwargs):
        # 控制实例化过程
        print(f"Creating instance of {cls.__name__}")
        return super().__call__(*args, **kwargs)

class MyClass(metaclass=Meta):
    def __init__(self, value):
        self.value = value

obj = MyClass(42)  # Creating instance of MyClass
print(obj.created_by)  # Meta

# 实际应用：单例模式
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        print("Connecting to database...")

db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

---

## 4. 设计模式

设计模式是软件工程中常见问题的可复用解决方案，是经过验证的编程经验总结。

### 4.1 单例模式 (Singleton Pattern)

**作用**：确保一个类只有一个实例，并提供一个全局访问点。

**常用场景**：
- 数据库连接池（只创建一个连接实例，避免资源浪费）
- 配置管理器（全局配置只需加载一次）
- 日志记录器（整个应用共享一个日志实例）
- 线程池、缓存管理器等需要唯一实例的场景

```python
# 方式1：使用元类（推荐）
# 元类在类定义时拦截 __call__，控制实例创建过程
class SingletonMeta(type):
    _instances = {}  # 类变量，存储所有单例实例
    
    def __call__(cls, *args, **kwargs):
        # 检查是否已存在实例，不存在则创建
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    """数据库连接类，整个应用只需一个实例"""
    def __init__(self):
        self.connection = "Connected"
    
    def query(self, sql):
        return f"Executing: {sql}"

# 方式2：装饰器（更灵活）
def singleton(cls):
    """单例装饰器：将被装饰的类转换为单例模式"""
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Config:
    """配置管理类，全局共享一份配置"""
    def __init__(self):
        self.settings = {}

# 方式3：__new__ 方法（最简单）
class App:
    """应用类，确保只有一个应用实例"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 4.2 工厂模式 (Factory Pattern)

**作用**：封装对象的创建过程，使代码与具体类解耦，通过接口创建对象而不必知道具体实现类。

**常用场景**：
- 数据库连接创建（根据配置返回 MySQL/PostgreSQL/MongoDB 连接）
- 支付方式选择（支付宝、微信、银联等）
- 跨平台 UI 组件（WindowsButton、MacButton）
- 插件系统中根据类型加载不同插件

```python
# 简单工厂：用一个类集中创建所有产品
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class AnimalFactory:
    """动物工厂：根据类型字符串创建对应的动物实例"""
    @staticmethod
    def create_animal(animal_type):
        # 映射表：类型字符串 -> 类
        animals = {"dog": Dog, "cat": Cat}
        if animal_type not in animals:
            raise ValueError(f"Unknown animal: {animal_type}")
        return animals[animal_type]()

# 工厂方法：定义创建接口，子类决定具体创建哪个类
from abc import ABC, abstractmethod

class Animal(ABC):
    """动物抽象基类，定义动物的标准接口"""
    @abstractmethod
    def speak(self):
        """动物发声"""
        pass

class Dog(Animal):
    """狗类，实现动物接口"""
    def speak(self):
        return "Woof!"

class Cat(Animal):
    """猫类，实现动物接口"""
    def speak(self):
        return "Meow!"

class AnimalFactory(ABC):
    """抽象工厂：定义创建动物的接口"""
    @abstractmethod
    def create_animal(self) -> Animal:
        """创建动物实例，由子类具体实现"""
        pass

class DogFactory(AnimalFactory):
    """狗的工厂：专门创建狗实例"""
    def create_animal(self) -> Animal:
        return Dog()

class CatFactory(AnimalFactory):
    """猫的工厂：专门创建猫实例"""
    def create_animal(self) -> Animal:
        return Cat()
```

### 4.3 观察者模式 (Observer Pattern)

**作用**：定义对象间的一对多依赖关系，当一个对象状态改变时，所有依赖它的对象都会自动收到通知。

**常用场景**：
- 事件系统（用户注册后发送邮件、短信、推送通知）
- MVC 架构中的 Model-View 同步
- 股票价格监控（价格变化时通知所有订阅者）
- 消息队列、发布-订阅系统

```python
from typing import Callable, List

class EventManager:
    """事件管理器：维护事件与监听器的映射关系"""
    def __init__(self):
        self._listeners: dict[str, List[Callable]] = {}
    
    def subscribe(self, event: str, callback: Callable):
        """订阅事件：添加事件监听器"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    
    def unsubscribe(self, event: str, callback: Callable):
        """取消订阅：移除事件监听器"""
        if event in self._listeners:
            self._listeners[event].remove(callback)
    
    def notify(self, event: str, *args, **kwargs):
        """通知：触发所有订阅该事件的回调"""
        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(*args, **kwargs)

# 使用示例
events = EventManager()

def on_user_registered(user):
    """监听器1：发送欢迎邮件"""
    print(f"Sending welcome email to {user}")

def on_user_registered_log(user):
    """监听器2：记录注册日志"""
    print(f"Logging: {user} registered")

# 订阅事件
events.subscribe("user.registered", on_user_registered)
events.subscribe("user.registered", on_user_registered_log)

# 触发事件，通知所有监听器
events.notify("user.registered", "Alice")
```

### 4.4 策略模式 (Strategy Pattern)

**作用**：定义一系列算法，将每个算法封装起来，使它们可以互相替换，让算法独立于使用它的客户端。

**常用场景**：
- 排序算法选择（快速排序、归并排序、堆排序）
- 支付方式（微信、支付宝、银联）
- 压缩算法（ZIP、RAR、7z）
- 缓存策略（LRU、LFU、FIFO）
- 表单验证（不同场景使用不同验证规则）

```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    """排序策略抽象基类"""
    @abstractmethod
    def sort(self, data: list) -> list:
        """排序算法接口"""
        pass

class QuickSort(SortStrategy):
    """快速排序策略：平均时间复杂度 O(n log n)"""
    def sort(self, data: list) -> list:
        # 实际项目中应实现真正的快速排序
        return sorted(data)

class MergeSort(SortStrategy):
    """归并排序策略：稳定排序，时间复杂度 O(n log n)"""
    def sort(self, data: list) -> list:
        return sorted(data, key=lambda x: x)

class Sorter:
    """排序器：持有策略对象，调用策略的排序方法"""
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    @property
    def strategy(self):
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: SortStrategy):
        """运行时切换排序策略"""
        self._strategy = strategy
    
    def sort(self, data: list) -> list:
        return self._strategy.sort(data)

# 使用
sorter = Sorter(QuickSort())
print(sorter.sort([3, 1, 2]))

# 运行时切换为归并排序
sorter.strategy = MergeSort()
print(sorter.sort([3, 1, 2]))
```

### 4.5 装饰器模式 (Decorator Pattern)

**作用**：动态地给对象添加额外职责，比继承更灵活地扩展对象功能。

**常用场景**：
- 咖啡店点餐系统（基础咖啡 + 牛奶 + 糖 + 奶油）
- 快餐店点餐（汉堡 + 薯条 + 可乐 + 套餐优惠）
- 权限控制（基础权限 + VIP权限 + 超级管理员）
- 日志记录、性能监控（在方法执行前后添加逻辑）

```python
# 装饰器模式（不是函数装饰器，而是类装饰器）
class Coffee:
    """基础咖啡组件"""
    def cost(self):
        return 5

class CoffeeDecorator:
    """咖啡装饰器基类：持有一个咖啡组件的引用"""
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self):
        return self._coffee.cost()

class Milk(CoffeeDecorator):
    """牛奶装饰器：增加牛奶，价格 +1.5"""
    def cost(self):
        return self._coffee.cost() + 1.5

class Sugar(CoffeeDecorator):
    """糖装饰器：增加糖，价格 +0.5"""
    def cost(self):
        return self._coffee.cost() + 0.5

class Whip(CoffeeDecorator):
    """奶油装饰器：增加奶油，价格 +2"""
    def cost(self):
        return self._coffee.cost() + 2

# 使用：层层装饰
coffee = Coffee()           # 基础咖啡：5元
coffee = Milk(coffee)       # 加牛奶：6.5元
coffee = Sugar(coffee)      # 加糖：7元
coffee = Whip(coffee)       # 加奶油：9元
print(coffee.cost())  # 9.0
```

### 4.6 适配器模式 (Adapter Pattern)

**作用**：将一个类的接口转换成客户期望的另一个接口，使原本不兼容的类可以合作。

**常用场景**：
- 旧系统升级（新代码调用旧API）
- 第三方库集成（统一不同SDK的接口）
- 数据格式转换（JSON、XML、CSV 互转）
- 跨语言调用（Python 调用 Java/C++ 库）

```python
# 适配器模式
class OldAPI:
    """旧接口：遗留系统的方法"""
    def legacy_method(self, data):
        return f"Processed: {data}"

class NewInterface:
    """新接口：现代系统定义的接口"""
    def modern_method(self, data, options=None):
        return f"Processed with options: {data}"

class Adapter(NewInterface):
    """适配器：将旧接口适配为新接口"""
    def __init__(self, legacy: OldAPI):
        self._legacy = legacy
    
    def modern_method(self, data, options=None):
        # 将新接口调用转换为旧接口调用
        result = self._legacy.legacy_method(data)
        if options:
            return f"{result}, options: {options}"
        return result

# 使用：通过适配器使用旧系统
legacy = OldAPI()
adapter = Adapter(legacy)
print(adapter.modern_method("test", options={"key": "value"}))
```

### 4.7 迭代器模式 (Iterator Pattern)

**作用**：提供一种方法顺序访问集合中的元素，而不暴露底层表示。

**常用场景**：
- 遍历树形结构（DOM树、文件系统）
- 遍历图（社交网络关系图）
- 翻页加载（数据库分页遍历）
- 自定义迭代逻辑（深度优先、广度优先遍历）

```python
class TreeNode:
    """二叉树节点"""
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class TreeIterator:
    """树的中序遍历迭代器"""
    def __init__(self, root):
        self._stack = []    # 用栈存储待访问节点
        self._current = root  # 当前指向的节点
    
    def __iter__(self):
        """返回迭代器本身"""
        return self
    
    def __next__(self):
        """返回下一个元素（中序遍历顺序：左-根-右）"""
        # 沿着左子树一直向下，把路径上的节点入栈
        while self._current or self._stack:
            while self._current:
                self._stack.append(self._current)
                self._current = self._current.left
            
            # 弹出栈顶节点，访问它
            self._current = self._stack.pop()
            value = self._current.value
            # 切换到右子树继续
            self._current = self._current.right
            return value
        
        # 遍历完成，抛出停止异常
        raise StopIteration

# 使用：遍历二叉树
#     1
#    / \
#   2   3
# 中序遍历结果：2, 1, 3
root = TreeNode(1, TreeNode(2), TreeNode(3))
for value in TreeIterator(root):
    print(value)  # 2, 1, 3
```

### 4.8 上下文管理器模式 (Context Manager Pattern)

**作用**：优雅地管理资源的获取和释放，确保资源使用后正确清理（如文件关闭、数据库连接释放、锁的获取释放）。

**常用场景**：
- 文件操作（自动关闭文件）
- 数据库连接（自动连接和断开）
- 线程锁（自动获取和释放锁）
- 临时修改状态（完成后恢复原状态）
- 性能计时（自动记录执行时间）

```python
# 上下文管理器
from contextlib import contextmanager

class DatabaseConnection:
    """数据库连接类"""
    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False
    
    def connect(self):
        """建立连接"""
        self.connected = True
        print(f"Connected to {self.db_name}")
    
    def disconnect(self):
        """断开连接"""
        self.connected = False
        print(f"Disconnected from {self.db_name}")
    
    def query(self, sql):
        if not self.connected:
            raise RuntimeError("Not connected")
        return f"Result: {sql}"

class DatabaseManager:
    """数据库管理器：实现上下文管理器协议"""
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        """进入上下文：创建并连接数据库"""
        self.connection = DatabaseConnection(self.db_name)
        self.connection.connect()
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文：确保资源释放"""
        if self.connection:
            self.connection.disconnect()
        return False  # 不抑制异常，异常会继续传播

# 使用：自动管理数据库连接生命周期
with DatabaseManager("mydb") as db:
    result = db.query("SELECT * FROM users")
    print(result)
# 离开 with 块时自动断开连接
```

---

## 5. 函数式与面向对象结合

### 5.1 常用模式

```python
# 数据转换管道
from functools import reduce

def pipe(*functions):
    """函数组合"""
    return lambda x: reduce(lambda v, f: f(v), functions, x)

# 示例
result = pipe(
    lambda x: x * 2,
    lambda x: x + 1,
    lambda x: str(x)
)(5)

print(result)  # "11"

# 链式调用
class Builder:
    def __init__(self, value):
        self.value = value
    
    def add(self, n):
        self.value += n
        return self
    
    def multiply(self, n):
        self.value *= n
        return self
    
    def build(self):
        return self.value

result = Builder(10).add(5).multiply(2).build()
print(result)  # 30

# 函数式数据处理
from dataclasses import dataclass
from typing import List

@dataclass
class Order:
    id: int
    customer: str
    amount: float
    status: str

orders = [
    Order(1, "Alice", 100.0, "completed"),
    Order(2, "Bob", 200.0, "pending"),
    Order(3, "Alice", 150.0, "completed"),
    Order(4, "Charlie", 80.0, "cancelled"),
]

# 函数式查询
def query(orders: List[Order], predicate, mapper):
    return list(map(mapper, filter(predicate, orders)))

# 查询 Alice 的已完成订单
alice_orders = query(
    orders,
    lambda o: o.customer == "Alice" and o.status == "completed",
    lambda o: o.amount
)
print(alice_orders)  # [100.0, 150.0]

# 计算总额
total = sum(alice_orders)
print(total)  # 250.0
```

---

## 6. 实战示例

### 6.1 事件驱动系统

```python
from dataclasses import dataclass, field
from typing import Callable, Dict, List
from datetime import datetime

@dataclass
class Event:
    name: str
    data: dict
    timestamp: datetime = field(default_factory=datetime.now)

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_name: str, handler: Callable):
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
    
    def unsubscribe(self, event_name: str, handler: Callable):
        if event_name in self._handlers:
            self._handlers[event_name].remove(handler)
    
    def publish(self, event: Event):
        print(f"[{event.timestamp}] Event: {event.name}")
        if event.name in self._handlers:
            for handler in self._handlers[event.name]:
                handler(event.data)

# 使用
bus = EventBus()

def on_user_login(data):
    print(f"User logged in: {data['username']}")

def on_user_action(data):
    print(f"Action logged: {data['action']}")

bus.subscribe("user.login", on_user_login)
bus.subscribe("user.action", on_user_action)

bus.publish(Event("user.login", {"username": "alice"}))
bus.publish(Event("user.action", {"action": "click", "button": "submit"}))
```

### 6.2 策略模式的日志系统

```python
from abc import ABC, abstractmethod
from datetime import datetime

class Logger(ABC):
    @abstractmethod
    def log(self, message: str):
        pass

class ConsoleLogger(Logger):
    def log(self, message: str):
        print(f"[{datetime.now()}] {message}")

class FileLogger(Logger):
    def __init__(self, filename: str):
        self.filename = filename
    
    def log(self, message: str):
        with open(self.filename, "a") as f:
            f.write(f"[{datetime.now()}] {message}\n")

class LoggerChain:
    def __init__(self):
        self._loggers: List[Logger] = []
    
    def add_logger(self, logger: Logger):
        self._loggers.append(logger)
        return self
    
    def log(self, message: str):
        for logger in self._loggers:
            logger.log(message)

# 使用
LoggerChain() \
    .add_logger(ConsoleLogger()) \
    .add_logger(FileLogger("app.log")) \
    .log("Application started")
```

---

## 下一步学习

完成本篇学习后，建议继续学习：

1. **Python 高级用法** - 文件 IO、网络请求、多线程、数据库操作
2. **Python 工程化** - 包管理、模块化、中间件
3. **Python 服务端框架** - Flask、Django、FastAPI

---

*持续更新中...*