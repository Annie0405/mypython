import tkinter as tk


def setup_window(window, title, width, height):
    # 获取屏幕尺寸
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # 添加窗口标题
    window.title(title)
    # 窗口大小和位置
    axis_x = int((screen_width - width) / 2)
    axis_y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{axis_x}+{axis_y}")
