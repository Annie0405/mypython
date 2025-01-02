import tkinter as tk
from split_train_val_test import split_train_val_test


def split(entry_root_dir, entry_server_dir, entry_train, entry_val, entry_test, radio_var):
    root_dir = entry_root_dir.get()
    server_dir = entry_server_dir.get()
    train = entry_train.get()
    val = entry_val.get()
    test = entry_test.get()
    option = radio_var.get()
    split_train_val_test(root_dir, server_dir, train, val, test, option)


def panel_split_train_val_test():
    # 实例化窗口
    root = tk.Tk()

    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 添加窗口标题
    root.title("训练集划分")

    # 窗口大小和位置
    window_width = int(screen_width * 0.35)
    window_height = int(screen_height * 0.4)
    axis_x = int((screen_width - window_width) / 2)
    axis_y = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    # 1. 第一个 frame 用于输入路径
    frame_width = int(0.8 * window_width)
    entry_width = int(0.1 * window_width)

    frame_path = tk.Frame(root, width=frame_width,
                          highlightbackground='#DCDCDC', highlightthickness=1)
    frame_path.place(relx=0.5, rely=0.25, anchor="center")

    # 文件存放根目录的 frame
    frame_root_dir = tk.Frame(frame_path, width=frame_width)
    frame_root_dir.pack(side="top", padx=15, pady=15)

    label_root_dir = tk.Label(frame_root_dir, text="文件存放根目录：")
    label_root_dir.pack(side="left")

    entry_root_dir = tk.Entry(frame_root_dir, width=entry_width)
    entry_root_dir.pack(side="left")

    # 服务器存放目录的 frame
    frame_server_dir = tk.Frame(frame_path, width=frame_width)
    frame_server_dir.pack(side="top", padx=15)

    label_server_dir = tk.Label(frame_server_dir, text="服务器存放目录：")
    label_server_dir.pack(side="left")

    entry_server_dir = tk.Entry(frame_server_dir, width=entry_width)
    entry_server_dir.pack(side="left")

    # 目录构造提示
    label_tips = tk.Label(frame_path,
                          text="“文件存放根目录”下必须有一个名为 0_original_data 的文件夹；\n"
                          + "0_original_data 文件夹中存放所有图片和名为 Label.txt/rec_gt.txt 的标签文件；\n"
                          + "图片数量必须是10的倍数；\n"
                          + "标签文件每行第一个元素必须是不含路径的文件名；\n"
                          + "“服务器存放目录”是训练集划分后生成的标签内容的前缀，结尾不要斜杠！")
    label_tips.pack(side="top", padx=15, pady=15)

    # 2. 第二个 frame 用于输入 train : val : test
    frame_width = int(0.4 * window_width)
    frame_height = int(0.35 * window_height)
    entry_width = 5

    frame_scale = tk.Frame(root, width=frame_width, height=frame_height,
                           highlightbackground='#DCDCDC', highlightthickness=1)
    frame_scale.place(relx=0.25, rely=0.675, anchor="center")
    frame_scale.pack_propagate(False)

    # 训练集划分比例提示
    label_tips = tk.Label(frame_scale,
                          text="填入的三个数必须是整数，且和为10；\n"
                          + "若不需要测试集，可置空。")
    label_tips.pack(side="top", pady=(10, 5))

    # 训练集划分比例输入
    frame_train = tk.Frame(frame_scale, width=frame_width)
    frame_train.pack(side="top", padx=15, pady=(0, 5))

    frame_val = tk.Frame(frame_scale, width=frame_width)
    frame_val.pack(side="top", padx=15, pady=(0, 5))

    frame_test = tk.Frame(frame_scale, width=frame_width)
    frame_test.pack(side="top", padx=15, pady=(0, 10))

    label_train = tk.Label(frame_train, text="train:", width=entry_width)
    label_train.pack(side="left")
    entry_train = tk.Entry(frame_train, width=entry_width)
    entry_train.pack(side="left")

    label_val = tk.Label(frame_val, text="  val:", width=entry_width)
    label_val.pack(side="left")
    entry_val = tk.Entry(frame_val, width=entry_width)
    entry_val.pack(side="left")

    label_test = tk.Label(frame_test, text=" test:", width=entry_width)
    label_test.pack(side="left")
    entry_test = tk.Entry(frame_test, width=entry_width)
    entry_test.pack(side="left")

    # 3. 第三个 frame 用于选择模式 det/rec
    frame_mode = tk.Frame(root, width=frame_width, height=frame_height,
                          highlightbackground='#DCDCDC', highlightthickness=1)
    frame_mode.place(relx=0.75, rely=0.675, anchor="center")
    frame_mode.grid_propagate(False)

    # 划分一个 6×3 的网格
    for i in range(6):
        frame_mode.grid_rowconfigure(i, weight=1)
    for i in range(3):
        frame_mode.grid_columnconfigure(i, weight=1)

    # 单选按钮
    def set_value(var, value):
        var.set(value)

    radio_var = tk.StringVar()
    radio_det = tk.Radiobutton(frame_mode, text="det", variable=radio_var, value="det",
                               command=lambda: set_value(radio_var, 'det'))
    radio_det.grid(row=2, column=1)
    radio_rec = tk.Radiobutton(frame_mode, text="rec", variable=radio_var, value="rec",
                               command=lambda: set_value(radio_var, 'rec'))
    radio_rec.grid(row=3, column=1)

    # 4. 底部按钮启动划分程序
    button = tk.Button(root, text="开始划分",
                       command=lambda: split(entry_root_dir, entry_server_dir,
                                             entry_train, entry_val, entry_test, radio_var))
    button.place(relx=0.5, rely=0.9, anchor="center")

    # 显示主窗口
    root.mainloop()
