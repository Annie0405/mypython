import tkinter as tk
from imageprocess.image_process import batch_rotate
from tkbuilder.panel_settings import setup_window


class RotateApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self.output = None
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "批量旋转图片", 720, 200)

    def _create_frames(self):
        # 图片目录的 frame
        self.frame_image = tk.Frame(self.root, width=720, height=30)
        self.frame_image.pack(pady=(10, 0))
        self.frame_image.pack_propagate(False)
        # 旋转角度的 frame
        self.frame_angle = tk.Frame(self.root, width=720, height=30)
        self.frame_angle.pack(pady=(10, 0))
        self.frame_angle.pack_propagate(False)
        # 按钮的 frame
        self.frame_button = tk.Frame(self.root, width=720, height=30)
        self.frame_button.pack(pady=(10, 10))
        self.frame_button.pack_propagate(False)
        # 输出框的 frame
        self.frame_output = tk.Frame(self.root, width=720, height=30)
        self.frame_output.pack(pady=(10, 0))
        self.frame_output.pack_propagate(False)

    def _create_widgets(self):
        # 图片目录的组件
        label_image = tk.Label(self.frame_image, text="图片目录：", anchor='e', width=20)
        label_image.pack(side="left")
        entry_image = tk.Entry(self.frame_image, width=70)
        entry_image.pack(side="left")
        self.entries["image"] = entry_image
        # 标注路径的组件
        label_angle = tk.Label(self.frame_angle, text="逆时针旋转：", anchor='e', width=20)
        label_angle.pack(side="left")
        entry_angle = tk.Entry(self.frame_angle, width=10)
        entry_angle.pack(side="left")
        self.entries["angle"] = entry_angle
        # 按钮
        button_det = tk.Button(self.frame_button, text="旋转", width=10, height=8, command=self._rotate)
        button_det.pack()
        # 输出框
        text_output = tk.Text(self.frame_output, width=80, height=20)
        text_output.pack()
        self.output = text_output

    def _rotate(self):
        self.output.delete(1.0, tk.END)
        image = self.entries["image"].get()
        angle = self.entries["angle"].get()
        output = batch_rotate(image, angle)
        self.output.insert(tk.END, output)
