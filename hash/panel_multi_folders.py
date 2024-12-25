from deduplicate_multi_folders import deduplicate_multiple_folders
import tkinter as tk


def deduplicate(entry_a, entry_b, entry_c):
    path_a = entry_a.get()
    path_b = entry_b.get()
    path_c = entry_c.get()
    deduplicate_multiple_folders(path_a, path_b, path_c)


def panel_multi_folders():
    # 实例化窗口
    root = tk.Tk()

    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 添加窗口标题
    root.title("三文件夹去重")

    # 窗口大小和位置
    window_width = int(screen_width * 0.45)
    window_height = int(screen_height * 0.2)
    axis_x = int((screen_width - window_width) / 2)
    axis_y = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    # 第一行：提示语，居中
    label_tip = tk.Label(root, text="目标文件夹 = 源文件夹 - 对比文件夹", font=("Arial", 12, "bold"))
    label_tip.place(relx=0.5, rely=0.15, anchor="center")

    # 第二、三、四行的纵坐标和间距
    rely = 0.3
    bias_y = 0.15

    # 输入框宽度
    entry_width = int(window_width * 0.1)   # 文本框可容纳字符数

    # 第二行：源文件夹
    frame_a = tk.Frame(root, width=window_width)
    frame_a.place(relx=0.5, rely=rely, anchor="center")

    label_a = tk.Label(frame_a, text="源文件夹：")
    label_a.pack(side="left")

    entry_a = tk.Entry(frame_a, width=entry_width)
    entry_a.pack(side="left")

    # 第三行：对比文件夹
    frame_b = tk.Frame(root, width=window_width)
    frame_b.place(relx=0.5, rely=rely+bias_y, anchor="center")

    label_b = tk.Label(frame_b, text="对比文件夹：")
    label_b.pack(side="left")

    entry_b = tk.Entry(frame_b, width=entry_width)
    entry_b.pack(side="left")

    # 第四行：目标文件夹
    frame_c = tk.Frame(root, width=window_width)
    frame_c.place(relx=0.5, rely=rely+bias_y*2, anchor="center")

    label_c = tk.Label(frame_c, text="目标文件夹：")
    label_c.pack(side="left")

    entry_c = tk.Entry(frame_c, width=entry_width)
    entry_c.pack(side="left")

    # 第五行：按钮，居中显示
    deduplicate_button = tk.Button(root, text="开始去重", command=lambda: deduplicate(entry_a, entry_b, entry_c))
    deduplicate_button.place(relx=0.5, rely=0.8, anchor="center")

    # 显示主窗口
    root.mainloop()

