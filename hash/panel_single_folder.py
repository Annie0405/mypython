from hash.deduplicate_single_folder import deduplicate_single_folder
import tkinter as tk


def deduplicate(entry):
    path = entry.get()
    deduplicate_single_folder(path)


def panel_single_folder():
    # 实例化窗口
    root = tk.Tk()

    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 添加窗口标题
    root.title("单文件夹去重")

    # 窗口大小和位置
    window_width = int(screen_width * 0.3)
    window_height = int(screen_height * 0.15)
    axis_x = int((screen_width - window_width) / 2)
    axis_y = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    # 第一行：标签、文本框
    frame = tk.Frame(root, width=window_width)
    frame.place(relx=0.5, rely=0.35, anchor="center")

    label = tk.Label(frame, text="文件夹路径：")
    label.pack(side="left")

    entry_width = int(window_width * 0.1)   # 文本框可容纳字符数
    entry = tk.Entry(frame, width=entry_width)
    entry.pack(side="left")

    # 第二行：按钮，居中显示
    deduplicate_button = tk.Button(root, text="开始去重", command=lambda: deduplicate(entry))
    deduplicate_button.place(relx=0.5, rely=0.7, anchor="center")

    # 显示主窗口
    root.mainloop()

