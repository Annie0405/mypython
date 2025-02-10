import tkinter as tk
from tkbuilder.panel_settings import setup_window
from labelme.labelme2ppocr import labelme2det


class Labelme2DetApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "labelme格式转为ppocr的det格式", 720, 200)

    def _create_frames(self):
        # 输入文件夹的 frame
        self.frame_input = tk.Frame(self.root, width=600, height=30)
        self.frame_input.grid(row=0, column=0, pady=(10, 0))
        self.frame_input.pack_propagate(False)
        # 输出文件夹的 frame
        self.frame_output = tk.Frame(self.root, width=600, height=30)
        self.frame_output.grid(row=1, column=0)
        self.frame_output.pack_propagate(False)
        # 按钮的 frame
        self.frame_button = tk.Frame(self.root, width=600, height=30)
        self.frame_button.grid(row=2, column=0, pady=(0, 10))

    def _create_widgets(self):
        # 创建网格
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)  # 居中列
        # 输入文件夹的组件
        label_input = tk.Label(self.frame_input, text="输入文件夹的路径：", anchor='e', width=20)
        label_input.pack(side="left")
        entry_input = tk.Entry(self.frame_input, width=70)
        entry_input.pack(side="left")
        self.entries["input_path"] = entry_input
        # 输出文件夹的组件
        label_output = tk.Label(self.frame_output, text="输出文件夹的路径：", anchor='e', width=20)
        label_output.pack(side="left")
        entry_output = tk.Entry(self.frame_output, width=70)
        entry_output.pack(side="left")
        self.entries["output_path"] = entry_output
        # 按钮的组件
        button = tk.Button(self.frame_button, text="开始转换", command=self._convert)
        button.place(relx=0.5, rely=0.5, anchor="center")

    def _convert(self):
        input_path = self.entries["input_path"].get()
        output_path = self.entries["output_path"].get()
        if input_path and output_path:
            labelme2det(input_path, output_path)
        else:
            print("警告：文件夹路径不得为空！")
