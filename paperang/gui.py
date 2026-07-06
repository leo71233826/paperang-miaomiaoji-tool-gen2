#!/usr/bin/env python3
"""
Paperang 喵喵机 GUI 界面 - 跨平台图形化打印工具
支持 MacOS 和 Windows，自动发现设备，自定义打印内容

注意：需要 tkinter 支持 (通常随 Python 一起安装)
MacOS: 使用系统自带 Python 或 brew install python-tk
Windows: 安装 Python 时勾选 tcl/tk 选项
"""

import sys
import os

# 检查 tkinter 可用性
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("⚠️  tkinter 不可用，GUI 功能将无法使用")
    print("💡 MacOS 安装方法：brew install python-tk")
    print("💡 Windows: 重新安装 Python 并勾选 tcl/tk 选项")

if TKINTER_AVAILABLE:
    from PIL import Image, ImageTk

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from paperang.config import setup_config, find_paperang_port, load_config, save_config
from paperang.bt import BtManager
from paperang.image import ImageConverter
from paperang.text import TextConverter


class PaperangGUI:
    """Paperang 喵喵机图形化界面"""
    
    def __init__(self, root):
        if not TKINTER_AVAILABLE:
            messagebox.showerror("错误", "tkinter 不可用，无法启动 GUI")
            root.destroy()
            return
        
        self.root = root
        self.root.title("🖨️ Paperang 喵喵机打印工具")
        self.root.geometry("800x650")
        self.root.minsize(700, 600)
        
        # 状态变量
        self.bt_manager = None
        self.connected = False
        self.current_image_path = None
        self.print_queue = []
        
        # 配置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 启动时尝试自动连接
        self.root.after(100, self.auto_connect)
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        
        # 尝试使用现代主题
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
        
        # 自定义颜色
        self.colors = {
            'primary': '#2196F3',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#F44336',
            'bg': '#F5F5F5',
            'text': '#333333'
        }
        
        self.root.configure(bg=self.colors['bg'])
    
    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # === 连接状态区域 ===
        conn_frame = ttk.LabelFrame(main_frame, text="📡 设备连接", padding="10")
        conn_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(conn_frame, text="● 未连接", foreground=self.colors['danger'])
        self.status_label.grid(row=0, column=0, padx=5)
        
        self.port_label = ttk.Label(conn_frame, text="端口：未选择")
        self.port_label.grid(row=0, column=1, padx=5)
        
        self.connect_btn = ttk.Button(conn_frame, text="🔌 连接设备", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=2, padx=5)
        
        self.scan_btn = ttk.Button(conn_frame, text="🔍 扫描设备", command=self.scan_devices)
        self.scan_btn.grid(row=0, column=3, padx=5)
        
        # === 打印内容区域 ===
        content_frame = ttk.Notebook(main_frame)
        content_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(1, weight=1)
        
        # 标签页 1: 文字打印
        text_tab = ttk.Frame(content_frame, padding="10")
        content_frame.add(text_tab, text="📝 文字打印")
        
        ttk.Label(text_tab, text="输入要打印的文字:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.text_input = scrolledtext.ScrolledText(text_tab, height=8, width=60, wrap=tk.WORD)
        self.text_input.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        text_tab.columnconfigure(0, weight=1)
        
        ttk.Label(text_tab, text="字体大小:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.font_size_var = tk.IntVar(value=24)
        font_size_slider = ttk.Scale(text_tab, from_=8, to=72, variable=self.font_size_var, orient=tk.HORIZONTAL)
        font_size_slider.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.font_size_label = ttk.Label(text_tab, text="24 pt")
        self.font_size_label.grid(row=2, column=2, padx=5)
        font_size_slider.configure(command=lambda v: self.font_size_label.config(text=f"{int(float(v))} pt"))
        
        self.print_text_btn = ttk.Button(text_tab, text="🖨️ 打印文字", command=self.print_text)
        self.print_text_btn.grid(row=3, column=0, pady=10)
        
        # 标签页 2: 图片打印
        image_tab = ttk.Frame(content_frame, padding="10")
        content_frame.add(image_tab, text="🖼️ 图片打印")
        
        ttk.Label(image_tab, text="选择图片文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.image_path_var = tk.StringVar()
        image_entry = ttk.Entry(image_tab, textvariable=self.image_path_var, width=50)
        image_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        image_tab.columnconfigure(0, weight=1)
        
        browse_btn = ttk.Button(image_tab, text="📁 浏览...", command=self.browse_image)
        browse_btn.grid(row=1, column=2, padx=5)
        
        # 图片预览
        self.preview_label = ttk.Label(image_tab, text="暂无预览")
        self.preview_label.grid(row=2, column=0, columnspan=3, pady=10)
        
        ttk.Label(image_tab, text="处理模式:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.dither_mode_var = tk.StringVar(value="auto")
        mode_combo = ttk.Combobox(image_tab, textvariable=self.dither_mode_var, 
                                   values=["auto", "floyd", "adaptive"], state="readonly", width=15)
        mode_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        self.print_image_btn = ttk.Button(image_tab, text="🖨️ 打印图片", command=self.print_image)
        self.print_image_btn.grid(row=4, column=0, pady=10)
        
        # 标签页 3: 二维码打印
        qr_tab = ttk.Frame(content_frame, padding="10")
        content_frame.add(qr_tab, text="📱 二维码打印")
        
        ttk.Label(qr_tab, text="输入二维码内容:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.qr_input = scrolledtext.ScrolledText(qr_tab, height=6, width=60, wrap=tk.WORD)
        self.qr_input.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        qr_tab.columnconfigure(0, weight=1)
        
        self.print_qr_btn = ttk.Button(qr_tab, text="🖨️ 打印二维码", command=self.print_qrcode)
        self.print_qr_btn.grid(row=2, column=0, pady=10)
        
        # === 控制区域 ===
        control_frame = ttk.LabelFrame(main_frame, text="⚙️ 打印机控制", padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="📄 走纸", command=self.feed_paper).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="🧪 自检页", command=self.self_test).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="🔋 电量查询", command=self.query_battery).grid(row=0, column=2, padx=5)
        
        # === 日志区域 ===
        log_frame = ttk.LabelFrame(main_frame, text="📋 操作日志", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(3, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def log(self, message, level="INFO"):
        """添加日志消息"""
        timestamp = threading.current_thread().name
        formatted_msg = f"[{level}] {message}\n"
        
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, formatted_msg)
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
    
    def auto_connect(self):
        """启动时自动连接设备"""
        self.log("正在自动查找 Paperang 设备...")
        try:
            cfg = setup_config(auto_find=True)
            if cfg.get("serial_port"):
                self.log(f"找到设备端口：{cfg['serial_port']}")
                self.port_label.config(text=f"端口：{cfg['serial_port']}")
                self.connect_to_device(cfg)
            else:
                self.log("未找到设备，请手动点击「扫描设备」或「连接设备」", "WARNING")
        except Exception as e:
            self.log(f"自动连接失败：{e}", "ERROR")
    
    def scan_devices(self):
        """扫描可用设备"""
        self.log("正在扫描串口设备...")
        try:
            port = find_paperang_port()
            if port:
                self.log(f"✓ 找到 Paperang 设备：{port}")
                self.port_label.config(text=f"端口：{port}")
                messagebox.showinfo("设备发现", f"找到 Paperang 设备:\n{port}")
            else:
                self.log("✗ 未找到 Paperang 设备", "WARNING")
                messagebox.showwarning("未找到设备", "未检测到 Paperang 设备\n请确保设备已配对并开启")
        except Exception as e:
            self.log(f"扫描失败：{e}", "ERROR")
            messagebox.showerror("错误", f"扫描设备失败:\n{e}")
    
    def toggle_connection(self):
        """切换连接状态"""
        if self.connected:
            self.disconnect()
        else:
            self.connect()
    
    def connect(self):
        """连接设备"""
        cfg = load_config()
        if not cfg.get("serial_port"):
            messagebox.showwarning("提示", "请先扫描或选择设备端口")
            return
        
        self.connect_to_device(cfg)
    
    def connect_to_device(self, cfg):
        """执行连接"""
        def connect_thread():
            try:
                self.log(f"正在连接 {cfg['serial_port']}...")
                self.bt_manager = BtManager(cfg)
                
                if self.bt_manager.connected:
                    self.connected = True
                    self.root.after(0, lambda: self.update_connection_status(True, cfg['serial_port']))
                    self.root.after(0, lambda: self.log("✓ 连接成功"))
                else:
                    self.root.after(0, lambda: self.log("✗ 连接失败", "ERROR"))
                    self.root.after(0, lambda: messagebox.showerror("错误", "连接失败，请检查设备"))
            except Exception as e:
                self.root.after(0, lambda: self.log(f"连接异常：{e}", "ERROR"))
        
        thread = threading.Thread(target=connect_thread, daemon=True)
        thread.start()
    
    def disconnect(self):
        """断开连接"""
        try:
            if self.bt_manager:
                self.bt_manager.disconnect()
            self.connected = False
            self.update_connection_status(False, None)
            self.log("已断开连接")
        except Exception as e:
            self.log(f"断开连接失败：{e}", "ERROR")
    
    def update_connection_status(self, is_connected, port):
        """更新连接状态显示"""
        if is_connected:
            self.status_label.config(text="● 已连接", foreground=self.colors['success'])
            self.connect_btn.config(text="❌ 断开连接")
            self.port_label.config(text=f"端口：{port}")
        else:
            self.status_label.config(text="● 未连接", foreground=self.colors['danger'])
            self.connect_btn.config(text="🔌 连接设备")
            self.bt_manager = None
    
    def check_connection(self):
        """检查是否已连接"""
        if not self.connected or not self.bt_manager:
            messagebox.showwarning("提示", "请先连接设备")
            return False
        return True
    
    def print_text(self):
        """打印文字"""
        if not self.check_connection():
            return
        
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("提示", "请输入要打印的文字")
            return
        
        def print_thread():
            try:
                self.log("正在渲染文字...")
                font_size = self.font_size_var.get()
                bitmap_data = TextConverter.text2bmp(text, font_size=font_size)
                
                self.log("正在发送打印数据...")
                self.bt_manager.sendImageToBt(bitmap_data)
                self.log("✓ 打印任务已发送")
            except Exception as e:
                self.root.after(0, lambda: self.log(f"打印失败：{e}", "ERROR"))
                self.root.after(0, lambda: messagebox.showerror("错误", f"打印失败:\n{e}"))
        
        thread = threading.Thread(target=print_thread, daemon=True)
        thread.start()
    
    def browse_image(self):
        """浏览选择图片"""
        filetypes = [
            ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("所有文件", "*.*")
        ]
        filepath = filedialog.askopenfilename(title="选择图片", filetypes=filetypes)
        
        if filepath:
            self.image_path_var.set(filepath)
            self.show_image_preview(filepath)
    
    def show_image_preview(self, filepath):
        """显示图片预览"""
        try:
            img = Image.open(filepath)
            img.thumbnail((200, 200))
            
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo  # 保持引用
            
            self.log(f"已加载图片：{os.path.basename(filepath)} ({img.size[0]}x{img.size[1]})")
        except Exception as e:
            self.log(f"加载图片失败：{e}", "ERROR")
            self.preview_label.config(image="", text="预览失败")
    
    def print_image(self):
        """打印图片"""
        if not self.check_connection():
            return
        
        filepath = self.image_path_var.get().strip()
        if not filepath or not os.path.exists(filepath):
            messagebox.showwarning("提示", "请选择有效的图片文件")
            return
        
        mode = self.dither_mode_var.get()
        
        def print_thread():
            try:
                self.log(f"正在处理图片 (模式：{mode})...")
                bitmap_data = ImageConverter.process_image_for_printing_with_mode(filepath, mode)
                
                self.log("正在发送打印数据...")
                self.bt_manager.sendImageToBt(bitmap_data)
                self.log("✓ 打印任务已发送")
            except Exception as e:
                self.root.after(0, lambda: self.log(f"打印失败：{e}", "ERROR"))
                self.root.after(0, lambda: messagebox.showerror("错误", f"打印失败:\n{e}"))
        
        thread = threading.Thread(target=print_thread, daemon=True)
        thread.start()
    
    def print_qrcode(self):
        """打印二维码"""
        if not self.check_connection():
            return
        
        content = self.qr_input.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("提示", "请输入二维码内容")
            return
        
        def print_thread():
            try:
                self.log("正在生成二维码...")
                bitmap_data = ImageConverter.generate_qr_code(content)
                
                self.log("正在发送打印数据...")
                self.bt_manager.sendImageToBt(bitmap_data)
                self.log("✓ 打印任务已发送")
            except Exception as e:
                self.root.after(0, lambda: self.log(f"打印失败：{e}", "ERROR"))
                self.root.after(0, lambda: messagebox.showerror("错误", f"打印失败:\n{e}"))
        
        thread = threading.Thread(target=print_thread, daemon=True)
        thread.start()
    
    def feed_paper(self):
        """走纸"""
        if not self.check_connection():
            return
        
        def feed_thread():
            try:
                self.log("正在走纸...")
                self.bt_manager.sendFeedLineToBt(50)
                self.log("✓ 走纸完成")
            except Exception as e:
                self.root.after(0, lambda: self.log(f"走纸失败：{e}", "ERROR"))
        
        thread = threading.Thread(target=feed_thread, daemon=True)
        thread.start()
    
    def self_test(self):
        """打印自检页"""
        if not self.check_connection():
            return
        
        def test_thread():
            try:
                self.log("正在发送自检命令...")
                self.bt_manager.sendSelfTestToBt()
                self.log("✓ 自检页打印中")
            except Exception as e:
                self.root.after(0, lambda: self.log(f"自检失败：{e}", "ERROR"))
        
        thread = threading.Thread(target=test_thread, daemon=True)
        thread.start()
    
    def query_battery(self):
        """查询电量"""
        if not self.check_connection():
            return
        
        def query_thread():
            try:
                self.log("正在查询电量...")
                # 注意：实际实现需要解析返回数据
                self.bt_manager.queryBatteryStatus()
                self.log("✓ 电量查询命令已发送 (查看设备响应)")
            except Exception as e:
                self.root.after(0, lambda: self.log(f"查询失败：{e}", "ERROR"))
        
        thread = threading.Thread(target=query_thread, daemon=True)
        thread.start()
    
    def on_closing(self):
        """窗口关闭时的清理"""
        if self.connected:
            self.disconnect()
        self.root.destroy()


def main():
    """主函数"""
    if not TKINTER_AVAILABLE:
        print("❌ 无法启动 GUI：tkinter 不可用")
        print("\n💡 安装方法:")
        print("   MacOS:  brew install python-tk")
        print("   Windows: 重新运行 Python 安装程序，勾选 'tcl/tk and IDLE'")
        print("   Linux:  sudo apt-get install python3-tk\n")
        print("🔄 将使用命令行交互模式...")
        from paperang.interactive import main as interactive_main
        interactive_main()
        return
    
    root = tk.Tk()
    app = PaperangGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
