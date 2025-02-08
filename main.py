import tkinter as tk
from tkinter import ttk
import winreg
import os
import subprocess

class WeChatPathFinder:
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("WXMulti 微信多开启动器")
        self.root.geometry("460x220")
        self.root.resizable(False, False)  # 禁止调整窗口大小
        
        # 创建界面元素
        self.create_widgets()
        
        # 自动获取微信信息
        self.get_wechat_info()
        
    def create_widgets(self):
        # 创建标签和文本框
        info_frame = ttk.LabelFrame(self.root, text="微信信息", padding=(15, 10))
        info_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        # 设置网格列的权重
        info_frame.grid_columnconfigure(1, weight=1)
        
        # 安装路径
        ttk.Label(info_frame, text="安装路径:", width=10).grid(row=0, column=0, sticky="w", pady=3)
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(info_frame, textvariable=self.path_var, width=45)
        path_entry.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=3)
        path_entry.config(state='readonly')
        
        # 版本信息
        ttk.Label(info_frame, text="版本:", width=10).grid(row=1, column=0, sticky="w", pady=3)
        self.version_var = tk.StringVar()
        version_entry = ttk.Entry(info_frame, textvariable=self.version_var, width=45)
        version_entry.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=3)
        version_entry.config(state='readonly')
        
        # 程序名称
        ttk.Label(info_frame, text="程序名称:", width=10).grid(row=2, column=0, sticky="w", pady=3)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.name_var, width=45)
        name_entry.grid(row=2, column=1, sticky="ew", padx=(5, 0), pady=3)
        name_entry.config(state='readonly')
        
        # 添加多开控制面板
        control_frame = ttk.LabelFrame(self.root, text="多开控制", padding=(15, 10))
        control_frame.pack(fill="x", padx=15, pady=5)
        
        # 添加数量输入框和启动按钮到同一行
        ttk.Label(control_frame, text="打开数量:", width=10).grid(row=0, column=0, sticky="w")
        
        # 数量输入框
        self.count_var = tk.StringVar(value="2")
        count_entry = ttk.Entry(control_frame, textvariable=self.count_var, width=8)
        count_entry.grid(row=0, column=1, padx=(5, 15))
        
        # 验证函数：只允许输入数字，限制最大值为10
        def validate_number(P):
            if P == "": return True
            return P.isdigit() and 1 <= int(P) <= 10
        
        vcmd = (self.root.register(validate_number), '%P')
        count_entry.config(validate='key', validatecommand=vcmd)
        
        # 启动按钮
        launch_btn = ttk.Button(control_frame, text="启动微信", command=self.launch_wechat, width=15)
        launch_btn.grid(row=0, column=2, padx=(10, 0))
        
        # 状态提示标签 - 移到按钮后面
        self.status_var = tk.StringVar()
        status_label = ttk.Label(control_frame, textvariable=self.status_var, foreground="gray")
        status_label.grid(row=0, column=3, padx=(10, 0))

    def get_wechat_info(self):
        try:
            # 打开注册表键
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\WeChat",
                0,
                winreg.KEY_READ
            )
            
            # 获取各项信息
            install_location = winreg.QueryValueEx(key, "InstallLocation")[0]
            version = winreg.QueryValueEx(key, "DisplayVersion")[0]
            name = winreg.QueryValueEx(key, "DisplayName")[0]
            uninstall_string = winreg.QueryValueEx(key, "UninstallString")[0]
            
            # 更新界面显示
            self.path_var.set(install_location)
            self.version_var.set(version)
            self.name_var.set(name)
            
            winreg.CloseKey(key)
        except WindowsError:
            self.path_var.set("未找到微信安装信息")
            self.version_var.set("未知")
            self.name_var.set("未知")
    
    def launch_wechat(self):
        try:
            wechat_path = self.path_var.get()
            if wechat_path == "未找到微信安装信息":
                self.status_var.set("启动失败")
                return
                
            exe_path = os.path.join(wechat_path, "WeChat.exe")
            if not os.path.exists(exe_path):
                self.status_var.set("启动失败")
                return
                
            count = int(self.count_var.get())
            for _ in range(count):
                subprocess.Popen([exe_path])
                
            self.status_var.set("启动成功")
            
        except Exception as e:
            self.status_var.set("启动失败")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WeChatPathFinder()
    app.run() 