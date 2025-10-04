# 招聘信息管理系统 - 前端

基于Vue 3和Vite构建的前端应用，用于展示和筛选招聘数据。

## 技术栈

- Vue 3
- Vite
- Axios
- CSS3

## 功能特性

1. **招聘信息展示**：以卡片形式展示招聘信息，包括职位名称、公司名称、薪资、工作地点等
2. **多条件搜索**：支持按职位名称、公司名称、工作地点、技能标签进行搜索
3. **分页浏览**：支持分页功能，便于浏览大量数据
4. **响应式设计**：适配不同屏幕尺寸的设备

## 项目结构

```
frontend/
├── src/
│   ├── api/         # API服务文件
│   ├── components/  # Vue组件
│   ├── assets/      # 静态资源
│   ├── App.vue      # 根组件
│   ├── main.js      # 入口文件
│   └── style.css    # 全局样式
├── public/          # 静态资源目录
├── index.html       # HTML入口文件
├── package.json     # 项目依赖配置
└── vite.config.js   # Vite配置文件
```

## 安装与运行

### 前提条件

- Node.js 14+ 
- 确保后端服务已启动并运行在 http://localhost:8000/

### 安装依赖

```bash
npm install
```

### 开发模式运行

```bash
npm run dev
```
应用将运行在 http://localhost:5173/

### 构建生产版本

```bash
npm run build
```
构建后的文件将生成在`dist`目录中

## API接口调用

前端通过Axios调用后端API，API服务配置在`src/api/jobService.js`文件中：

- **getJobList(params)**：获取招聘信息列表，支持搜索参数
- **getJobDetail(id)**：获取单个招聘信息详情

## 组件说明

### JobList组件

主要功能：
- 展示招聘信息列表
- 提供搜索和筛选功能
- 支持分页浏览
- 显示职位名称、公司信息、薪资、工作地点、经验要求、学历要求、技能标签等

### 样式设计

- 使用CSS变量管理主题颜色
- 响应式布局，适配不同屏幕尺寸
- 卡片式设计，提供良好的视觉体验
- 悬停效果，提升交互体验

## 注意事项

1. 确保后端Django服务已启动
2. 如需修改API地址，请在`src/api/jobService.js`中更新baseURL
3. 开发环境使用Vite的热更新功能，提高开发效率
4. 生产环境建议使用Nginx等Web服务器部署构建后的静态文件
