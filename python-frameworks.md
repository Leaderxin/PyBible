# Python 开发圣经——服务端框架篇

> 目标读者：具备其他编程语言经验的开发者  
> Python 版本：3.11+  
> 更新时间：2025

## 目录

1. [Web 框架概述](#1-web-框架概述)
2. [Flask 轻量级框架](#2-flask-轻量级框架)
3. [Django 全栈框架](#3-django-全栈框架)
4. [FastAPI 现代高性能框架](#4-fastapi-现代高性能框架)
5. [框架对比与选型](#5-框架对比与选型)
6. [RESTful API 设计](#6-restful-api-设计)
7. [认证与授权](#7-认证与授权)
8. [部署与运维](#8-部署与运维)

---

## 1. Web 框架概述

### 1.1 Python Web 框架生态

```
Python Web 框架
├── 微型框架
│   ├── Flask          # 轻量、灵活
│   ├── FastAPI        # 现代、高性能、自动文档
│   └── Bottle         # 单文件框架
│
├── 全栈框架
│   ├── Django         # 完整解决方案、ORM、内置后台
│   └── Pyramid        # 可扩展、灵活
│
├── 异步框架
│   ├── aiohttp        # 异步 HTTP 客户端/服务端
│   ├── Starlette      # ASGI 框架
│   └── Tornado        # 异步、实时应用
│
└── API 框架
    ├── FastAPI        # 基于 Starlette
    ├── Falcon         # 高性能 API
    └── Eve            # REST API 框架
```

### 1.2 WSGI 与 ASGI

```python
# WSGI (Web Server Gateway Interface) - 同步
# 传统服务器如 Gunicorn、uWSGI 使用

# 最小 WSGI 应用
def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)
    return [b'Hello, World!']

# ASGI (Asynchronous Server Gateway Interface) - 异步
# 支持 WebSocket、长连接
# uvicorn、daphne 使用

# 最小 ASGI 应用
async def app(scope, receive, send):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'content-type', b'text/plain']],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, World!',
    })
```

---

## 2. Flask 轻量级框架

### 2.1 快速开始

```bash
# 安装
pip install flask

# 创建应用
```

```python
# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# 路由
@app.route("/")
def index():
    return {"message": "Hello, World!"}

@app.route("/api/users/<int:user_id>")
def get_user(user_id):
    return jsonify({
        "id": user_id,
        "name": f"User {user_id}"
    })

# POST 请求
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    return jsonify({"message": "User created", "data": data}), 201

# 启动服务器
if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

### 2.2 请求与响应

```python
from flask import (
    Flask, request, jsonify, 
    render_template, redirect, url_for, 
    make_response, session, flash
)

app = Flask(__name__)
app.secret_key = "secret-key"

# 获取请求数据
@app.route("/example")
def example():
    # URL 参数
    name = request.args.get("name", "Guest")
    
    # 表单数据
    email = request.form.get("email")
    
    # JSON 数据
    data = request.get_json()
    
    # 请求头
    auth = request.headers.get("Authorization")
    
    # 创建响应
    response = make_response(jsonify({"message": "OK"}))
    response.headers["X-Custom"] = "value"
    response.set_cookie("token", "abc123")
    
    return response

# 模板渲染
@app.route("/hello/<name>")
def hello(name):
    return render_template("hello.html", name=name)
```

### 2.3 Blueprint 模块化

```python
# auth/routes.py
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    return {"message": "Login endpoint"}

@auth_bp.route("/logout")
def logout():
    return {"message": "Logout endpoint"}

# user/routes.py
user_bp = Blueprint("user", __name__, url_prefix="/api/users")

@user_bp.route("/")
def list_users():
    return {"users": []}

@user_bp.route("/<int:user_id>")
def get_user(user_id):
    return {"id": user_id, "name": f"User {user_id}"}

# app.py - 注册蓝图
from flask import Flask
from auth.routes import auth_bp
from user.routes import user_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
```

### 2.4 Flask 扩展

```python
# Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

# Flask-Migrate
from flask_migrate import Migrate
migrate = Migrate(app, db)

# Flask-Login
from flask_login import LoginManager, UserMixin, login_user, logout_user

login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Flask-WTF 表单
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
```

### 2.5 错误处理与中间件

```python
from flask import jsonify

# 错误处理器
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# 自定义中间件
@app.before_request
def before_request():
    # 请求前执行
    pass

@app.after_request
def after_request(response):
    # 请求后执行
    response.headers["X-Custom"] = "value"
    return response

@app.teardown_request
def teardown(exception):
    # 请求结束时执行
    pass
```

### 2.6 Flask-RESTful API

```bash
pip install flask-restful
```

```python
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# 定义资源
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            return {"id": user_id, "name": f"User {user_id}"}
        return {"users": [{"id": 1}, {"id": 2}]}
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("email", type=str, required=True)
        args = parser.parse_args()
        return {"message": "User created", "data": args}, 201
    
    def put(self, user_id):
        return {"message": f"User {user_id} updated"}
    
    def delete(self, user_id):
        return {"message": f"User {user_id} deleted"}

# 注册路由
api.add_resource(UserResource, "/api/users", "/api/users/<int:user_id>")
```

---

## 3. Django 全栈框架

### 3.1 项目结构

```bash
# 安装 Django
pip install django

# 创建项目
django-admin startproject myproject
cd myproject

# 创建应用
python manage.py startapp blog

# 项目结构
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py      # 配置
│   ├── urls.py          # 路由
│   ├── wsgi.py          # WSGI 入口
│   └── asgi.py          # ASGI 入口
├── blog/
│   ├── __init__.py
│   ├── models.py        # 数据模型
│   ├── views.py         # 视图
│   ├── urls.py          # 应用路由
│   ├── admin.py         # 管理后台
│   └── apps.py
└── templates/
```

### 3.2 配置

```python
# settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]

# 应用
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
]

# 中间件
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# 数据库
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 模板
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 静态文件
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# 媒体文件
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# 国际化
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True
```

### 3.3 模型

```python
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# 自定义用户模型
class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 文章模型
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "草稿"),
        ("published", "已发布"),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=500, blank=True)
    featured_image = models.ImageField(upload_to="posts/", blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField("Tag", blank=True, related_name="posts")
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
```

### 3.4 视图

```python
# views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import Post, Category

# 函数视图
def post_list(request):
    posts = Post.objects.filter(status="published")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/post_list.html", {"page_obj": page_obj})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    post.views += 1
    post.save(update_fields=["views"])
    return render(request, "blog/post_detail.html", {"post": post})

# 类视图
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(status="published")

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "category", "content", "excerpt", "featured_image", "status", "tags"]
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "category", "content", "excerpt", "featured_image", "status", "tags"]
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
```

### 3.5 URLs

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

```python
# blog/urls.py
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/create/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
]
```

### 3.6 Admin 后台

```python
# admin.py
from django.contrib import admin
from .models import Post, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "status", "created_at", "views"]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    date_hierarchy = "created_at"
    
    fieldsets = (
        ("基本信息", {
            "fields": ("title", "slug", "author")
        }),
        ("内容", {
            "fields": ("content", "excerpt", "featured_image")
        }),
        ("分类与标签", {
            "fields": ("category", "tags")
        }),
        ("发布", {
            "fields": ("status",)
        }),
    )
```

### 3.7 DRF (Django REST Framework)

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    "rest_framework",
]

# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Category, Tag

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "avatar", "bio"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source="category", 
        write_only=True
    )
    
    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "author", "category", "category_id",
            "content", "excerpt", "featured_image", "status",
            "views", "created_at", "updated_at", "tags"
        ]
        read_only_fields = ["views", "created_at", "updated_at"]

# views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status="published")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=["post"])
    def increment_views(self, request, slug=None):
        post = self.get_object()
        post.views += 1
        post.save(update_fields=["views"])
        return Response({"views": post.views})

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

---

## 4. FastAPI 现代高性能框架

### 4.1 快速开始

```bash
# 安装
pip install fastapi uvicorn
```

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI(
    title="My API",
    description="API 文档",
    version="1.0.0"
)

# 数据模型
class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int
    created_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 模拟数据库
users_db = []
posts_db = []

# 路由
@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/users", response_model=List[User])
def list_users(skip: int = 0, limit: int = 10):
    return users_db[skip : skip + limit]

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate):
    new_user = User(
        id=len(users_db),
        **user.model_dump(),
        created_at=datetime.now(),
        is_active=True
    )
    users_db.append(new_user)
    return new_user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = User(
        id=user_id,
        **user.model_dump(),
        created_at=users_db[user_id].created_at,
        is_active=True
    )
    users_db[user_id] = updated_user
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db.pop(user_id)
    return {"message": "User deleted"}

# 启动服务器
# uvicorn main:app --reload --port 8000
```

### 4.2 依赖注入

```python
from fastapi import Depends, Header, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta
import jwt

# 模拟数据库依赖
def get_db():
    db = []  # 模拟数据库连接
    try:
        yield db
    finally:
        pass  # 清理资源

# 缓存依赖
def get_cache():
    cache = {}
    yield cache
    # 清理

# 认证依赖
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload["sub"]
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# 可选认证
def get_current_user_optional(authorization: Optional[str] = Header(None)):
    if not authorization:
        return None
    # ... 解析 token
    return "user"

# 使用依赖
@app.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    return {"message": f"Hello, {user}"}

@app.get("/items")
def list_items(
    db = Depends(get_db),
    cache = Depends(get_cache),
    current_user: Optional[str] = Depends(get_current_user_optional)
):
    return {"items": [], "user": current_user}
```

### 4.3 请求体验证

```python
from pydantic import BaseModel, Field, validator, constr
from typing import Optional, List
from enum import Enum

# 枚举
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

# 嵌套模型
class Address(BaseModel):
    street: str
    city: str
    country: str = "China"
    zip_code: str

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    age: Optional[int] = Field(None, ge=0, le=150)
    role: UserRole = UserRole.USER
    addresses: List[Address] = []
    
    # 自定义验证
    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v
    
    @validator("email")
    def email_lowercase(cls, v):
        return v.lower()

# 创建示例
user = User(
    username="alice",
    email="ALICE@EXAMPLE.COM",
    age=25,
    role="user",
    addresses=[Address(street="123 Main St", city="Beijing")]
)
print(user.email)  # alice@example.com（自动转小写）
```

### 4.4 中间件

```python
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time

app = FastAPI()

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip 压缩
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 自定义中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 请求拦截
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response: {response.status_code}")
    return response
```

### 4.5 数据库集成

```python
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from datetime import datetime

# SQLAlchemy 设置
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# 依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 路由
@app.get("/users", response_model=List[dict])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {"id": u.id, "name": u.name, "email": u.email, "created_at": u.created_at}
        for u in users
    ]
```

### 4.6 WebSocket

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# WebSocket 连接管理器
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({
                "type": "message",
                "data": data
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({
            "type": "disconnect",
            "message": "Client disconnected"
        })
```

### 4.7 后台任务

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    # 立即返回
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification scheduled"}

# 延迟响应
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio

@app.get("/long-operation")
async def long_operation():
    await asyncio.sleep(5)  # 模拟耗时操作
    return {"message": "Operation completed"}
```

---

## 5. 框架对比与选型

### 5.1 核心对比

| 特性 | Flask | Django | FastAPI |
|------|-------|--------|---------|
| 定位 | 微框架 | 全栈框架 | 现代 API 框架 |
| 学习曲线 | 低 | 中 | 低 |
| 灵活性 | 高 | 低 | 高 |
| ORM | SQLAlchemy（可选） | Django ORM（内置） | SQLAlchemy（推荐） |
| 管理后台 | 扩展 | 内置 | 扩展 |
| 异步支持 | 扩展 | 扩展 | 原生 |
| 自动文档 | 扩展 | 可选 | 原生 |
| 性能 | 中 | 中 | 高 |
| 适用场景 | 小型项目、API | 大型全栈项目 | 高性能 API、微服务 |

### 5.2 选型建议

```python
# 选择 Flask 如果：
# - 需要完全控制应用结构
# - 构建小型到中型应用
# - 快速原型开发
# - 简单的 REST API

# 选择 Django 如果：
# - 构建大型全栈应用
# - 需要内置管理后台
# - 需要完整的认证系统
# - 团队有 Django 经验

# 选择 FastAPI 如果：
# - 构建高性能 REST/gRPC API
# - 需要自动生成 API 文档
# - 需要异步支持
# - 构建微服务架构
```

---

## 6. RESTful API 设计

### 6.1 最佳实践

```python
# 资源命名 - 使用名词复数
# ✅ GET /users
# ✅ GET /users/123/posts
# ❌ GET /getUsers
# ❌ GET /getUserPosts

# HTTP 方法正确使用
# GET - 读取资源
# POST - 创建资源
# PUT - 完整更新（替换）
# PATCH - 部分更新
# DELETE - 删除资源

# 状态码
# 200 OK - 成功
# 201 Created - 创建成功
# 204 No Content - 删除成功
# 400 Bad Request - 客户端错误
# 401 Unauthorized - 未认证
# 403 Forbidden - 无权限
# 404 Not Found - 资源不存在
# 500 Server Error - 服务器错误

# 错误响应格式
{
    "error": {
        "code": "USER_NOT_FOUND",
        "message": "User with id 123 not found",
        "details": {}
    }
}

# 成功响应格式
{
    "data": {
        "id": 123,
        "name": "Alice"
    },
    "meta": {
        "page": 1,
        "total": 100
    }
}

# 分页
GET /users?page=1&limit=20

# 过滤
GET /users?status=active&role=admin

# 排序
GET /users?sort=-created_at,name

# 字段选择
GET /users?fields=id,name,email
```

### 6.2 版本控制

```python
# URL 版本（推荐）
# GET /api/v1/users
# GET /api/v2/users

# 请求头版本
# Accept: application/vnd.myapp.v1+json

# 响应头版本
# Content-Version: v1
```

---

## 7. 认证与授权

### 7.1 JWT 认证

```python
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

security = HTTPBearer()

@app.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    return {"user": payload["sub"]}
```

### 7.2 OAuth 2.0

```python
# 使用 python-jose 和 httpx
from fastapi import OAuth2PasswordBearer, Depends
from fastapi.security import OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 验证用户名密码
    user = verify_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

---

## 8. 部署与运维

### 8.1 Gunicorn + Nginx

```bash
# 安装
pip install gunicorn

# 启动
gunicorn -w 4 -b 127.0.0.1:8000 main:app
gunicorn -w 4 -b 127.0.0.1:8000 main:app --worker-class=gevent
```

```nginx
# nginx 配置
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static {
        alias /var/www/static;
    }
    
    location /media {
        alias /var/www/media;
    }
}
```

### 8.2 Uvicorn

```bash
# 直接运行
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# 使用配置文件
# uvicorn.yaml
```

### 8.3 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb

  redis:
    image: redis:7
```

---

## 9. 实战示例

### 9.1 FastAPI 完整项目结构

```
myapi/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── auth.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── utils/
│       ├── __init__.py
│       └── security.py
├── tests/
├── requirements.txt
├── pyproject.toml
└── .env
```

### 9.2 完整示例代码

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, auth
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

---

## 下一步学习

完成本篇学习后，建议继续学习：

1. **Python 最佳实践** - 代码规范、性能优化、安全
2. **实战项目** - 将知识应用于实际项目

---

*持续更新中……*