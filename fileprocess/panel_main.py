"""
文件操作脚本的可视化面板
集成所有文件操作功能
"""
from panel_rand_move import panel_rand_move
from panel_merge_dir import DirMergeApp
import tkinter as tk

# 实例化窗口
root = tk.Tk()

# 获取屏幕尺寸
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 添加窗口标题
root.title("文件操作")

# 窗口大小和位置
window_width = int(screen_width * 0.2)
window_height = int(screen_height * 0.2)
axis_x = int((screen_width - window_width) / 2)
axis_y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

# 配置网格行和列的权重，确保按钮居中
for i in range(4):
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)  # 居中列

# 按键宽度
button_width = 12

# 随机移动文件
button_rand_move = tk.Button(root, text="随机移动文件", width=button_width, command=panel_rand_move)
button_rand_move.grid(row=1, column=0)

# 文件夹合并
button_merge_dir = tk.Button(root, text="文件夹合并", width=button_width, command=lambda: DirMergeApp())
button_merge_dir.grid(row=2, column=0)

# 显示主窗口
root.mainloop()
