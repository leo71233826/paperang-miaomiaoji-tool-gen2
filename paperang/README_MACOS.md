# MacOS Paperang 喵喵机自动打印指南

本项目已重构以支持 MacOS 系统，实现了 Paperang 设备的自动发现、稳定连接和自定义打印功能。

## 📋 目录

- [系统要求](#系统要求)
- [安装步骤](#安装步骤)
- [使用方法](#使用方法)
- [故障排除](#故障排除)
- [API 说明](#api-说明)

---

## 🔧 系统要求

### 硬件
- Paperang 2 (喵喵机 2) 或兼容设备
- Mac 电脑（支持蓝牙）

### 软件
- macOS 10.15+ (Catalina 或更高版本)
- Python 3.8+
- 依赖库：`pyserial`, `pillow`, `qrcode`

---

## 📦 安装步骤

### 1. 克隆项目
```bash
cd /path/to/your/workspace
git clone <repository-url>
cd paperang
```

### 2. 安装依赖
```bash
pip install pyserial pillow qrcode
```

### 3. 配对蓝牙设备

1. 打开 **系统设置** → **蓝牙**
2. 开启喵喵机电源
3. 在蓝牙列表中找到 "Paperang" 或类似名称的设备
4. 点击 **连接** 进行配对

### 4. 授予蓝牙权限

macOS 需要为终端应用授予蓝牙权限：

1. 打开 **系统设置** → **隐私与安全性** → **蓝牙**
2. 找到你使用的终端应用（如 Terminal、iTerm2、VSCode）
3. 勾选允许访问蓝牙

---

## 🚀 使用方法

### 方式一：使用专用脚本（推荐）

```bash
# 进入项目目录
cd /path/to/paperang

# 设置环境变量
export PYTHONPATH=/path/to/paperang/..

# 扫描可用设备
python mac_auto_print.py scan

# 打印文字
python mac_auto_print.py text "Hello World"

# 打印图片
python mac_auto_print.py image photo.jpg

# 打印二维码
python mac_auto_print.py qrcode "https://example.com"

# 打印自检页
python mac_auto_print.py selftest

# 走纸
python mac_auto_print.py feed 100
```

### 方式二：使用原有 CLI 工具

```bash
# 设置环境变量
export PYTHONPATH=/path/to/paperang/..

# 运行原有命令
python -m paperang text "Hello"
python -m paperang image photo.jpg
python -m paperang interactive
```

### 方式三：Python API 调用

```python
from paperang.mac_auto_print import PaperangPrinter

# 创建打印机实例（自动连接）
printer = PaperangPrinter(auto_connect=True)

if printer.connected:
    # 打印文字
    printer.print_text("Hello World", font_size=24)
    
    # 打印图片
    printer.print_image("photo.jpg", mode="floyd")
    
    # 打印二维码
    printer.print_qrcode("https://example.com")
    
    # 断开连接
    printer.disconnect()
```

---

## ⚙️ 高级选项

### 文字打印选项
```bash
# 自定义字体大小和走纸长度
python mac_auto_print.py text "内容" --font-size 32 --feed 128
```

### 图片处理模式
```bash
# Floyd 抖动（默认，效果好）
python mac_auto_print.py image photo.jpg --mode floyd

# 自适应阈值（速度快）
python mac_auto_print.py image photo.jpg --mode adaptive

# 简写
python mac_auto_print.py image photo.jpg --mode f   # floyd
python mac_auto_print.py image photo.jpg --mode a   # adaptive
```

---

## 🔍 故障排除

### 问题 1：找不到设备

**症状**: 运行 `scan` 命令显示 0 个设备

**解决方案**:
1. 确认喵喵机已开机（长按电源键）
2. 在 macOS 蓝牙设置中确认设备已配对
3. 检查蓝牙权限是否已授予终端应用
4. 尝试关闭并重新打开蓝牙

### 问题 2：连接失败

**症状**: 找到设备但连接失败

**解决方案**:
1. 删除已配对的设备，重新配对
2. 重启喵喵机
3. 检查是否有其他应用占用了蓝牙连接
4. 尝试增加重试次数（修改配置中的 `max_retries`）

### 问题 3：打印内容模糊

**解决方案**:
1. 调整加热密度：在代码中修改 `sendDensityToBt()` 参数（50-150）
2. 确保纸张安装正确
3. 清洁打印头

### 问题 4：MacOS 特定端口问题

在 macOS 上，蓝牙串口设备通常位于 `/dev/cu.*` 路径下：

```bash
# 查看所有可用串口
ls -la /dev/cu.*

# Paperang 设备通常命名为类似：
# /dev/cu.Paperang_XXXX
# /dev/cu.MLP_XXXX
```

---

## 📚 API 说明

### PaperangPrinter 类

#### 构造函数
```python
PaperangPrinter(auto_connect=True, max_retries=3)
```
- `auto_connect`: 是否自动连接设备
- `max_retries`: 最大重试次数

#### 方法

| 方法 | 描述 | 参数 |
|------|------|------|
| `connect()` | 手动连接设备 | 无 |
| `disconnect()` | 断开连接 | 无 |
| `print_text(text, font_size, feed)` | 打印文字 | text: 文字内容<br>font_size: 字体大小 (默认 24)<br>feed: 走纸长度 (默认 64) |
| `print_image(path, mode, feed)` | 打印图片 | path: 图片路径<br>mode: 处理模式 (floyd/adaptive)<br>feed: 走纸长度 |
| `print_qrcode(content, feed)` | 打印二维码 | content: 二维码内容<br>feed: 走纸长度 |
| `self_test()` | 打印自检页 | 无 |
| `feed_paper(length)` | 走纸 | length: 走纸长度 |

### 配置项

配置文件保存在 `config.json`，可手动编辑：

```json
{
  "serial_port": "/dev/cu.Paperang_XXXX",
  "baudrate": 115200,
  "timeout": 1,
  "auto_reconnect": true,
  "max_retries": 3
}
```

---

## 📝 注意事项

1. **首次使用**: 运行 `scan` 命令查看可用设备
2. **配置保存**: 成功连接后，串口信息会自动保存到 `config.json`
3. **批量打印**: 连续打印时设置 `--feed 0`，最后统一走纸
4. **电量检查**: 低电量会影响打印质量，请及时充电

---

## 🛠️ 开发调试

启用详细日志：
```bash
export LOG_LEVEL=DEBUG
python mac_auto_print.py scan
```

---

## 📄 许可证

与原项目保持一致。
