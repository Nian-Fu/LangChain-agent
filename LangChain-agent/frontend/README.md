# 前端使用说明

## 📁 文件说明

```
frontend/
├── index.html      # 主页面
├── styles.css      # 样式文件
├── app.js          # JavaScript逻辑
└── README.md       # 本文档
```

## 🚀 快速启动

### 方法1: 使用Python HTTP服务器（推荐）

```bash
# 在frontend目录下运行
cd frontend
python -m http.server 8080

# 或使用 Python 3
python3 -m http.server 8080
```

然后在浏览器访问: `http://localhost:8080`

### 方法2: 使用Node.js HTTP服务器

```bash
# 安装 http-server
npm install -g http-server

# 在frontend目录下运行
cd frontend
http-server -p 8080
```

### 方法3: 直接打开HTML文件

直接双击 `index.html` 文件，但可能会遇到CORS问题。

### 方法4: 使用VS Code Live Server

1. 安装 Live Server 扩展
2. 右键点击 `index.html`
3. 选择 "Open with Live Server"

## ⚙️ 配置

### 修改API地址

如果后端服务不是运行在 `http://localhost:8000`，需要修改 `app.js` 中的配置：

```javascript
// 在 app.js 顶部修改
const API_BASE_URL = 'http://your-api-address:port';
```

### 启用CORS（如果需要）

如果遇到CORS错误，确保后端已正确配置CORS。后端已配置允许所有来源：

```python
# main.py 中已配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🎨 功能说明

### 1. 智能助手
- 自然语言对话
- 快捷操作按钮
- 历史记录查看
- 实时响应

### 2. 机票查询
- 出发地/目的地选择
- 日期选择
- 乘客数量
- 智能建议

### 3. 酒店查询
- 目的地选择
- 预算设置
- 偏好多选
- 评分排序

### 4. 景点推荐
- 目的地输入
- 旅行天数
- 兴趣偏好
- 个性化推荐

### 5. 关于页面
- 系统介绍
- 功能说明
- API状态检查

## 🎯 使用流程

### 完整流程

1. **启动后端服务**
   ```bash
   cd /Users/funian/PycharmProjects/LangChain-agent
   python main.py
   ```

2. **启动前端服务**
   ```bash
   cd frontend
   python -m http.server 8080
   ```

3. **访问前端**
   - 打开浏览器
   - 访问 `http://localhost:8080`

4. **开始使用**
   - 选择功能标签
   - 输入查询条件
   - 获取智能推荐

## 🔍 故障排除

### 问题1: 无法连接到API

**症状**: 页面显示"API服务未连接"

**解决方案**:
1. 确认后端服务已启动
2. 检查API地址配置
3. 查看浏览器控制台错误信息

### 问题2: CORS错误

**症状**: 浏览器控制台显示CORS错误

**解决方案**:
1. 确认后端CORS配置正确
2. 使用HTTP服务器运行前端，不要直接打开HTML文件
3. 检查API地址是否正确

### 问题3: 样式不显示

**症状**: 页面显示但没有样式

**解决方案**:
1. 确认 `styles.css` 文件存在
2. 检查浏览器控制台是否有加载错误
3. 清除浏览器缓存

### 问题4: JavaScript不工作

**症状**: 按钮点击无响应

**解决方案**:
1. 检查浏览器控制台错误
2. 确认 `app.js` 文件存在
3. 检查API地址配置

## 💡 开发提示

### 修改样式

编辑 `styles.css` 文件：

```css
/* 修改主题色 */
:root {
    --primary-color: #your-color;
}
```

### 添加新功能

在 `app.js` 中添加新的函数和事件监听器。

### 调试技巧

1. 打开浏览器开发者工具 (F12)
2. 查看 Console 标签的错误信息
3. 查看 Network 标签的网络请求

## 📱 响应式设计

前端已适配移动设备：
- 自动调整布局
- 触摸友好
- 优化的移动体验

## 🎨 界面特性

- ✅ 现代化设计
- ✅ 流畅动画
- ✅ 直观操作
- ✅ 实时反馈
- ✅ 加载提示
- ✅ 错误处理

## 🔐 安全建议

### 生产环境部署

1. **使用HTTPS**
   ```
   确保前后端都使用HTTPS
   ```

2. **限制CORS**
   ```python
   # 后端只允许特定域名
   allow_origins=["https://yourdomain.com"]
   ```

3. **添加认证**
   ```javascript
   // 在API请求中添加认证token
   headers: {
       'Authorization': 'Bearer ' + token
   }
   ```

## 📊 性能优化

### 建议的优化

1. **压缩资源**
   - 压缩CSS和JavaScript
   - 使用CDN加载第三方库

2. **缓存策略**
   - 设置适当的缓存headers
   - 使用Service Worker

3. **延迟加载**
   - 图片懒加载
   - 按需加载组件

## 🌐 浏览器兼容性

支持的浏览器：
- ✅ Chrome (推荐)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ⚠️ IE 11 (部分功能可能不支持)

## 📞 获取帮助

遇到问题？
1. 查看浏览器控制台
2. 检查后端日志
3. 阅读主项目README
4. 提交GitHub Issue

## 🎉 开始使用

现在你可以：
1. 启动后端服务
2. 启动前端服务
3. 在浏览器中打开
4. 开始体验智能旅行助手！

祝使用愉快！ ✈️

