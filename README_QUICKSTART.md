# Paperang 喵喵机 - 快速开始指南

## 🚀 一键安装与启动

### 第一步：运行自动配置脚本

```bash
python setup_env.py
```

这个脚本会自动完成以下操作：
1. ✅ 检查 Python 版本 (需要 3.7+)
2. ✅ 检测 Tkinter 支持 (GUI 必需)
3. ✅ 创建虚拟环境 (`.venv` 目录)
4. ✅ 安装所有依赖 (pyserial, pillow, numpy, qrcode)
5. ✅ 创建快捷启动脚本 (`start.sh` 或 `start.bat`)

### 第二步：启动应用

配置完成后，使用生成的启动脚本：

**MacOS / Linux:**
```bash
./start.sh            # 启动 GUI 界面
./start.sh --cli      # 命令行交互模式
./start.sh text "Hello"   # 直接打印文字
./start.sh image photo.jpg  # 直接打印图片
```

**Windows:**
```bat
start.bat             # 启动 GUI 界面
start.bat --cli       # 命令行交互模式
start.bat text "Hello"    # 直接打印文字
```

## 📋 手动安装 (可选)

如果不想使用自动脚本，可以手动操作：

### 1. 创建虚拟环境
```bash
python -m venv .venv
```

### 2. 激活虚拟环境
**MacOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bat
.venv\Scripts\activate
```

### 3. 安装依赖
```bash
pip install pyserial pillow numpy qrcode[pil]
```

### 4. 运行程序
```bash
python run_paperang.py
```

## 🔧 MacOS 特别说明

### 安装 Tkinter
如果使用 Homebrew 安装的 Python:
```bash
brew install python-tk
```

如果使用官方安装包，Tkinter 应该已包含在内。

### 蓝牙权限
1. 打开 **系统设置** → **隐私与安全性** → **蓝牙**
2. 确保你的终端应用 (Terminal, iTerm2, VSCode 等) 已勾选

### 设备配对
1. 打开喵喵机电源
2. 在 **系统设置** → **蓝牙** 中找到 "Paperang" 或类似设备
3. 点击配对

## 📱 使用方式

### GUI 界面 (推荐新手)
- 自动发现并连接设备
- 可视化打印预览
- 支持文字、图片、二维码
- 实时日志显示

### 命令行模式
```bash
# 扫描设备
python run_paperang.py scan

# 打印文字
python run_paperang.py text "你好，世界！"

# 打印图片
python run_paperang.py image test.png

# 打印二维码
python run_paperang.py qrcode "https://example.com"

# 走纸
python run_paperang.py feed

# 自检页
python run_paperang.py selftest
```

### API 调用 (开发者)
```python
from paperang.gui import PaperangPrinter

printer = PaperangPrinter()
printer.auto_connect()

# 打印文字
printer.print_text("Hello World", font_size=24)

# 打印图片
printer.print_image("photo.jpg", dither_mode="floyd")

# 打印二维码
printer.print_qrcode("https://example.com")

# 走纸
printer.feed_paper(50)
```

## ❓ 常见问题

### Q: 找不到设备？
A: 
1. 确认喵喵机已开机
2. 在系统蓝牙设置中确认已配对
3. 重启蓝牙服务
4. 靠近设备重新扫描

### Q: Tkinter 导入错误？
A: 
- **MacOS**: `brew install python-tk`
- **Ubuntu**: `sudo apt-get install python3-tk`
- **Windows**: 重新安装 Python，勾选 tcl/tk 选项

### Q: 打印内容模糊？
A:
1. 尝试调整二值化模式 (floyd / adaptive)
2. 确保图片清晰度足够
3. 检查打印机头是否清洁

### Q: 虚拟环境问题？
A:
删除 `.venv` 目录后重新运行 `python setup_env.py`

## 📂 项目结构

```
paperang/
├── setup_env.py          # 自动配置脚本 ⭐
├── run_paperang.py       # 主启动入口
├── start.sh / start.bat  # 快捷启动脚本 (自动生成)
├── .venv/                # 虚拟环境 (自动生成)
├── paperang/
│   ├── __init__.py
│   ├── const.py          # 协议常量
│   ├── bt.py             # 蓝牙通信
│   ├── image.py          # 图像处理
│   ├── text.py           # 文字渲染
│   ├── mac_auto_print.py # MacOS 自动连接
│   └── gui.py            # GUI 界面
├── README.md             # 项目说明
├── README_GUI.md         # GUI 详细文档
└── README_QUICKSTART.md  # 本文件
```

## 🎯 下一步

- 查看 `README_GUI.md` 了解 GUI 详细功能
- 查看 `paperang/mac_auto_print.py` 了解命令行参数
- 尝试打印你的第一张标签！

祝你使用愉快！🖨️✨
