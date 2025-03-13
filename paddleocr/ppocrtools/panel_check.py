import tkinter as tk
from tkinter import ttk
from paddleocr.ppocrtools.det_process import check_det_labels
# from paddleocr.ppocrtools.rec_process import check_rec_labels
from tkbuilder.panel_settings import setup_window


class CheckApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self.output = None
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "图片和标注匹配校验", 720, 300)

    def _create_frames(self):
        # 提示的 frame
        self.frame_tips = tk.Frame(self.root)
        self.frame_tips.pack()
        # 图片目录的 frame
        self.frame_image = tk.Frame(self.root, width=720, height=30)
        self.frame_image.pack(pady=(10, 0))
        self.frame_image.pack_propagate(False)
        # 标注路径的 frame
        self.frame_label = tk.Frame(self.root, width=720, height=30)
        self.frame_label.pack(pady=(10, 0))
        self.frame_label.pack_propagate(False)
        # 按钮的 frame
        self.frame_button = tk.Frame(self.root, width=720, height=30)
        self.frame_button.pack(pady=(10, 10))
        # 输出框的 frame
        self.frame_output = tk.Frame(self.root, width=720, height=30)
        self.frame_output.pack(pady=(10, 0))
        self.frame_label.pack_propagate(False)

    def _create_widgets(self):
        # 提示的组件
        label_tips = tk.Label(self.frame_tips, text="图片目录需保证只有纯净的图片")
        # 图片目录的组件
        label_image = tk.Label(self.frame_image, text="图片目录：", anchor='e', width=20)
        label_image.pack(side="left")
        entry_image = tk.Entry(self.frame_image, width=70)
        entry_image.pack(side="left")
        self.entries["image"] = entry_image
        # 标注路径的组件
        label_label = tk.Label(self.frame_label, text="标注路径：", anchor='e', width=20)
        label_label.pack(side="left")
        entry_label = tk.Entry(self.frame_label, width=70)
        entry_label.pack(side="left")
        self.entries["label"] = entry_label
        # 按钮
        button_det = tk.Button(self.frame_button, text="det标注对应性校验", width=20, height=8, command=self._check_det)
        button_det.place(relx=0.25, rely=0.5, anchor="center")
        button_rec = tk.Button(self.frame_button, text="rec标注对应性校验\n(待施工)", width=20, height=8, command=self._check_rec)
        button_rec.place(relx=0.75, rely=0.5, anchor="center")
        # 输出框
        text_output = tk.Text(self.frame_output, width=80, height=10)
        text_output.pack()
        self.output = text_output

    def _check_det(self):
        self.output.delete(1.0, tk.END)
        image = self.entries["image"].get()
        label = self.entries["label"].get()
        output = check_det_labels(image, label)
        self.output.insert(tk.END, output)

    def _check_rec(self):
        image = self.entries["image"].get()
        label = self.entries["label"].get()
