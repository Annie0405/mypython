import tkinter as tk
from fileprocess.rename_files import rename_files


class RenameFilesApp:
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
        self.root.title("文件重命名")
        # 窗口大小和位置
        window_width = 700
        window_height = 156
        axis_x = int((screen_width - window_width) / 2)
        axis_y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    def _create_frames(self):
        # 文件夹路径的 frame
        self.frame_path = tk.Frame(self.root, width=600, height=30)
        self.frame_path.place(x=50, y=20)
        self.frame_path.pack_propagate(False)
        # 其他配置的 frame
        self.frame_cfg = tk.Frame(self.root, width=600, height=30)
        self.frame_cfg.place(x=50, y=60)
        # 前缀的 frame
        self.frame_prefix = tk.Frame(self.frame_cfg, width=300, height=30)
        self.frame_prefix.place(relx=0.35, rely=0.5, anchor="center")
        self.frame_prefix.pack_propagate(False)
        # 后缀位数的 frame
        self.frame_suffix = tk.Frame(self.frame_cfg, width=150, height=30)
        self.frame_suffix.place(relx=0.575, rely=0.5, anchor="center")
        self.frame_suffix.pack_propagate(False)
        # 文件数量的 frame
        self.frame_num = tk.Frame(self.frame_cfg, width=150, height=30)
        self.frame_num.place(relx=0.8, rely=0.5, anchor="center")
        self.frame_num.pack_propagate(False)

    def _create_widgets(self):
        # 文件夹路径的相关组件
        label_path = tk.Label(self.frame_path, text="文件夹路径：", anchor='e', width=15)
        label_path.pack(side="left")
        entry_path = tk.Entry(self.frame_path, width=70)
        entry_path.pack(side="left")
        self.entries["path"] = entry_path
        # 其他配置的相关组件
        # 前缀的组件
        label_prefix = tk.Label(self.frame_prefix, text="前缀：", anchor='e', width=5)
        label_prefix.pack(side="left")
        entry_prefix = tk.Entry(self.frame_prefix, width=20)
        entry_prefix.pack(side="left")
        self.entries["prefix"] = entry_prefix
        # 后缀位数的组件
        label_suffix = tk.Label(self.frame_suffix, text="后缀位数：", anchor='e', width=10)
        label_suffix.pack(side="left")
        entry_suffix = tk.Entry(self.frame_suffix, width=5)
        entry_suffix.pack(side="left")
        self.entries["suffix"] = entry_suffix
        # 文件数量的组件
        label_num = tk.Label(self.frame_num, text="文件数量：", anchor='e', width=10)
        label_num.pack(side="left")
        entry_num = tk.Entry(self.frame_num, width=10)
        entry_num.pack(side="left")
        self.entries["num"] = entry_num
        # 底部按钮
        button_ok = tk.Button(self.root, text="确定", width=10, command=self.start_rename)
        button_ok.place(relx=0.5, y=120, anchor="center")

    def start_rename(self):
        dir_path = self.entries["path"].get()
        prefix = self.entries["prefix"].get()
        suffix_digits = self.entries["suffix"].get()
        file_num = self.entries["num"].get()
        rename_files(dir_path, prefix, suffix_digits, file_num)
