import tkinter as tk
from coco.split_train_data import TrainDataSplit
from tkbuilder.panel_settings import setup_window


class TrainDataSpiltApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "COCO格式训练集分割", 720, 450)

    def _create_frames(self):
        # 文件路径及文件目录格式
        self.frame_file = tk.Frame(self.root, width=620, height=250)
        self.frame_file.place(x=50, y=20)
        self.frame_file.pack_propagate(False)
        # 分隔符
        self.frame_sep = tk.Frame(self.root, highlightcolor='#DCDCDC',
                                  highlightbackground='#DCDCDC', highlightthickness=1,
                                  width=620, height=1)
        self.frame_sep.place(x=50, y=270)
        # 分割比例
        self.frame_scale = tk.Frame(self.root, width=620, height=100)
        self.frame_scale.place(x=50, y=290)
        self.frame_file.pack_propagate(False)

    def _create_widgets(self):
        # 文件提示
        label_tips1 = tk.Label(self.frame_file, text="*图片数量必须是10的倍数")
        label_tips1.pack()
        # 文件存放根目录
        frame_path = tk.Frame(self.frame_file, width=620)
        frame_path.pack(pady=10)
        label_path = tk.Label(frame_path, text="文件存放根目录：", width=15)
        label_path.pack(side="left")
        entry_path = tk.Entry(frame_path, width=70)
        entry_path.pack(side="left")
        self.entries["root_dir"] = entry_path
        # 文件目录格式提示
        label_tips2 = tk.Label(self.frame_file,
                               text=
                               "root_dir/\n" +
                               "├────1_original_data_COCO/\n" +
                               "│    ├────annotations/\n" +
                               "│    │    └────annotations_coco.json\n"
                               "│    └────images/\n" +
                               "│         ├────image000.jpg\n" +
                               "│         ├────image001.jpg\n" +
                               "│         ├────image002.jpg\n" +
                               "│         └────......\n" +
                               "└────2_labels/\n",
                               justify="left")
        label_tips2.pack()

        # 分割提示
        label_split = tk.Label(self.frame_scale, text="填入的三个数必须是整数，且和为10；若不需要测试集，可置空")
        label_split.pack()
        # 分割比例输入
        frame_scale_entry = tk.Frame(self.frame_scale, width=620, height=30)
        frame_scale_entry.pack(pady=(15, 0))
        frame_train = tk.Frame(frame_scale_entry)
        frame_train.place(relx=0.3, rely=0.5, anchor="center")
        frame_val = tk.Frame(frame_scale_entry)
        frame_val.place(relx=0.5, rely=0.5, anchor="center")
        frame_test = tk.Frame(frame_scale_entry)
        frame_test.place(relx=0.7, rely=0.5, anchor="center")
        scales = [("train:", "train", frame_train), ("val:", "val", frame_val), ("test:", "test", frame_test)]
        for label, key, frame in scales:
            label_scale = tk.Label(frame, text=label, width=5)
            label_scale.pack(side="left")
            entry_scale = tk.Entry(frame, width=5)
            entry_scale.pack(side="left")
            self.entries[key] = entry_scale

        # 底部按钮
        button_start = tk.Button(self.root, text="开始分割", command=self.start_split)
        button_start.place(relx=0.5, y=400, anchor="center")

    def start_split(self):
        root_dir = self.entries["root_dir"].get()
        split_scale = {"train": self.entries["train"].get(),
                       "val": self.entries["val"].get(),
                       "test": self.entries["test"].get()}
        TrainDataSplit(root_dir, split_scale)
