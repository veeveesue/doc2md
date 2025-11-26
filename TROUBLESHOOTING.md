# 🔧 故障排除指南

## 常见问题与解决方案

### 问题 1: 选择文件夹后转换报错 500

**错误信息**:
```
[26/Nov/2025 20:41:11] "POST /convert HTTP/1.1" 500 -
```

**可能原因**:
1. 文件路径包含特殊字符或非 ASCII 字符
2. 文件权限问题
3. 临时目录创建失败
4. 输出路径不存在或无权限

**解决方案**:

#### 方案 1: 查看详细错误日志
服务器终端会显示详细的错误堆栈，查看具体错误信息：

```bash
# 重启服务器并查看日志
./start_server.sh
```

错误信息示例：
```
Error converting file: Traceback (most recent call last):
  File "/path/to/server.py", line 142, in handle_convert
    markdown = converter.convert_file(temp_file, output_file)
  ...
```

#### 方案 2: 检查文件名
文件名不应包含特殊字符：
- ❌ 避免: `文件名 (1).docx`（括号可能有问题）
- ❌ 避免: `file[test].docx`（方括号）
- ✅ 推荐: `file_test.docx` 或 `文件名-1.docx`

#### 方案 3: 使用绝对路径作为输出
如果选择文件夹时出错，尝试指定一个明确的输出路径：

```
输出路径: /Users/vee/Downloads/output
```

#### 方案 4: 单个文件测试
先尝试转换单个文件，确认服务器工作正常：

1. 不选择文件夹
2. 点击"选择 DOCX 文件"
3. 选择单个文件测试

#### 方案 5: 测试服务器
使用测试脚本验证服务器：

```bash
cd /Users/vee/project/docx-to-md-extension
python3 test_server.py /Users/vee/Downloads/test.docx
```

### 问题 2: 服务器无法连接

**错误信息**:
```
🔴 服务器未运行 - 请先启动服务器
```

**解决方案**:

```bash
# 1. 检查服务器是否运行
lsof -i :8765

# 2. 如果没有运行，启动服务器
cd /Users/vee/project/docx-to-md-extension
./start_server.sh

# 3. 如果端口被占用，使用其他端口
python3 server.py --port 8766
```

然后更新插件中的服务器地址（`js/popup.js`）：
```javascript
const SERVER_URL = 'http://localhost:8766';
```

### 问题 3: 图片提取失败

**错误信息**:
```
✓ file.docx → file.md
  ✓ Extracted 0 images
```

**可能原因**:
1. 文档中没有图片
2. 图片格式不支持
3. media 文件夹权限问题

**解决方案**:

#### 检查原文档
用 Word 打开文档，确认是否真的有图片

#### 检查 media 文件夹
```bash
# 查看 media 文件夹是否创建
ls -la /path/to/output/media/

# 检查权限
chmod -R 755 /path/to/output/
```

#### 查看转换后的 Markdown
```bash
cat output.md | grep "!\[\]"
```

如果有 `![](media/xxx.png)` 但 media 文件夹为空，说明图片提取有问题。

### 问题 4: 文件转换后乱码

**症状**:
- Markdown 文件中文显示为乱码
- 特殊字符变成问号

**解决方案**:

#### 检查文件编码
```bash
file -I output.md
```

应该显示 `charset=utf-8`

#### 使用正确的文本编辑器
- ✅ VSCode
- ✅ Sublime Text
- ✅ Typora
- ❌ 记事本（Windows，可能不支持 UTF-8）

### 问题 5: .doc 文件转换失败

**错误信息**:
```
✗ old-file.doc: 不支持旧版 .doc 格式
```

**解决方案**:

#### 方案 1: 安装 LibreOffice
```bash
# macOS
brew install --cask libreoffice

# Ubuntu/Debian
sudo apt-get install libreoffice
```

然后勾选插件中的 "自动转换 .doc 文件"

#### 方案 2: 手动转换
1. 用 Word 打开 .doc 文件
2. 另存为 .docx 格式
3. 转换 .docx 文件

### 问题 6: 输出路径无效

**错误信息**:
```
✗ file.docx: Permission denied: /path/to/output/
```

**解决方案**:

```bash
# 1. 检查路径是否存在
ls -la /path/to/output/

# 2. 创建目录
mkdir -p /path/to/output/

# 3. 设置权限
chmod 755 /path/to/output/

# 4. 或留空输出路径，使用默认位置
```

### 问题 7: 批量转换中断

**症状**:
- 转换 10 个文件，只成功了 3 个就停止了
- 进度条卡住不动

**解决方案**:

#### 检查失败的文件
查看结果列表中哪个文件出错：
```
✓ file1.docx → file1.md
✓ file2.docx → file2.md
✓ file3.docx → file3.md
✗ file4.docx: BadZipFile: File is not a zip file
```

#### 跳过问题文件
移除或修复 `file4.docx`，然后重新批量转换

#### 分批转换
如果文件很多，分批转换：
- 第 1-5 个文件
- 第 6-10 个文件
- ...

### 问题 8: 转换速度很慢

**症状**:
- 单个小文件转换需要 10+ 秒
- 大文件转换超过 1 分钟

**解决方案**:

#### 检查文件大小
```bash
ls -lh file.docx
```

如果文件很大（> 5MB），慢是正常的

#### 检查图片数量
图片多会影响速度，可以临时关闭图片提取测试

#### 检查系统资源
```bash
# 查看 CPU 和内存使用
top
```

#### 重启服务器
```bash
# Ctrl+C 停止服务器
# 重新启动
./start_server.sh
```

## 调试技巧

### 启用详细日志

修改 `server.py`，在错误处理中添加：

```python
except Exception as e:
    import traceback
    error_detail = traceback.format_exc()
    print(f"Error detail:\n{error_detail}")  # 已添加
    ...
```

### 测试单个文件

使用命令行直接测试：

```bash
cd /Users/vee/project/anylisppt
python3 -c "
from md_trans import DocxToMarkdown
converter = DocxToMarkdown()
converter.convert_file('/path/to/test.docx', '/path/to/output.md')
"
```

### 检查浏览器控制台

1. 打开 Chrome DevTools (F12)
2. 切换到 Console 标签
3. 查看是否有 JavaScript 错误

### 使用测试脚本

```bash
python3 test_server.py /path/to/test.docx
```

## 获取帮助

如果以上方法都无法解决问题：

1. **收集信息**:
   - Python 版本: `python3 --version`
   - python-docx 版本: `pip3 show python-docx`
   - 操作系统版本
   - 完整错误信息（服务器终端输出）

2. **查看日志**:
   - 服务器终端的完整输出
   - 浏览器控制台的错误信息

3. **简化问题**:
   - 使用最小的测试文件（只包含文本，无图片）
   - 单个文件测试
   - 默认选项（不改变任何设置）

4. **提交 Issue**:
   - 包含上述所有信息
   - 提供可复现的步骤

---

**大多数问题都可以通过查看服务器日志来诊断** 📝
