# DOCX to Markdown Converter - Chrome Extension

一个用于将 Word 文档（.docx/.doc）转换为 Markdown 格式的 Chrome 浏览器插件。支持提取图片、批量转换、自动转换旧版 .doc 文件等功能。

## ✨ 功能特性

- 📄 **单文件转换** - 选择单个或多个 DOCX/DOC 文件进行转换
- 📁 **文件夹批量转换** - 选择文件夹，自动转换其中所有 Word 文档
- 🖼️ **图片提取** - 自动提取文档中的图片并保存到 media 文件夹
- 🔄 **自动转换 .doc** - 可选自动将旧版 .doc 文件转换为 .docx（需要 LibreOffice）
- 📊 **实时进度** - 显示转换进度和详细结果
- ⚙️ **自定义输出** - 可指定输出路径
- 🎨 **精美界面** - 现代化的用户界面设计

## 📋 系统要求

- Python 3.7+
- Google Chrome 浏览器
- 依赖包：
  - `python-docx`
  - （可选）LibreOffice - 用于转换 .doc 文件

## 🚀 安装步骤

### 1. 安装 Python 依赖

```bash
pip install python-docx
```

### 2. 安装 Chrome 插件

1. 打开 Chrome 浏览器，访问 `chrome://extensions/`
2. 开启右上角的 **"开发者模式"**
3. 点击 **"加载已解压的扩展程序"**
4. 选择本项目的 `docx-to-md-extension` 文件夹
5. 插件安装完成，会在浏览器工具栏显示图标

### 3. 启动本地服务器

插件需要配合本地 Python 服务器使用。在终端中运行：

```bash
cd /path/to/docx-to-md-extension
python3 server.py
```

或指定端口：

```bash
python3 server.py --port 8765
```

服务器启动后会显示：

```
╔══════════════════════════════════════════════════════════════╗
║  DOCX to Markdown Converter Server                          ║
║  Server running at: http://localhost:8765                   ║
║  Press Ctrl+C to stop                                        ║
╚══════════════════════════════════════════════════════════════╝
```

## 📖 使用说明

### 基本使用流程

1. **启动服务器**
   ```bash
   python3 server.py
   ```

2. **打开插件**
   - 点击浏览器工具栏的插件图标
   - 确认服务器状态显示为 🟢 "服务器已连接"

3. **选择文件**
   - **单文件/多文件**: 点击 "选择 DOCX 文件"，可以按住 Ctrl/Cmd 多选
   - **文件夹**: 点击 "选择文件夹"，自动扫描其中的 Word 文档

4. **配置选项**
   - ✅ **提取图片到 media 文件夹** - 自动提取文档中的图片
   - ☐ **自动转换 .doc 文件** - 需要安装 LibreOffice
   - **输出路径** - 留空则保存到源文件同目录

5. **开始转换**
   - 点击 "开始转换" 按钮
   - 查看实时进度和转换结果

### 输出格式

转换后会生成：

```
your-document.md          # Markdown 文件
media/                    # 图片文件夹（如果启用图片提取）
  ├── 17641588732171.png
  ├── 17641588732175.png
  └── ...
```

## 🎯 功能说明

### 图片处理

- 自动提取 Word 文档中的所有图片
- 支持现代格式（DrawingML）和旧版格式（VML）
- 图片按时间戳命名，避免冲突
- 在 Markdown 中自动插入图片引用：`![](media/xxxxx.png)`

### 目录过滤

- 自动过滤 Word 文档中的目录（TOC）字段
- 跳过空标题和只包含空白字符的标题

### 格式支持

- ✅ 标题（H1-H6）
- ✅ 粗体、斜体、删除线
- ✅ 列表（有序、无序）
- ✅ 表格
- ✅ 图片
- ✅ 代码（等宽字体）

## 🛠️ 高级配置

### 自定义服务器地址

如果需要更改服务器端口或地址，修改以下文件：

**插件端** (`js/popup.js`):
```javascript
const SERVER_URL = 'http://localhost:8765';
```

**服务器端**:
```bash
python3 server.py --host localhost --port 8765
```

### LibreOffice 配置

如果需要自动转换 .doc 文件，请安装 LibreOffice：

**macOS**:
```bash
brew install --cask libreoffice
```

**Ubuntu/Debian**:
```bash
sudo apt-get install libreoffice
```

**Windows**:
从 [LibreOffice 官网](https://www.libreoffice.org/download/) 下载安装

## 📁 项目结构

```
docx-to-md-extension/
├── manifest.json          # Chrome 插件配置
├── popup.html            # 插件界面 HTML
├── server.py             # Python HTTP 服务器
├── README.md             # 说明文档
├── css/
│   └── style.css        # 样式文件
├── js/
│   └── popup.js         # 插件逻辑
└── icons/
    ├── icon16.png       # 16x16 图标
    ├── icon48.png       # 48x48 图标
    └── icon128.png      # 128x128 图标
```

## 🐛 故障排除

### 常见问题

**问题 1**: 插件显示 🔴 "服务器未运行"
- 确认 Python 服务器正在运行: `./start_server.sh`
- 检查端口 8765 是否被占用
- 尝试重启服务器

**问题 2**: 选择文件夹后转换报错 500
- 查看服务器终端的详细错误日志
- 尝试指定输出路径
- 检查文件名是否包含特殊字符
- 使用测试脚本: `python3 test_server.py /path/to/file.docx`

**问题 3**: 文件转换失败
- **文件损坏** - 用 Word 打开检查
- **缺少依赖** - 确认已安装 `python-docx`
- **文件格式** - 确认是 .docx 格式（不是 .doc）
- **路径权限** - 确认输出路径有写入权限

**问题 4**: .doc 文件无法转换
- 安装 LibreOffice: `brew install --cask libreoffice`
- 在插件中勾选 "自动转换 .doc 文件"
- 或手动用 Word 转换为 .docx 格式

**更多问题和详细解决方案**: 请查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 🔒 安全说明

- 本插件所有处理都在本地完成
- 不会上传任何文件到云端
- Python 服务器仅监听本地地址（localhost）
- 转换后的临时文件会自动清理

## 📝 更新日志

### v1.0.0 (2025-01-26)
- ✨ 初始版本发布
- 📄 支持 DOCX/DOC 转 Markdown
- 🖼️ 图片自动提取
- 📁 批量转换功能
- 🎨 现代化界面设计

## 📄 许可证

本项目基于原 `md_trans.py` 转换脚本开发。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请提交 GitHub Issue。

---

**Enjoy converting! 📝✨**

## 🌟 Star History

如果这个项目对你有帮助，欢迎 Star ⭐️

