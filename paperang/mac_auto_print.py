#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MacOS 专用 Paperang 喵喵机自动连接打印脚本

功能：
1. 自动扫描并连接 Paperang 设备
2. 支持文字、图片、二维码打印
3. 稳定的重连机制
4. 跨平台兼容（主要针对 MacOS 优化）

使用方法：
    python mac_auto_print.py text "Hello World"
    python mac_auto_print.py image photo.jpg
    python mac_auto_print.py qrcode "https://example.com"
    python mac_auto_print.py scan  # 扫描可用设备
"""

import sys
import os
import time
import logging
import argparse

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from paperang.config import (
    load_config, save_config, find_paperang_port, 
    list_serial_ports, is_paperang_device, setup_config
)
from paperang.bt import BtManager
from paperang.image import ImageConverter
from paperang.text import TextConverter


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PaperangPrinter:
    """Paperang 打印机管理类，支持自动连接和稳定打印"""
    
    def __init__(self, auto_connect=True, max_retries=3):
        self.mmj = None
        self.cfg = None
        self.connected = False
        self.max_retries = max_retries
        
        if auto_connect:
            self.connect()
    
    def connect(self):
        """自动查找并连接 Paperang 设备"""
        logger.info("正在查找 Paperang 设备...")
        
        # 尝试自动查找设备
        port = find_paperang_port()
        
        if not port:
            print("\n未自动找到 Paperang 设备")
            print("请确保:")
            print("  1. 喵喵机已开机")
            print("  2. 已在 MacOS 蓝牙设置中配对设备")
            print("  3. 已授予终端/Python 蓝牙权限\n")
            
            # 列出所有可用端口
            ports = list_serial_ports()
            if ports:
                print("可用串口列表:")
                for idx, (device, desc) in enumerate(ports, 1):
                    print(f"  {idx}. {device} - {desc}")
                
                try:
                    choice = int(input("\n请选择串口编号 (或按 Enter 退出): ").strip())
                    if 1 <= choice <= len(ports):
                        port = ports[choice - 1][0]
                    else:
                        return False
                except (ValueError, KeyboardInterrupt):
                    return False
            else:
                print("未检测到任何串口设备")
                return False
        
        # 保存配置
        self.cfg = load_config()
        self.cfg["serial_port"] = port
        self.cfg["max_retries"] = self.max_retries
        save_config(self.cfg)
        
        logger.info(f"使用串口：{port}")
        
        # 连接设备
        try:
            self.mmj = BtManager(self.cfg)
            if self.mmj.connected:
                logger.info("✓ 成功连接到 Paperang 设备")
                self.connected = True
                
                # 注册 CRC 密钥和设置默认参数
                self.mmj.registerCrcKeyToBt()
                self.mmj.sendDensityToBt(100)  # 加热密度
                self.mmj.sendPowerOffTimeToBt(0)  # 不休眠
                
                return True
            else:
                logger.error("✗ 连接失败")
                return False
        except Exception as e:
            logger.error(f"连接异常：{e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.mmj:
            try:
                self.mmj.disconnect()
                self.connected = False
                logger.info("已断开连接")
            except Exception as e:
                logger.warning(f"断开连接时出错：{e}")
    
    def print_text(self, text, font_size=24, feed=64):
        """打印文字"""
        if not self.connected:
            logger.error("设备未连接")
            return False
        
        try:
            logger.info(f"正在打印文字：{text[:50]}...")
            img_data = TextConverter.text2bmp(text, font_size=font_size)
            self.mmj.sendImageToBt(img_data)
            if feed > 0:
                self.mmj.sendFeedLineToBt(feed)
            logger.info("✓ 打印完成")
            return True
        except Exception as e:
            logger.error(f"打印失败：{e}")
            return False
    
    def print_image(self, image_path, mode="floyd", feed=64):
        """打印图片"""
        if not self.connected:
            logger.error("设备未连接")
            return False
        
        if not os.path.isfile(image_path):
            logger.error(f"文件不存在：{image_path}")
            return False
        
        try:
            logger.info(f"正在打印图片：{image_path}")
            img_data = ImageConverter.process_image_for_printing_with_mode(
                image_path, mode
            )
            self.mmj.sendImageToBt(img_data)
            if feed > 0:
                self.mmj.sendFeedLineToBt(feed)
            logger.info("✓ 打印完成")
            return True
        except Exception as e:
            logger.error(f"打印失败：{e}")
            return False
    
    def print_qrcode(self, content, feed=64):
        """打印二维码"""
        if not self.connected:
            logger.error("设备未连接")
            return False
        
        try:
            logger.info(f"正在打印二维码：{content}")
            img_data = ImageConverter.generate_qr_code(content)
            self.mmj.sendImageToBt(img_data)
            if feed > 0:
                self.mmj.sendFeedLineToBt(feed)
            logger.info("✓ 打印完成")
            return True
        except Exception as e:
            logger.error(f"打印失败：{e}")
            return False
    
    def self_test(self):
        """打印自检页"""
        if not self.connected:
            logger.error("设备未连接")
            return False
        
        try:
            logger.info("正在打印自检页")
            self.mmj.sendSelfTestToBt()
            logger.info("✓ 自检页已发送")
            return True
        except Exception as e:
            logger.error(f"自检失败：{e}")
            return False
    
    def feed_paper(self, length=64):
        """走纸"""
        if not self.connected:
            logger.error("设备未连接")
            return False
        
        try:
            self.mmj.sendFeedLineToBt(length)
            logger.info(f"✓ 走纸 {length} 点")
            return True
        except Exception as e:
            logger.error(f"走纸失败：{e}")
            return False


def cmd_scan(args):
    """扫描可用设备"""
    print("=" * 50)
    print("Paperang 设备扫描工具")
    print("=" * 50)
    
    ports = list_serial_ports()
    print(f"\n检测到 {len(ports)} 个串口设备:\n")
    
    for idx, (device, desc) in enumerate(ports, 1):
        is_paperang = is_paperang_device(type('PortInfo', (), {
            'device': device,
            'description': desc,
            'hwid': ''
        })())
        marker = " [Paperang?]" if is_paperang else ""
        print(f"  {idx}. {device}{marker}")
        print(f"     描述：{desc}\n")
    
    # 尝试自动查找
    print("-" * 50)
    paperang_port = find_paperang_port()
    if paperang_port:
        print(f"\n✓ 自动找到 Paperang 设备：{paperang_port}")
    else:
        print("\n✗ 未自动找到 Paperang 设备")


def cmd_text(args):
    """打印文字"""
    printer = PaperangPrinter(auto_connect=True)
    if not printer.connected:
        sys.exit(1)
    
    success = printer.print_text(
        args.text,
        font_size=args.font_size,
        feed=args.feed
    )
    printer.disconnect()
    
    if not success:
        sys.exit(1)


def cmd_image(args):
    """打印图片"""
    printer = PaperangPrinter(auto_connect=True)
    if not printer.connected:
        sys.exit(1)
    
    # 转换模式别名
    mode_map = {"f": "floyd", "a": "adaptive"}
    mode = mode_map.get(args.mode, args.mode)
    
    success = printer.print_image(
        args.path,
        mode=mode,
        feed=args.feed
    )
    printer.disconnect()
    
    if not success:
        sys.exit(1)


def cmd_qrcode(args):
    """打印二维码"""
    printer = PaperangPrinter(auto_connect=True)
    if not printer.connected:
        sys.exit(1)
    
    success = printer.print_qrcode(
        args.content,
        feed=args.feed
    )
    printer.disconnect()
    
    if not success:
        sys.exit(1)


def cmd_selftest(args):
    """打印自检页"""
    printer = PaperangPrinter(auto_connect=True)
    if not printer.connected:
        sys.exit(1)
    
    success = printer.self_test()
    printer.disconnect()
    
    if not success:
        sys.exit(1)


def cmd_feed(args):
    """走纸"""
    printer = PaperangPrinter(auto_connect=True)
    if not printer.connected:
        sys.exit(1)
    
    success = printer.feed_paper(args.length)
    printer.disconnect()
    
    if not success:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="mac_auto_print",
        description="MacOS Paperang 喵喵机自动连接打印工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s scan                      # 扫描可用设备
  %(prog)s text "Hello World"        # 打印文字
  %(prog)s image photo.jpg           # 打印图片
  %(prog)s qrcode "https://..."      # 打印二维码
  %(prog)s selftest                  # 打印自检页
  %(prog)s feed 100                  # 走纸 100 点
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # scan
    p_scan = subparsers.add_parser("scan", help="扫描可用设备")
    p_scan.set_defaults(func=cmd_scan)
    
    # text
    p_text = subparsers.add_parser("text", help="打印文字")
    p_text.add_argument("text", help="要打印的文字内容")
    p_text.add_argument("--font-size", type=int, default=24, help="字体大小 (默认 24)")
    p_text.add_argument("--feed", type=int, default=64, help="打印后走纸长度")
    p_text.set_defaults(func=cmd_text)
    
    # image
    p_img = subparsers.add_parser("image", help="打印图片")
    p_img.add_argument("path", help="图片路径")
    p_img.add_argument("--mode", choices=["floyd", "adaptive", "f", "a"], 
                       default="floyd", help="图像处理模式")
    p_img.add_argument("--feed", type=int, default=64, help="打印后走纸长度")
    p_img.set_defaults(func=cmd_image)
    
    # qrcode
    p_qr = subparsers.add_parser("qrcode", help="打印二维码")
    p_qr.add_argument("content", help="二维码内容")
    p_qr.add_argument("--feed", type=int, default=64, help="打印后走纸长度")
    p_qr.set_defaults(func=cmd_qrcode)
    
    # selftest
    p_test = subparsers.add_parser("selftest", help="打印自检页")
    p_test.set_defaults(func=cmd_selftest)
    
    # feed
    p_feed = subparsers.add_parser("feed", help="走纸")
    p_feed.add_argument("length", type=int, help="走纸长度")
    p_feed.set_defaults(func=cmd_feed)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
