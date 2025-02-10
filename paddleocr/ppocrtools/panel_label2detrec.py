import tkinter as tk
from tkinter import ttk
from paddleocr.ppocrtools.det_process import label2det
from paddleocr.ppocrtools.rec_process import label2rec
from tkbuilder.panel_settings import setup_window


class Label2DetRecApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "Label文件中导出det或rec标注", 720, 190)

    def _create_frames(self):
        # 标注项目的根目录的 frame
        self.frame_path = tk.Frame(self.root, width=600, height=30)
        self.frame_path.place(x=50, y=30)
        self.frame_path.pack_propagate(False)
        # 提示框的 frame
        self.frame_tips = tk.Frame(self.root, width=600, height=30)
        self.frame_tips.place(x=50, y=60)
        # 下拉框的 frame
        self.frame_combo = tk.Frame(self.root, width=600, height=30)
        self.frame_combo.place(x=50, y=90)
        # 按钮的 frame
        self.frame_button = tk.Frame(self.root, width=600, height=30)
        self.frame_button.place(x=50, y=130)

    def _create_widgets(self):
        # 标注项目的根目录的组件
        label_path = tk.Label(self.frame_path, text="标注项目的根目录：", anchor='e', width=20)
        label_path.pack(side="left")
        entry_path = tk.Entry(self.frame_path, width=70)
        entry_path.pack(side="left")
        self.entries["path"] = entry_path
        # 提示框
        label_tips = tk.Label(self.frame_tips, text="*路径中不得包含中文字符")
        label_tips.place(relx=0.5, rely=0.5, anchor="center")
        # 下拉框
        options = ["", "det", "rec"]
        combo = ttk.Combobox(self.frame_combo, values=options, width=10)
        combo.set("")
        combo.place(relx=0.5, rely=0.5, anchor="center")
        self.entries["mode"] = combo
        # 底部按钮
        button_export = tk.Button(self.frame_button, text="开始导出", width=10, command=self._export)
        button_export.place(relx=0.5, rely=0.5, anchor="center")

    def _export(self):
        path = self.entries["path"].get()
        mode = self.entries["mode"].get()
        if mode == "":
            print("请选择导出的标注类型！")
        elif mode == "det":
            label2det(path)
        else:
            label2rec(path)
