from fileprocess.rand_move_files import rand_move_files
import tkinter as tk


def move(entry_src, entry_dst, entry_num):
    path_src = entry_src.get()
    path_dst = entry_dst.get()
    num = int(entry_num.get())
    rand_move_files(path_src, path_dst, num)


def panel_rand_move():
    # 实例化窗口
    root = tk.Tk()

    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 添加窗口标题
    root.title("随机移动文件")

    # 窗口大小和位置
    window_width = int(screen_width * 0.3)
    window_height = int(screen_height * 0.15)
    axis_x = int((screen_width - window_width) / 2)
    axis_y = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    # 第一行：源文件夹
    frame = tk.Frame(root, width=window_width)
    frame.place(relx=0.5, rely=0.2, anchor="center")

    label = tk.Label(frame, text="源文件夹：")
    label.pack(side="left")

    entry_width = int(window_width * 0.1)  # 文本框可容纳字符数
    entry_src = tk.Entry(frame, width=entry_width)
    entry_src.pack(side="left")

    # 第二行：目标文件夹
    frame = tk.Frame(root, width=window_width)
    frame.place(relx=0.5, rely=0.4, anchor="center")

    label = tk.Label(frame, text="目标文件夹：")
    label.pack(side="left")

    entry_width = int(window_width * 0.1)  # 文本框可容纳字符数
    entry_dst = tk.Entry(frame, width=entry_width)
    entry_dst.pack(side="left")

    # 第三行：要移动的文件数量
    frame = tk.Frame(root, width=window_width)
    frame.place(relx=0.5, rely=0.6, anchor="center")

    label = tk.Label(frame, text="随机移动的文件数量：")
    label.pack(side="left")

    entry_width = int(window_width * 0.05)  # 文本框可容纳字符数
    entry_num = tk.Entry(frame, width=entry_width)
    entry_num.pack(side="left")

    # 第四行：按钮，居中显示
    move_button = tk.Button(root, text="移动", command=lambda: move(entry_src, entry_dst, entry_num))
    move_button.place(relx=0.5, rely=0.8, anchor="center")

    # 显示主窗口
    root.mainloop()
