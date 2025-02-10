import os.path
import tkinter as tk
from labelme.labelme2COCO_split import Labelme2COCOSplit
from tkbuilder.panel_settings import setup_window


class Labelme2COCOSplitApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "labelme标注一键转COCO格式并划分", 720, 460)

    def _create_frames(self):
        # 提示框的 frame
        self.frame_tips = tk.Frame(self.root, width=650, height=50)
        self.frame_tips.place(x=35, y=20)
        # 文件存放根目录的 frame
        self.frame_root_dir = tk.Frame(self.root, width=650, height=30)
        self.frame_root_dir.place(x=35, y=80)
        self.frame_root_dir.pack_propagate(False)
        # 树形结构图的 frame
        self.frame_tree = tk.Frame(self.root, width=650, height=220)
        self.frame_tree.place(x=35, y=115)
        # 分隔符
        self.frame_sep = tk.Frame(self.root, highlightcolor='#DCDCDC', highlightbackground='#DCDCDC',
                                  highlightthickness=1, width=650, height=1)
        self.frame_sep.place(x=35, y=330)
        # 分割提示的 frame
        self.frame_split_tips = tk.Frame(self.root, width=650, height=30)
        self.frame_split_tips.place(x=35, y=340)
        self.frame_split_tips.pack_propagate(False)
        # 分割比例的 frame
        self.frame_scale = tk.Frame(self.root, width=650, height=30)
        self.frame_scale.place(x=35, y=370)
        self.frame_scale.pack_propagate(False)
        # 底部按钮的 frame
        self.frame_button = tk.Frame(self.root, width=650, height=50)
        self.frame_button.place(x=35, y=400)

    def _create_widgets(self):
        # 提示文本
        label_tips = tk.Label(self.frame_tips,
                              text="*图片数量必须是10的倍数\n"
                                   + "*先构建好categories，保存在COCO路径下的categories_file.json文件中\n"
                                   + "categories需包含属性id, name, supercategory, iscrowd")
        label_tips.place(relx=0.5, rely=0.5, anchor="center")
        # 文件存放根目录的组件
        label_root_dir = tk.Label(self.frame_root_dir, text="文件存放根目录：", anchor='e', width=15)
        label_root_dir.pack(side="left")
        entry_root_dir = tk.Entry(self.frame_root_dir, width=75)
        entry_root_dir.pack(side="left")
        self.entries["root_dir"] = entry_root_dir
        # 树形结构图
        label_tree = tk.Label(self.frame_tree,
                              text=
                              "root_dir/\n" +
                              "├────0_original_data_labelme/\n" +
                              "├────1_original_data_COCO/\n" +
                              "│            ├────annotations/\n" +
                              "│            │            └────annotations_coco.json\n"
                              "│            ├────images/\n" +
                              "│            │            ├────image000.jpg\n" +
                              "│            │            ├────image001.jpg\n" +
                              "│            │            ├────image002.jpg\n" +
                              "│            │            └────......\n" +
                              "│            └────categories_file.json/\n" +
                              "└────2_labels/\n",
                              justify="left")
        label_tree.place(relx=0.5, rely=0.5, anchor="center")
        # 分割提示
        label_split_tips = tk.Label(self.frame_split_tips, text="填入的三个数必须是整数，且和为10；若不需要测试集，可置空")
        label_split_tips.pack()
        # 分割比例输入
        frame_train = tk.Frame(self.frame_scale)
        frame_train.place(relx=0.3, rely=0.5, anchor="center")
        frame_val = tk.Frame(self.frame_scale)
        frame_val.place(relx=0.5, rely=0.5, anchor="center")
        frame_test = tk.Frame(self.frame_scale)
        frame_test.place(relx=0.7, rely=0.5, anchor="center")
        scales = [("train:", "train", frame_train), ("val:", "val", frame_val), ("test:", "test", frame_test)]
        for label, key, frame in scales:
            label_scale = tk.Label(frame, text=label, width=5)
            label_scale.pack(side="left")
            entry_scale = tk.Entry(frame, width=5)
            entry_scale.pack(side="left")
            self.entries[key] = entry_scale
        # 底部按钮
        button_verify = tk.Button(self.frame_button, text="校验", command=self.verify, width=10)
        button_verify.place(relx=0.35, rely=0.5, anchor="center")
        button_start = tk.Button(self.frame_button, text="开始分割", command=self.start_split, width=10)
        button_start.place(relx=0.65, rely=0.5, anchor="center")

    def verify(self):
        root_dir = self.entries["root_dir"].get()
        labelme_dir = os.path.join(root_dir, "0_original_data_labelme")
        Labelme2COCOSplit.verify(labelme_dir)

    def start_split(self):
        root_dir = self.entries["root_dir"].get()
        train = self.entries["train"].get()
        val = self.entries["val"].get()
        test = self.entries["test"].get()
        Labelme2COCOSplit(root_dir, {"train": train, "val": val, "test": test})
