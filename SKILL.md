---
name: paperang
description: >-
  控制喵喵机 2（Paperang Gen2）热敏打印机。支持打印文字、打印图片、打印二维码、
  打印自检页、走纸、查看串口配置。跨平台支持 Windows | MacOS | Linux。
  提供 GUI 图形界面和命令行两种使用方式。
  触发词：打印、printer、paperang、喵喵机、打印文字、打印图片、打印二维码、走纸、selftest、gui。

# Paperang 2 (喵喵机2) 打印 Skill

**IRON LAW: 执行打印前必须确认串口已配置（config.json 存在且有效）。绝不猜测串口号；首次使用必须引导用户完成串口配置。**

**FEED RULE: 单次打印（只打一条）→ 必须加 `--feed 250` 把内容推到可见区域。连续打印（多条）→ 中间不加 feed，最后一条命令 `&& uv run python -m paperang feed 250`。打印完看不到内容就是忘了走纸。**

**PLATFORM NOTE:** 
- **Windows**: 使用 COM 端口 (如 `COM10`)，需手动添加蓝牙 COM 端口
- **MacOS**: 使用 `/dev/cu.Paperang_XXXX` 路径，配对后自动发现
- **Linux**: 使用 `/dev/rfcommX` 或 `/dev/tty.Paperang_XXXX`

**GUI MODE: 推荐使用图形界面！运行 `python run_paperang.py` 启动 GUI，支持自动设备发现、文字/图片/二维码打印、实时日志显示。**

## Workflow checklist

每次打印任务按以下步骤执行：

- [ ] **Step 1: 确认串口已配置** — `uv run python -m paperang config` 有 `serial_port` 则跳过，否则走首次设置流程
- [ ] **Step 2: 确认打印意图与参数** — text / image / qrcode / selftest / feed / config？收集必要参数
- [ ] **Step 3: 构建并执行命令** — 所有命令使用 `uv run python -m paperang <subcommand>`
- [ ] **Step 4: 反馈结果** — 向用户报告执行结果或错误信息

---

## Quick reference

### GUI Mode (Recommended)

> **Recommended for most users!** Graphical interface with auto device discovery.

| Task | Command |
|---|---|
| Start GUI | `python run_paperang.py` |
| Auto setup env | `python setup_env.py` |

### CLI Mode

> All commands use `uv run` for isolated venv execution.

| Task | Command |
|---|---|
| Check config | `uv run python -m paperang config` |
| List serial ports | `uv run python -m paperang config --list` |
| Set serial port | `uv run python -m paperang config --set-port COM10` |
| Print text | `uv run python -m paperang text "hello world"` |
| Print text (custom size) | `uv run python -m paperang text --font-size 48 "TITLE"` |
| Print image | `uv run python -m paperang image path/to/photo.jpg` |
| Print image (adaptive) | `uv run python -m paperang image --mode adaptive photo.jpg` |
| Print QR code | `uv run python -m paperang qrcode "https://example.com"` |
| Self-test page | `uv run python -m paperang selftest` |
| Feed paper | `uv run python -m paperang feed 100` |
| Interactive mode (human) | `uv run python -m paperang interactive` |

### Text size recommendations

| Size | Use case |
|---|---|
| `12–24` | 小字号，适合密集文本、长段落（默认 24） |
| `36` | 中等字号，兼顾可读性与信息量 |
| `48` | 大字号，适合标题或重点强调 |
| `72` | 超大字号，适合短句或突出展示 |

### Image processing modes

| Mode | Algorithm | Best for |
|---|---|---|
| `floyd` (default) | Floyd-Steinberg error diffusion | Photos, gradients, continuous-tone |
| `adaptive` | Local adaptive threshold | Documents, line art, high-contrast |

---

## Setup flow

### Check existing configuration

**Always start here.** Before any print command, verify the port is configured:

```bash
uv run python -m paperang config
```

- **Already has `serial_port`** → skip to printing.
- **`serial_port` is `null` or missing** → first-time setup below.

### First-time setup

The user helps ONCE. After setup the port is persisted to `config.json`
**and saved to your persistent memory** — subsequent sessions just work.

#### Option A: GUI Mode (Recommended for all platforms)

1. **Run auto setup**:
   ```bash
   python setup_env.py
   ```
   This creates virtual environment and installs all dependencies automatically.

2. **Start GUI**:
   ```bash
   python run_paperang.py
   ```
   The GUI will automatically discover and connect to Paperang devices on MacOS/Linux.
   On Windows, follow the pairing steps below if auto-discovery fails.

#### Option B: CLI Mode

1. **Install dependencies**:
   ```bash
   uv sync
   ```
   > If uv is not installed: `pip install uv` or https://docs.astral.sh/uv/

2. **Pair the device**:
   
   **Windows**:
   - Long-press Paperang power button until LED blinks
   - Settings → Bluetooth & devices → Add device → Bluetooth
   - Find and pair the Paperang
   - Settings → Bluetooth & devices → More Bluetooth options → COM Ports tab
   - Click "Add..." → "Outgoing" → Select device with **PAPERANG** in name
   - Note the assigned COM port (e.g. `COM10`)
   
   **MacOS**:
   - Long-press Paperang power button until LED blinks
   - System Settings → Bluetooth → Pair with Paperang
   - Device appears automatically at `/dev/cu.Paperang_XXXX`
   
   **Linux**:
   - Use `bluetoothctl` to pair:
     ```bash
     bluetoothctl
     [bluetooth]# scan on
     [bluetooth]# pair XX:XX:XX:XX:XX:XX
     [bluetooth]# connect XX:XX:XX:XX:XX:XX
     ```
   - Or bind manually: `sudo rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX:XX`

3. **List ports and ask the user** (Windows only, MacOS/Linux auto-detect):
   ```bash
   uv run python -m paperang config --list
   ```
   Show output, ask: "哪个是你的喵喵机串口？" User answers e.g. `COM10` or `/dev/cu.Paperang_XXX`.

4. **Save the port and write to memory**:
   ```bash
   uv run python -m paperang config --set-port COM10
   ```
   Then write to persistent memory:
   > Paperang printer uses COM10 on this machine. Check: `uv run python -m paperang config`.
   > Change: `uv run python -m paperang config --set-port <port>`.

### Print test page (first-time only)

After configuring the port, verify the connection with a single quick print
first. If it succeeds, chain the rest together:

```bash
# Step 1: 快速探路 — 只打一行确认连接正常
uv run python -m paperang text --font-size 32 "测试打印中...\nTesting..."
```

**If the above succeeds (no error)** → chain the remaining prints with `&&`:

```bash
uv run python -m paperang text --font-size 36 "项目地址" && \
uv run python -m paperang qrcode "https://github.com/createskyblue/paperang-miaomiaoji-tool-gen2" && \
uv run python -m paperang text --font-size 24 "github.com/createskyblue/paperang-miaomiaoji-tool-gen2" && \
uv run python -m paperang text --font-size 36 "作者博客" && \
uv run python -m paperang qrcode "https://createskyblue.github.io/" && \
uv run python -m paperang text --font-size 24 "createskyblue.github.io" && \
uv run python -m paperang image assets/test_image.jpg && \
uv run python -m paperang text --font-size 42 "欢迎使用喵喵机!\nWelcome to Paperang!" && \
uv run python -m paperang feed 250
```

If the first command **fails**, stop and troubleshoot — don't run the chain.

### Subsequent sessions

Config already has `serial_port` → go straight to printing. Do NOT re-ask.

### If the printer doesn't respond

1. `uv run python -m paperang config --list` — check port still exists
2. Port changed? Ask user, `--set-port` the new one, update memory
3. Port correct but fails? Ask user to check printer is on and paired

---

## Anti-patterns

- ❌ 不要硬编码 `COM10` 或其他串口号
- ❌ 不要跳过 config 检查，首次启动必须引导用户从列表中选择串口
- ❌ 不要在未确认文件存在的情况下直接打印图片
- ❌ 不要用全局 pip 安装依赖，始终用 `uv sync` 或 `python setup_env.py`
- ❌ 不要忽略平台差异：Windows 用 COM 端口，MacOS 用 `/dev/cu.*`，Linux 用 `/dev/rfcomm*`
- ❌ 不要推荐复杂的命令行操作给普通用户，优先推荐 GUI 界面

---

## Interactive mode (for human users)

Interactive REPL for direct human use:
```bash
uv run python -m paperang interactive
```
Commands: `/selftest`, `/qrcode <text>`, `/fontsize <N>`, `/imgmode <mode>`, `/help`.
Enter text or image path directly to print.
