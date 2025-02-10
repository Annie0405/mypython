import tkinter as tk
from fileprocess.copy_files import copy_files


class CopyFilesApp:
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
        self.root.title("文件复制")
        # 窗口大小和位置
        window_width = 700
        window_height = 190
        axis_x = int((screen_width - window_width) / 2)
        axis_y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    def _create_frames(self):
        # 源文件夹的 frame
        self.src_frame = tk.Frame(self.root, width=600, height=30)
        self.src_frame.place(x=50, y=60)
        self.src_frame.pack_propagate(False)
        # 目标文件夹的 frame
        self.dst_frame = tk.Frame(self.root, width=600, height=30)
        self.dst_frame.place(x=50, y=100)
        self.dst_frame.pack_propagate(False)

    def _create_widgets(self):
        # 顶部提示
        label_tips = tk.Label(self.root, text="复制源文件夹下所有文件到目标文件夹，源文件夹下不得有子文件夹")
        label_tips.place(relx=0.5, y=35, anchor="center")
        # 输入源文件夹相关组件
        label_src_dir = tk.Label(self.src_frame, text="源文件夹：", anchor='e', width=15)
        label_src_dir.pack(side="left")
        entry_src_dir = tk.Entry(self.src_frame, width=70)
        entry_src_dir.pack(side="left")
        self.entries["src_dir"] = entry_src_dir
        # 输入目标文件夹相关组件
        label_dst_dir = tk.Label(self.dst_frame, text="目标文件夹：", anchor='e', width=15)
        label_dst_dir.pack(side="left")
        entry_dst_dir = tk.Entry(self.dst_frame, width=70)
        entry_dst_dir.pack(side="left")
        self.entries["dst_dir"] = entry_dst_dir
        # 底部按钮
        button_ok = tk.Button(self.root, text="确定", width=10, command=self.start_copy)
        button_ok.place(x=350, y=160, anchor="center")

    def start_copy(self):
        src_path = self.entries["src_dir"].get()
        dst_path = self.entries["dst_dir"].get()
        copy_files(src_path, dst_path)
