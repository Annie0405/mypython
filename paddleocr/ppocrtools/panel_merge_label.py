import tkinter as tk
from paddleocr.ppocrtools.det_process import merge_label
from tkbuilder.panel_settings import setup_window


class MergeLabelApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "det标注文件合并", 720, 140)

    def _create_frames(self):
        # det标注文件路径的 frame
        self.frame_path = tk.Frame(self.root, width=600, height=30)
        self.frame_path.place(x=50, y=20)
        self.frame_path.pack_propagate(False)
        # 提示框的 frame
        self.frame_tips = tk.Frame(self.root, width=600, height=40)
        self.frame_tips.place(x=50, y=50)
        # 按钮的 frame
        self.frame_button = tk.Frame(self.root, width=600, height=30)
        self.frame_button.place(x=50, y=95)

    def _create_widgets(self):
        # labelme标注路径的组件
        label_path = tk.Label(self.frame_path, text="det标注文件路径：", anchor='e', width=20)
        label_path.pack(side="left")
        entry_path = tk.Entry(self.frame_path, width=70)
        entry_path.pack(side="left")
        self.entries["path"] = entry_path
        # 提示框
        label_tips = tk.Label(self.frame_tips,
                              text="*所有要合并的det标注文件放在路径下，文件名中必须包含“Label”")
        label_tips.place(relx=0.5, rely=0.5, anchor="center")
        # 底部按钮
        button_merge = tk.Button(self.frame_button, text="开始合并", width=10, command=self._merge)
        button_merge.place(relx=0.5, rely=0.5, anchor="center")

    def _merge(self):
        path = self.entries["path"].get()
        merge_label(path)
