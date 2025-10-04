# 招聘信息管理系统

一个基于Vue.js和Django的招聘信息管理系统，用于展示和筛选招聘数据。

## 技术栈

### 前端
- Vue 3
- Vite
- Axios
- CSS3

### 后端
- Python 3
- Django
- Django REST Framework
- MySQL

## 功能特性

1. **招聘信息列表展示**：展示职位名称、公司名称、薪资、工作地点等信息
2. **多条件搜索**：支持按职位名称、公司名称、工作地点、技能标签等进行搜索
3. **分页功能**：支持分页浏览大量招聘数据
4. **响应式设计**：适配不同屏幕尺寸

## 项目结构

```
data_analysis_system/
├── frontend/            # Vue前端项目
│   ├── src/             # 前端源码
│   ├── public/          # 静态资源
│   └── package.json     # 前端依赖
└── recruitment_system/  # Django后端项目
    ├── job_app/         # 招聘应用
    └── recruitment_system/ # 项目配置
```

## 安装与运行

### 前提条件

- Python 3.8+ 
- Node.js 14+ 
- MySQL 5.7+（需创建recruitment数据库）

### 后端安装与运行

1. 进入后端项目目录
```bash
cd recruitment_system
```

2. 安装Python依赖
```bash
pip install django mysql-connector-python djangorestframework django-cors-headers
```

3. 配置数据库连接
修改`recruitment_system/settings.py`中的数据库配置，确保与您的MySQL配置一致：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'recruitment',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

4. 运行Django开发服务器
```bash
python manage.py runserver
```
后端服务将运行在 http://localhost:8000/

### 前端安装与运行

1. 进入前端项目目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 运行开发服务器
```bash
npm run dev
```
前端服务将运行在 http://localhost:5173/

## API接口说明

- **获取招聘列表**：GET /api/job_postings/
  - 参数：job_title（职位名称）、company_name（公司名称）、location（地点）、skills（技能）
  - 返回：招聘信息列表

## 注意事项

1. 确保MySQL服务已启动，并且已创建recruitment数据库
2. 确保job_postings表已存在于recruitment数据库中
3. 如有跨域问题，请检查Django的CORS配置
4. 开发环境下使用的是Django和Vue的开发服务器，生产环境请使用合适的部署方案