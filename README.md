> 🤖 **AI assistants:** 请先阅读 [SKILL.md](SKILL.md) 了解如何与本项目交互。
> *AI assistants: read [SKILL.md](SKILL.md) first for instructions on using this project.*

# 🖨️ Paperang 2 喵喵机工具

[![License](https://img.shields.io/github/license/createskyblue/paperang-miaomiaoji-tool-gen2)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20MacOS%20%7C%20Linux-blue.svg)]()

> 基于 [ihciah/paperang-miaomiaoji-tool](https://github.com/ihciah/miaomiaoji-tool) 适配，专为 **喵喵机2代 (Paperang 2)** 优化的蓝牙打印工具。
> 支持 **命令行模式**（适合脚本/AI 调用）与 **交互式模式**（适合人工直接使用）。

A Python tool for controlling the **Paperang 2** portable Bluetooth thermal printer. Supports both a
**CLI mode** (for scripts / AI agents) and an **interactive mode** (for direct human use).

![实拍效果](img/PixPin_2026-07-06_22-24-31.jpg)

---

## ✨ 功能特性 / Features

- 🔤 **文本打印** — 支持中英文，可调字体大小（8–72pt），集成 MapleMono 等宽字体
- 🖼️ **图片打印** — 自动旋转、缩放至 576px 宽度，支持 Floyd-Steinberg 扩散二值化与自适应阈值两种模式
- 📱 **二维码打印** — 一键生成并打印二维码
- ⚙️ **设备控制** — 自检打印、走纸、浓度调节、自动关机时间设置
- 💻 **三模式** — GUI 图形界面 + `python -m paperang <command>` 命令行 + `python -m paperang interactive` 交互式
- 🍎 **跨平台** — 支持 Windows / MacOS / Linux，MacOS 自动蓝牙设备发现
- 🤖 **Claude Code Skill** — 附带 `SKILL.md`，可直接作为 `/paperang` skill 使用
- 🚀 **一键安装** — `python setup_env.py` 自动创建虚拟环境并安装所有依赖

---

## 📦 安装 / Installation

### 🚀 一键自动安装（推荐）

> **最简单的方式**：运行自动配置脚本，自动创建虚拟环境并安装所有依赖。

```bash
# 1. 克隆仓库
git clone https://github.com/createskyblue/paperang-miaomiaoji-tool-gen2.git
cd paperang-miaomiaoji-tool-gen2

# 2. 运行自动配置脚本
python setup_env.py
```

脚本会自动完成：
- ✅ 检查 Python 版本（需要 3.7+）
- ✅ 检测 Tkinter 支持（GUI 必需）
- ✅ 创建虚拟环境 (`.venv`)
- ✅ 安装所有依赖（pyserial, pillow, numpy, qrcode[pil]）
- ✅ 生成启动脚本（`start.sh` 或 `start.bat`）

完成后直接运行：
```bash
# MacOS/Linux
./start.sh

# Windows
.\start.bat
```

### 📋 手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/createskyblue/paperang-miaomiaoji-tool-gen2.git
cd paperang-miaomiaoji-tool-gen2

# 2. 使用 uv 安装依赖（推荐）
uv sync

# 或使用 pip
pip install -r requirements.txt

# 3. 启动 GUI
python run_paperang.py
```

> 💡 推荐使用 [uv](https://docs.astral.sh/uv/) 管理虚拟环境和依赖。首次使用需 `pip install uv`。
> 使用 uv 后，所有命令前加 `uv run`，如 `uv run python -m paperang config --list`。

---

## 🔧 系统依赖 / System Requirements

### MacOS
```bash
# 安装 tkinter（如果缺失）
brew install python-tk

# 蓝牙权限：系统设置 → 隐私与安全性 → 蓝牙 → 添加终端应用
```

### Ubuntu/Debian
```bash
sudo apt-get install python3-tk python3-venv
```

### Windows
- tkinter 通常随 Python 一起安装
- 确保安装 Python 时勾选了 "tcl/tk" 选项

---

## 🔵 Windows 蓝牙配置 / Bluetooth Setup

1. 开启电脑蓝牙，长按喵喵机电源键至指示灯闪烁
2. **设置** → **设备** → **蓝牙和其他设备** → 添加蓝牙设备 → 配对喵喵机
3. **设置** → **蓝牙和其他设备** → **更多蓝牙选项** → **COM 端口** 标签页 → 点击"添加" → 选择"传出（你的计算机启动连接）" → 浏览并选择名称含 **PAPERANG** 的设备 → 记下分配的 COM 端口号（如 `COM10`）
4. 配置工具：

```bash
python -m paperang config --list              # 列出可用串口
python -m paperang config --set-port COM10    # 设置端口（仅需一次）
```

![蓝牙设置步骤1](img/PixPin_2025-10-22_00-16-01.png)
![蓝牙设置步骤2](img/PixPin_2025-10-22_00-16-06.png)
![蓝牙设置步骤3](img/PixPin_2025-10-22_00-16-15.png)
![蓝牙设置步骤4](img/PixPin_2025-10-22_00-16-25.png)
![蓝牙设置步骤5](img/PixPin_2025-10-22_00-16-30.png)
![蓝牙设置步骤6](img/PixPin_2025-10-22_00-17-06.png)

---

## 🚀 使用方式 / Usage

### 🖥️ GUI 图形界面（推荐）

> **最简单的方式**：双击启动脚本，享受可视化操作体验。

```bash
# MacOS/Linux
./start.sh

# Windows
.\start.bat

# 或直接运行
python run_paperang.py
```

GUI 功能：
- 📝 文字打印（可调字体大小 8-72pt）
- 🖼️ 图片打印（带预览，支持 floyd/adaptive 模式）
- 📱 二维码打印
- ⚙️ 打印机控制（走纸、自检、电量查询）
- 🔍 自动设备发现与连接

### 💻 命令行模式 / CLI Mode

> 适合脚本、自动化、AI agent 调用。每个命令连接 → 打印 → 断开。

```bash
# 打印文字
python -m paperang text "你好，世界！"
python -m paperang text --font-size 48 "大标题"
python -m paperang text "Line1\nLine2"              # \n 换行

# 打印图片
python -m paperang image photo.jpg
python -m paperang image --mode adaptive drawing.png  # 文档/线条图推荐 adaptive

# 打印二维码
python -m paperang qrcode "https://github.com"

# 自检页
python -m paperang selftest

# 走纸
python -m paperang feed 100

# 查看/修改配置
python -m paperang config --list
python -m paperang config --set-port COM10
python -m paperang config                            # 查看当前配置
```

### 交互式模式 / Interactive Mode

> 适合人工直接使用，启动后可持续输入。

```bash
python -m paperang interactive
# 或直接运行:
python paperang/interactive.py
```

交互式模式下支持的指令：

| 指令 | 说明 |
|---|---|
| 直接输入文字 | 打印文字内容 |
| 输入图片路径 | 打印图片（支持 jpg/png/bmp/gif） |
| `/selftest` | 打印自检页 |
| `/fontsize 32` | 设置字体大小（8–72） |
| `/qrcode <内容>` | 生成并打印二维码 |
| `/imgmode floyd` | 图像模式：扩散二值化（照片推荐） |
| `/imgmode adaptive` | 图像模式：自适应阈值（文档推荐） |
| `/help` | 显示帮助 |
| 直接回车 | 走纸 25 单位 |

---

## 📁 项目结构 / Project Structure

```
paperang-miaomiaoji-tool-gen2/
├── paperang/                     # Python 包
│   ├── __init__.py               # 版本信息
│   ├── __main__.py               # python -m paperang 入口
│   ├── cli.py                    # 命令行界面（argparse）
│   ├── bt.py                     # 蓝牙串口通信管理
│   ├── config.py                 # 配置读写、串口扫描
│   ├── const.py                  # 蓝牙协议常量
│   ├── image.py                  # 图像处理（二值化/缩放/二维码）
│   ├── text.py                   # 文字转位图
│   ├── interactive.py            # 交互式终端界面
│   ├── gui.py                    # Tkinter 图形界面
│   └── mac_auto_print.py         # MacOS 自动设备发现
├── assets/                       # 静态资源
│   ├── MapleMono-NF-CN-Light.ttf # 等宽字体
│   └── test_image.jpg            # 测试图片
├── img/                          # 文档截图
├── scripts/
│   └── 喵喵机.bat                # Windows 启动脚本（旧版）
├── setup_env.py                  # 🆕 自动环境配置脚本
├── run_paperang.py               # 🆕 统一启动入口（GUI/CLI）
├── start.sh / start.bat          # 🆕 一键启动脚本（自动生成）
├── SKILL.md                      # Claude Code Skill 定义
├── requirements.txt
├── README.md                     # 本文档
├── README_GUI.md                 # GUI 详细使用文档
├── README_MACOS.md               # MacOS 适配说明
├── LICENSE
└── .gitignore
```

---

## 🤖 Claude Code Skill

本项目根目录下的 `SKILL.md` 是 Claude Code skill 定义文件。
在 Claude Code 中使用 `/paperang` 即可让 AI 助手操控喵喵机打印。

---

## 🔍 故障排除 / Troubleshooting

### MacOS 常见问题

**Q: 找不到蓝牙设备？**
- 确保已在系统设置→蓝牙中配对 Paperang 设备
- 检查权限：系统设置→隐私与安全性→蓝牙，确保终端应用已授权
- 运行 `python run_paperang.py scan` 扫描设备

**Q: GUI 无法启动（Tkinter 错误）？**
```bash
# 安装 tkinter
brew install python-tk
```

**Q: 权限被拒绝？**
```bash
# 赋予执行权限
chmod +x start.sh
```

### Windows 常见问题

**Q: 找不到 COM 端口？**
- 打开"设备管理器"→"端口 (COM & LPT)"查看 Paperang 设备
- 重新配对设备并添加传出 COM 端口

**Q: tkinter 缺失？**
- 重新安装 Python，确保勾选 "tcl/tk" 选项

### Linux 常见问题

**Q: 权限不足？**
```bash
# 将用户加入 dialout 组
sudo usermod -a -G dialout $USER
# 重启或重新登录
```

---

## 🖼️ 图像处理说明 / Image Processing

| 模式 | 算法 | 适用场景 |
|---|---|---|
| `floyd` | Floyd-Steinberg 误差扩散 | 照片、渐变图、连续色调 |
| `adaptive` | 局部自适应阈值 | 文档、线稿、高对比度图形 |

图像自动旋转以获得最佳打印方向，宽度统一缩放至 576 像素。

---

## 🙏 致谢 / Credits

- 原始项目 [ihciah/miaomiaoji-tool](https://github.com/ihciah/miaomiaoji-tool) — 喵喵机蓝牙协议逆向
- 字体 [subframe7536/maple-font](https://github.com/subframe7536/maple-font) — MapleMono 等宽字体
- 作者 [createskyblue](https://github.com/createskyblue) — 二代适配、CLI 重构、交互式功能、GUI 界面、MacOS 适配

---

## 📄 License

MIT © [ihciah](https://github.com/ihciah), [createskyblue](https://github.com/createskyblue)
