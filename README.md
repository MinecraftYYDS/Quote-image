# 语录卡片生成器

在线语录卡片生成工具，纯浏览器端渲染，无需服务器处理。

## 功能

- **实时预览** — 所有修改即时反映到画布
- **头像获取** — 输入 QQ 号自动获取头像，或上传本地图片
- **文字自定义** — 语录内容、署名均可自定义文字内容、字号、颜色
- **字体选择** — 默认 TsukuA 字体，可切换系统字体或上传自定义字体（.ttf / .otf / .woff2）
- **一键导出** — 下载 PNG 或复制到剪贴板

## 部署到 Cloudflare Pages

### 方式一：Git 连接（推荐）

1. 将项目推送到 GitHub / GitLab
2. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Workers & Pages** → **Create**
3. 选择 **Pages** → 连接 Git 仓库
4. 构建设置：
   - **构建命令**：留空
   - **输出目录**：`.`（根目录）
5. 点击部署

### 方式二：Wrangler CLI 直接上传

```bash
npm install -g wrangler
wrangler login
wrangler pages deploy . --project-name=quote-image
```

> 部署完成后，`functions/api/avatar.js` 会自动作为 Pages Function 运行，提供 QQ 头像代理接口（解决跨域问题）。

## 本地预览

使用任意静态服务器即可预览（不含 QQ 头像代理功能）：

```bash
# Python
python -m http.server 8080

# Node.js
npx serve .
```

打开 `http://localhost:8080` 即可使用。本地模式下 QQ 头像功能可能因跨域受限，可直接上传图片。

## 项目结构

```
├── index.html              主页面（HTML + CSS + JS 单文件）
├── TsukuA.ttc              默认字体文件
├── functions/
│   └── api/
│       └── avatar.js       CF Pages Function — QQ 头像代理
└── README.md
```

## 技术栈

- 纯前端：HTML5 Canvas + Vanilla JS
- 部署平台：Cloudflare Pages + Pages Functions
- 无构建步骤、无依赖
