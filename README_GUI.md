# 🖨️ Paperang 喵喵机打印工具 - GUI 使用说明

## 📋 功能概述

本项目已添加完整的图形化界面 (GUI)，支持在 **MacOS** 和 **Windows** 系统上运行，提供以下功能：

- ✅ **自动设备发现**：启动时自动扫描并连接 Paperang 喵喵机
- ✅ **文字打印**：自定义文字内容，可调节字体大小
- ✅ **图片打印**：支持多种格式图片，带预览功能
- ✅ **二维码打印**：一键生成并打印二维码
- ✅ **打印机控制**：走纸、自检页、电量查询
- ✅ **实时日志**：显示操作状态和调试信息

---

## 🚀 快速启动

### 方法一：使用启动脚本（推荐）

```bash
# 进入项目目录
cd /workspace

# 启动 GUI 界面
python run_paperang.py

# 或使用命令行交互模式
python run_paperang.py --cli

# 直接打印文字
python run_paperang.py text "Hello World"

# 直接打印图片
python run_paperang.py image photo.jpg

# 直接打印二维码
python run_paperang.py qrcode "https://example.com"
```

### 方法二：直接运行 GUI 模块

```bash
cd /workspace
export PYTHONPATH=/workspace
python -m paperang.gui
```

---

## 📦 依赖安装

### MacOS

```bash
# 安装 tkinter 支持
brew install python-tk

# 安装 Python 依赖
pip install pyserial pillow numpy qrcode
```

### Windows

1. 重新运行 Python 安装程序
2. 勾选 **"tcl/tk and IDLE"** 选项
3. 安装 Python 依赖：
   ```bash
   pip install pyserial pillow numpy qrcode
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get install python3-tk
pip install pyserial pillow numpy qrcode
```

---

## 🎨 GUI 界面说明

### 界面布局

```
┌─────────────────────────────────────────────┐
│ 📡 设备连接                                  │
│ ● 已连接  端口：/dev/cu.Paperang_XXX        │
│ [🔌 连接] [🔍 扫描]                         │
├─────────────────────────────────────────────┤
│ [📝 文字打印] [🖼️ 图片打印] [📱 二维码打印] │
│                                             │
│  (标签页内容区域)                            │
├─────────────────────────────────────────────┤
│ ⚙️ 打印机控制                                │
│ [📄 走纸] [🧪 自检页] [🔋 电量查询]          │
├─────────────────────────────────────────────┤
│ 📋 操作日志                                  │
│ [INFO] 正在自动查找 Paperang 设备...         │
│ [INFO] ✓ 找到 Paperang 设备：/dev/cu.xxx    │
│ [INFO] ✓ 连接成功                           │
└─────────────────────────────────────────────┘
```

### 功能标签页

#### 📝 文字打印
- 输入任意文字内容（支持换行）
- 滑动条调节字体大小（8-72pt）
- 点击"打印文字"按钮执行

#### 🖼️ 图片打印
- 浏览选择本地图片文件
- 实时预览缩略图
- 选择处理模式：
  - `auto`: 自动选择最佳模式
  - `floyd`: Floyd-Steinberg 抖动算法
  - `adaptive`: 自适应阈值二值化

#### 📱 二维码打印
- 输入网址、文本等任意内容
- 自动生成二维码并打印

---

## 🔧 MacOS 特别注意事项

### 1. 蓝牙配对

在开始使用前，确保已完成蓝牙配对：

1. 打开 **系统设置 → 蓝牙**
2. 开启 Paperang 喵喵机电源
3. 点击设备进行配对
4. 配对成功后会显示为 `/dev/cu.Paperang_XXXX`

### 2. 蓝牙权限

macOS Ventura 及更高版本需要授予蓝牙权限：

1. 打开 **系统设置 → 隐私与安全性 → 蓝牙**
2. 找到你使用的终端应用（如 Terminal、iTerm2、VSCode）
3. 开启蓝牙访问权限

### 3. 设备路径

MacOS 上的串口设备路径格式：
- `/dev/cu.Paperang_XXXX` - 呼叫设备（用于通信）
- `/dev/tty.Paperang_XXXX` - 终端设备（用于监听）

程序会自动识别并使用正确的路径。

---

## ⌨️ 命令行参数

```bash
python run_paperang.py [选项] [模式] [内容]

模式:
  text      打印文字
  image     打印图片
  qrcode    打印二维码
  scan      扫描设备
  feed      走纸
  selftest  打印自检页

选项:
  --cli     启动命令行交互模式
  --gui     强制启动 GUI（默认）
  --help    显示帮助信息
```

### 使用示例

```bash
# 扫描可用设备
python run_paperang.py scan

# 打印文字
python run_paperang.py text "Hello World"

# 打印指定图片
python run_paperang.py image /path/to/photo.jpg

# 打印二维码
python run_paperang.py qrcode "https://github.com"

# 走纸 50 行
python run_paperang.py feed

# 打印自检页
python run_paperang.py selftest
```

---

## ❓ 故障排除

### GUI 无法启动

**问题**: 提示 `tkinter not available`

**解决**:
- MacOS: `brew install python-tk`
- Windows: 重新安装 Python，勾选 tcl/tk
- Linux: `sudo apt-get install python3-tk`

### 找不到设备

**问题**: 扫描不到 Paperang 设备

**解决**:
1. 确认设备已开机
2. 在系统蓝牙设置中检查是否已配对
3. 重启设备后重试
4. 查看日志输出获取详细错误信息

### 连接失败

**问题**: 连接设备时超时或失败

**解决**:
1. 关闭其他可能占用蓝牙的应用
2. 断开重连设备
3. 检查蓝牙权限设置
4. 尝试手动选择串口端口

---

## 📁 项目结构

```
/workspace/
├── run_paperang.py          # 主启动脚本
├── paperang/
│   ├── gui.py               # GUI 界面模块
│   ├── bt.py                # 蓝牙通信模块
│   ├── config.py            # 配置管理模块
│   ├── image.py             # 图像处理模块
│   ├── text.py              # 文字转换模块
│   ├── const.py             # 常量定义
│   ├── mac_auto_print.py    # MacOS 自动化脚本
│   └── interactive.py       # 命令行交互模式
└── README_GUI.md            # 本说明文档
```

---

## 🎯 下一步

1. **启动应用**: `python run_paperang.py`
2. **连接设备**: 点击"扫描设备"或直接等待自动连接
3. **选择内容**: 切换到对应标签页输入内容
4. **打印**: 点击打印按钮享受热敏打印乐趣！

如有问题，请查看日志区域的详细输出信息。
