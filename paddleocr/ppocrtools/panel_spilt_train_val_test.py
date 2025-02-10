import tkinter as tk
from paddleocr.ppocrtools.split_train_val_test import split


class TrainValTestSplitterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # 添加窗口标题
        self.root.title("训练集划分")
        # 窗口大小和位置
        window_width = 700
        window_height = 450
        axis_x = int((screen_width - window_width) / 2)
        axis_y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    def _create_frames(self):
        # 上方的 frame 用于输入路径
        self.frame_path = tk.Frame(self.root, highlightcolor='#DCDCDC',
                                   highlightbackground='#DCDCDC', highlightthickness=1,
                                   width=600, height=200)
        self.frame_path.place(x=50, y=20)
        self.frame_path.pack_propagate(False)
        # 左下方的 frame 用于输入划分训练集的比例
        self.frame_scale = tk.Frame(self.root, highlightcolor='#DCDCDC',
                                    highlightbackground='#DCDCDC', highlightthickness=1,
                                    width=300, height=150)
        self.frame_scale.place(x=50, y=240)
        self.frame_scale.pack_propagate(False)
        # 右下方的 frame 用于选择模式 det/rec
        self.frame_mode = tk.Frame(self.root, highlightcolor='#DCDCDC',
                                   highlightbackground='#DCDCDC', highlightthickness=1,
                                   width=300, height=150)
        self.frame_mode.place(x=350, y=240)
        self.frame_mode.pack_propagate(False)

    def _create_widgets(self):
        # 输入路径相关组件
        self._create_path_input()
        # 训练集比例输入相关组件
        self._create_scale_input()
        # 模式选择相关组件
        self._create_mode_selector()
        # 底部按钮
        button = tk.Button(self.root, text="开始划分",
                           command=lambda: self._start_split())
        button.place(x=350, y=420, anchor="center")

    def _create_path_input(self):
        # 文件存放根目录的 frame
        frame_root_dir = tk.Frame(self.frame_path)
        frame_root_dir.pack(side="top", padx=15, pady=15)

        label_root_dir = tk.Label(frame_root_dir, text="文件存放根目录：", width=15)
        label_root_dir.pack(side="left")

        entry_root_dir = tk.Entry(frame_root_dir, width=70)
        entry_root_dir.pack(side="left")
        self.entries["root_dir"] = entry_root_dir

        # 服务器存放目录的 frame
        frame_server_dir = tk.Frame(self.frame_path)
        frame_server_dir.pack(side="top", padx=15)

        label_server_dir = tk.Label(frame_server_dir, text="服务器存放目录：", width=15)
        label_server_dir.pack(side="left")

        entry_server_dir = tk.Entry(frame_server_dir, width=70)
        entry_server_dir.pack(side="left")
        self.entries["server_dir"] = entry_server_dir

        # 目录构造提示
        label_tips = tk.Label(self.frame_path,
                              text="“文件存放根目录”下必须有一个名为 0_original_data 的文件夹；\n"
                                   + "0_original_data 文件夹中存放所有图片和名为 Label.txt/rec_gt.txt 的标签文件；\n"
                                   + "图片数量必须是10的倍数；\n"
                                   + "标签文件每行第一个元素必须是不含路径的文件名；\n"
                                   + "“服务器存放目录”是训练集划分后生成的标签内容的前缀，结尾不要斜杠！")
        label_tips.pack(side="top", padx=15, pady=15)

    def _create_scale_input(self):
        # 训练集划分比例提示
        label_tips = tk.Label(self.frame_scale,
                              text="填入的三个数必须是整数，且和为10；\n若不需要测试集，可置空。")
        label_tips.pack(side="top", pady=(10, 5))
        # 训练集划分比例输入
        frame_train = tk.Frame(self.frame_scale)
        frame_train.pack(side="top", padx=15, pady=(0, 5))
        frame_val = tk.Frame(self.frame_scale)
        frame_val.pack(side="top", padx=15, pady=(0, 5))
        frame_test = tk.Frame(self.frame_scale)
        frame_test.pack(side="top", padx=15, pady=(0, 10))
        scales = [("train:", "train", frame_train), ("val:", "val", frame_val), ("test:", "test", frame_test)]
        for label, key, frame in scales:
            label_scale = tk.Label(frame, text=label, width=5)
            label_scale.pack(side="left")
            entry_scale = tk.Entry(frame, width=5)
            entry_scale.pack(side="left")
            self.entries[key] = entry_scale

    def _create_mode_selector(self):
        def set_value(var, value):
            var.set(value)

        frame_radiobutton = tk.Frame(self.frame_mode)
        frame_radiobutton.pack(expand=True)

        radio_var = tk.StringVar()
        radio_det = tk.Radiobutton(frame_radiobutton, text="det", variable=radio_var, value="det",
                                   command=lambda: set_value(radio_var, 'det'))
        radio_det.pack()
        radio_rec = tk.Radiobutton(frame_radiobutton, text="rec", variable=radio_var, value="rec",
                                   command=lambda: set_value(radio_var, 'rec'))
        radio_rec.pack()
        self.entries["mode"] = radio_var

    def _start_split(self):
        root_dir = self.entries["root_dir"].get()
        server_dir = self.entries["server_dir"].get()
        train = self.entries["train"].get()
        val = self.entries["val"].get()
        test = self.entries["test"].get()
        mode = self.entries["mode"].get()
        split(root_dir, server_dir, train, val, test, mode)
