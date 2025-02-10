import tkinter as tk
from yolo.augment import augment
from tkbuilder.panel_settings import setup_window


class AugmentApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "yolo数据增强", 720, 200)

    def _create_frames(self):
        # labelme标注路径的 frame
        self.frame_input = tk.Frame(self.root, width=600, height=30)
        self.frame_input.place(x=50, y=20)
        self.frame_input.pack_propagate(False)
        # COCO标注存放路径的 frame
        self.frame_output = tk.Frame(self.root, width=600, height=30)
        self.frame_output.place(x=50, y=60)
        self.frame_output.pack_propagate(False)
        # 提示框的 frame
        self.frame_tips = tk.Frame(self.root, width=600, height=40)
        self.frame_tips.place(x=50, y=100)
        # 按钮的 frame
        self.frame_button = tk.Frame(self.root, width=600, height=30)
        self.frame_button.place(x=50, y=150)

    def _create_widgets(self):
        # labelme标注路径的组件
        label_input = tk.Label(self.frame_input, text="输入路径：", anchor='e', width=12)
        label_input.pack(side="left")
        entry_input = tk.Entry(self.frame_input, width=70)
        entry_input.pack(side="left")
        self.entries["in_dir"] = entry_input

        # COCO标注存放路径相关组件
        label_output = tk.Label(self.frame_output, text="输出路径：", anchor='e', width=12)
        label_output.pack(side="left")
        entry_output = tk.Entry(self.frame_output, width=70)
        entry_output.pack(side="left")
        self.entries["out_dir"] = entry_output
        # 提示框
        label_tips = tk.Label(self.frame_tips,
                              text="随机对图片进行裁剪、旋转、水平翻转，随机调整对比度、亮度，并且更新yolo标签\n"
                                   + "作用对象是yolo数据集")
        label_tips.place(relx=0.5, rely=0.5, anchor="center")
        # 底部按钮
        button_start = tk.Button(self.frame_button, text="开始增强", width=10, command=self.start_augment)
        button_start.place(relx=0.5, rely=0.5, anchor="center")

    def start_augment(self):
        in_dir = self.entries["in_dir"].get()
        out_dir = self.entries["out_dir"].get()
        augment(in_dir, out_dir)
