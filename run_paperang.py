#!/usr/bin/env python3
"""
Paperang 喵喵机打印工具 - 启动脚本

使用方法:
    python run_paperang.py          # 启动 GUI 界面
    python run_paperang.py --cli    # 启动命令行交互模式
    python run_paperang.py --help   # 查看帮助信息
"""

import sys
import os
import argparse

# 添加项目路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)


def main():
    parser = argparse.ArgumentParser(
        description="🖨️ Paperang 喵喵机打印工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run_paperang.py                 启动图形界面
  python run_paperang.py --cli           启动命令行交互模式
  python run_paperang.py text "Hello"    直接打印文字
  python run_paperang.py image photo.jpg 直接打印图片
        """
    )
    
    parser.add_argument('--cli', action='store_true', 
                        help='启动命令行交互模式')
    parser.add_argument('--gui', action='store_true', 
                        help='启动图形界面 (默认)')
    parser.add_argument('mode', nargs='?', choices=['text', 'image', 'qrcode', 'scan', 'feed', 'selftest'],
                        help='直接执行的模式')
    parser.add_argument('content', nargs='?', 
                        help='对应模式的内容 (文字/图片路径/二维码内容)')
    
    args = parser.parse_args()
    
    # 直接执行命令模式
    if args.mode:
        from paperang.mac_auto_print import PaperangPrinter
        
        printer = PaperangPrinter()
        
        if args.mode == 'scan':
            printer.scan_devices()
        elif args.mode == 'text':
            if not args.content:
                print("❌ 错误：请提供要打印的文字")
                sys.exit(1)
            printer.print_text(args.content)
        elif args.mode == 'image':
            if not args.content or not os.path.exists(args.content):
                print("❌ 错误：请提供有效的图片路径")
                sys.exit(1)
            printer.print_image(args.content)
        elif args.mode == 'qrcode':
            if not args.content:
                print("❌ 错误：请提供二维码内容")
                sys.exit(1)
            printer.print_qrcode(args.content)
        elif args.mode == 'feed':
            printer.feed_paper()
        elif args.mode == 'selftest':
            printer.self_test()
        
        return
    
    # 命令行交互模式
    if args.cli:
        print("🚀 启动命令行交互模式...")
        from paperang.interactive import main as interactive_main
        interactive_main()
        return
    
    # 默认：启动 GUI 界面
    print("🚀 启动图形界面...")
    try:
        from paperang.gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"⚠️  GUI 模块导入失败：{e}")
        print("💡 提示：请确保已安装 tkinter (通常随 Python 一起安装)")
        print("🔄 切换到命令行交互模式...")
        from paperang.interactive import main as interactive_main
        interactive_main()


if __name__ == "__main__":
    main()
