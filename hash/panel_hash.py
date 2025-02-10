"""
哈希脚本的可视化面板
集成所有哈希功能
"""
from hash.panel_single_folder import panel_single_folder
from hash.panel_multi_folders import panel_multi_folders
import tkinter as tk


class HashApp:
    def __init__(self):
        # 实例化窗口
        root = tk.Tk()

        # 获取屏幕尺寸
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 添加窗口标题
        root.title("文件去重")

        # 窗口大小和位置
        window_width = int(screen_width * 0.2)
        window_height = int(screen_height * 0.2)
        axis_x = int((screen_width - window_width) / 2)
        axis_y = int((screen_height - window_height) / 2)
        root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

        # 配置网格行和列的权重，确保按钮居中
        root.grid_rowconfigure(0, weight=1)  # 顶部留空
        root.grid_rowconfigure(1, weight=1)  # 中间按钮行
        root.grid_rowconfigure(2, weight=1)  # 中间按钮行
        root.grid_rowconfigure(3, weight=1)  # 底部留空
        root.grid_columnconfigure(0, weight=1)  # 居中列

        # 创建按钮
        button_single_folder = tk.Button(root, text="单文件夹去重", command=panel_single_folder)
        button_multi_folders = tk.Button(root, text="三文件夹去重", command=panel_multi_folders)
        button_single_folder.grid(row=1, column=0)
        button_multi_folders.grid(row=2, column=0)

        # 显示主窗口
        root.mainloop()
