import json
import os
import sys
import time
import logging
import serial
import serial.tools.list_ports

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULT_CONFIG = {
    "serial_port": None,
    "baudrate": 115200,
    "timeout": 1,
    "auto_reconnect": True,
    "max_retries": 3
}

# Paperang 设备识别关键词（支持多语言）
PAPERANG_KEYWORDS = ['paperang', 'bt', 'mlp', 'bluetooth']


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return {**DEFAULT_CONFIG, **cfg}
    return DEFAULT_CONFIG.copy()


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def is_paperang_device(port_info):
    """判断串口设备是否为 Paperang 喵喵机"""
    device_name = (port_info.device or "").lower()
    description = (port_info.description or "").lower()
    hwid = (port_info.hwid or "").lower()
    
    # 组合所有信息进行匹配
    full_text = f"{device_name} {description} {hwid}"
    
    # 检查是否包含 Paperang 关键词
    if any(keyword in full_text for keyword in PAPERANG_KEYWORDS):
        return True
    
    # MacOS 特殊处理：/dev/cu. 开头的蓝牙串口设备
    if sys.platform == 'darwin':
        if device_name.startswith('/dev/cu.') and 'bt' in full_text:
            return True
    
    return False


def list_serial_ports():
    """列出所有可用串口"""
    ports = serial.tools.list_ports.comports()
    return [(p.device, f"{p.description}") for p in ports]


def find_paperang_port():
    """自动查找 Paperang 设备端口"""
    ports = serial.tools.list_ports.comports()
    paperang_ports = []
    
    logging.info(f"检测到 {len(ports)} 个串口设备")
    
    for port in ports:
        if is_paperang_device(port):
            paperang_ports.append(port)
            logging.info(f"找到 Paperang 设备：{port.device} - {port.description}")
    
    if not paperang_ports:
        logging.warning("未找到 Paperang 设备，列出所有可用串口:")
        for port in ports:
            logging.info(f"  {port.device} - {port.description}")
        return None
    
    # 优先返回第一个匹配的设备
    return paperang_ports[0].device


def setup_config(auto_find=True):
    """配置串口连接，支持自动发现"""
    cfg = load_config()
    
    # 如果已配置端口且有效，直接返回
    if cfg.get("serial_port"):
        try:
            # 验证端口是否仍然可用
            ports = [p.device for p in serial.tools.list_ports.comports()]
            if cfg["serial_port"] in ports:
                logging.info(f"使用已保存的串口：{cfg['serial_port']}")
                return cfg
            else:
                logging.warning(f"已保存的串口 {cfg['serial_port']} 不可用，尝试自动查找")
        except Exception as e:
            logging.warning(f"验证串口失败：{e}")
    
    # 自动查找 Paperang 设备
    if auto_find:
        print("正在自动查找 Paperang 设备...")
        port = find_paperang_port()
        if port:
            cfg["serial_port"] = port
            save_config(cfg)
            print(f"✓ 找到 Paperang 设备：{port}")
            print(f"  配置已保存至：{CONFIG_FILE}")
            return cfg
        else:
            print("✗ 未自动找到 Paperang 设备")
    
    # 手动选择备用方案
    print("\n未找到设备或需要手动选择，可用串口列表：")
    ports = list_serial_ports()
    if not ports:
        print("未检测到可用串口，请检查设备连接后重试。")
        print("💡 MacOS 用户请确保:")
        print("   1. 在系统设置→蓝牙中配对 Paperang 设备")
        print("   2. 在系统设置→隐私与安全性→蓝牙中授予终端应用权限")
        print("   3. 运行 'ls /dev/cu.*' 查看是否有 Paperang 相关设备")
        # 返回一个空配置而不是抛出异常，允许 GUI 显示但无法连接
        return cfg

    for idx, (device, desc) in enumerate(ports, 1):
        marker = " *已保存" if device == cfg.get("serial_port") else ""
        print(f"  {idx}. {device} - {desc}{marker}")

    while True:
        try:
            choice_input = input("\n请选择串口编号 (或按 Enter 重试自动查找): ").strip()
            if not choice_input:
                # 重新自动查找
                port = find_paperang_port()
                if port:
                    cfg["serial_port"] = port
                    save_config(cfg)
                    print(f"✓ 找到 Paperang 设备：{port}")
                    return cfg
                continue
            
            choice = int(choice_input)
            if 1 <= choice <= len(ports):
                selected = ports[choice - 1][0]
                break
            else:
                print("输入无效，请重新选择。")
        except ValueError:
            print("请输入数字编号。")

    cfg["serial_port"] = selected
    save_config(cfg)
    print(f"已保存配置：{selected} -> {CONFIG_FILE}\n")
    return cfg
