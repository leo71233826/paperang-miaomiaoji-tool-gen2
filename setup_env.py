#!/usr/bin/env python3
"""
Paperang 喵喵机 - 自动环境配置脚本
功能：
1. 自动创建虚拟环境 (.venv)
2. 自动安装依赖 (pyserial, pillow, numpy, qrcode[pil])
3. 自动检测系统依赖 (如 MacOS 的 tkinter)
4. 提供一键启动入口

使用方法:
    python setup_env.py
"""

import os
import sys
import subprocess
import venv
import platform
from pathlib import Path

# 配置
VENV_DIR = ".venv"
REQUIREMENTS = [
    "pyserial",
    "pillow",
    "numpy",
    "qrcode[pil]"
]
PROJECT_NAME = "Paperang 喵喵机"

class Colors:
    """终端颜色代码"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def run_command(cmd, description=""):
    """运行命令并显示进度"""
    if description:
        print(f"→ {description}...")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print_error(f"命令执行失败: {e}")
        if e.stderr:
            print(e.stderr)
        return False, e.stderr

def check_python_version():
    """检查 Python 版本"""
    print_header("检查 Python 环境")
    version = sys.version_info
    print(f"当前 Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_error("Python 版本过低，需要 Python 3.7+")
        return False
    
    print_success("Python 版本符合要求")
    return True

def check_tkinter():
    """检查 tkinter 是否可用"""
    print_header("检查 Tkinter 支持")
    try:
        import tkinter
        print_success("Tkinter 已安装")
        return True
    except ImportError:
        print_warning("Tkinter 未安装")
        
        system = platform.system()
        if system == "Darwin":  # MacOS
            print("\n在 MacOS 上安装 tkinter:")
            print("  brew install python-tk")
            print("\n或者如果使用官方 Python:")
            print("  请重新安装包含 tk 的 Python 版本")
        elif system == "Linux":
            distro = subprocess.run(["lsb_release", "-i"], capture_output=True, text=True).stdout
            if "Ubuntu" in distro or "Debian" in distro:
                print("\n在 Ubuntu/Debian 上安装 tkinter:")
                print("  sudo apt-get install python3-tk")
            elif "CentOS" in distro or "Fedora" in distro:
                print("\n在 CentOS/Fedora 上安装 tkinter:")
                print("  sudo yum install python3-tkinter")
        elif system == "Windows":
            print("\n在 Windows 上，tkinter 通常随 Python 一起安装。")
            print("如果缺失，请重新安装 Python 并确保勾选 'tcl/tk' 选项。")
        
        response = input("\n是否继续安装其他依赖？(y/n): ")
        return response.lower() == 'y'

def create_venv():
    """创建虚拟环境"""
    print_header("创建虚拟环境")
    
    venv_path = Path(VENV_DIR)
    if venv_path.exists():
        print_warning(f"虚拟环境已存在于: {venv_path.absolute()}")
        response = input("是否删除并重新创建？(y/n): ")
        if response.lower() == 'y':
            import shutil
            shutil.rmtree(VENV_DIR)
            print_success("已删除旧虚拟环境")
        else:
            print("使用现有虚拟环境")
            return True
    
    try:
        venv.create(VENV_DIR, with_pip=True)
        print_success(f"虚拟环境创建成功: {venv_path.absolute()}")
        return True
    except Exception as e:
        print_error(f"创建虚拟环境失败: {e}")
        return False

def get_pip_path():
    """获取虚拟环境中 pip 的路径"""
    system = platform.system()
    if system == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "pip")
    else:
        return os.path.join(VENV_DIR, "bin", "pip")

def get_python_path():
    """获取虚拟环境中 python 的路径"""
    system = platform.system()
    if system == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python")
    else:
        return os.path.join(VENV_DIR, "bin", "python")

def install_dependencies():
    """安装依赖包"""
    print_header("安装依赖包")
    
    pip_path = get_pip_path()
    
    # 升级 pip
    run_command(f'"{pip_path}" install --upgrade pip', "升级 pip")
    
    # 安装 requirements
    for package in REQUIREMENTS:
        success, _ = run_command(f'"{pip_path}" install "{package}"', f"安装 {package}")
        if not success:
            print_warning(f"安装 {package} 失败，但将继续尝试其他包")
    
    print_success("依赖安装完成")
    return True

def verify_installation():
    """验证安装"""
    print_header("验证安装")
    
    python_path = get_python_path()
    
    test_script = """
import sys
sys.path.insert(0, '.')
try:
    import serial
    import PIL
    import numpy
    import qrcode
    print("SUCCESS")
except ImportError as e:
    print(f"FAILED: {e}")
"""
    
    success, output = run_command(f'"{python_path}" -c "{test_script}"', "验证模块导入")
    
    if "SUCCESS" in output:
        print_success("所有依赖模块验证通过")
        return True
    else:
        print_error("部分模块验证失败")
        print(output)
        return False

def create_launcher():
    """创建快捷启动脚本"""
    print_header("创建启动脚本")
    
    launcher_content = f'''#!/usr/bin/env bash
# Paperang 喵喵机 - 快速启动脚本
# 由 setup_env.py 自动生成

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
VENV_PYTHON="{os.path.abspath(get_python_path())}"

echo "🖨️  启动 {PROJECT_NAME}..."
"$VENV_PYTHON" "$SCRIPT_DIR/run_paperang.py" "$@"
'''
    
    launcher_path = "start.sh"
    if platform.system() == "Windows":
        launcher_path = "start.bat"
        launcher_content = f'''@echo off
REM Paperang 喵喵机 - 快速启动脚本
REM 由 setup_env.py 自动生成

SET SCRIPT_DIR=%~dp0
SET VENV_PYTHON={os.path.abspath(get_python_path())}

echo 🖨️  启动 {PROJECT_NAME}...
"%VENV_PYTHON%" "%SCRIPT_DIR%run_paperang.py" %*
'''
    
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    if platform.system() != "Windows":
        os.chmod(launcher_path, 0o755)
    
    print_success(f"启动脚本已创建: {launcher_path}")
    print(f"  运行方式: ./{launcher_path} 或 ./{launcher_path} --help")
    
    return True

def main():
    """主函数"""
    print_header(PROJECT_NAME + " - 自动环境配置")
    print("本脚本将自动:")
    print("  1. 检查 Python 版本")
    print("  2. 检查 Tkinter 支持")
    print("  3. 创建虚拟环境 (.venv)")
    print("  4. 安装所需依赖")
    print("  5. 创建快捷启动脚本")
    print()
    
    # 步骤 1: 检查 Python
    if not check_python_version():
        sys.exit(1)
    
    # 步骤 2: 检查 Tkinter
    has_tkinter = check_tkinter()
    
    # 步骤 3: 创建虚拟环境
    if not create_venv():
        sys.exit(1)
    
    # 步骤 4: 安装依赖
    if not install_dependencies():
        print_warning("依赖安装可能不完整，但将继续")
    
    # 步骤 5: 验证
    verify_installation()
    
    # 步骤 6: 创建启动脚本
    create_launcher()
    
    # 完成
    print_header("配置完成")
    print_success("环境配置成功!")
    print()
    print("📦 虚拟环境位置:", os.path.abspath(VENV_DIR))
    print("🚀 启动方式:")
    
    if platform.system() == "Windows":
        print("   .\\start.bat          # GUI 界面")
        print("   .\\start.bat --cli    # 命令行模式")
    else:
        print("   ./start.sh            # GUI 界面")
        print("   ./start.sh --cli      # 命令行模式")
    
    print()
    print("💡 提示:")
    print("   - 首次运行前请确保已在系统蓝牙设置中配对 Paperang 设备")
    if not has_tkinter:
        print("   - ⚠️  Tkinter 未安装，GUI 界面可能无法使用，请先安装系统依赖")
    print("   - 详细文档请查看 README_GUI.md")
    print()

if __name__ == "__main__":
    main()
