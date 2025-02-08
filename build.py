import PyInstaller.__main__
import os
from datetime import datetime

def build_exe():
    # 获取当前日期，格式为YYYYMMDD
    current_date = datetime.now().strftime('%Y%m%d')
    
    # 组合文件名：WXMulti_YYYYMMDD
    exe_name = f'WXMulti_{current_date}'
    
    PyInstaller.__main__.run([
        'main.py',  # 您的主程序文件
        f'--name={exe_name}',  # 生成的exe文件名带日期
        '--onefile',  # 打包成单个exe文件
        '--noconsole',  # 运行时不显示控制台窗口
        '--clean',  # 清理临时文件
        '--add-data=assets;assets',  # 如果有资源文件，请相应修改
        '--icon=assets/icon.png',  # 如果有图标文件，请相应修改
    ])

if __name__ == '__main__':
    build_exe() 