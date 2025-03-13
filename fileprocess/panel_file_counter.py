import tkinter as tk
from fileprocess.file_counter import count_files


class FileCounterApp:
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
        self.root.title("统计文件数量")
        # 窗口大小和位置
        window_width = 700
        window_height = 190
        axis_x = int((screen_width - window_width) / 2)
        axis_y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    def _create_frames(self):
        # 目录的 frame
        self.dir_frame = tk.Frame(self.root, width=600, height=30)
        self.dir_frame.place(x=50, y=60)
        self.dir_frame.pack_propagate(False)
        # 按钮的 frame
        self.btn_frame = tk.Frame(self.root, width=600, height=30)
        self.btn_frame.place(x=50, y=100)
        self.btn_frame.pack_propagate(False)

    def _create_widgets(self):
        # 目录相关组件
        label_dir = tk.Label(self.dir_frame, text="目录路径：", anchor='e', width=15)
        label_dir.pack(side="left")
        entry_dir = tk.Entry(self.dir_frame, width=70)
        entry_dir.pack(side="left")
        self.entries["dir"] = entry_dir
        # 按钮相关组件
        button = tk.Button(self.btn_frame, text="统计文件数量", command=self._count)
        button.pack()

    def _count(self):
        dir_path = self.entries["dir"].get()
        count_files(dir_path)
