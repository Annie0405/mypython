import tkinter as tk
from fileprocess.create_dir import create_dir


class DirCreateApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self.output = None
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # 添加窗口标题
        self.root.title("创建文件夹")
        # 窗口大小和位置
        window_width = 700
        window_height = 160
        axis_x = int((screen_width - window_width) / 2)
        axis_y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    def _create_frames(self):
        # 路径的 frame
        self.path_frame = tk.Frame(self.root, width=700, height=30)
        self.path_frame.place(x=0, y=20)
        self.path_frame.pack_propagate(False)
        # 其他参数的 frame
        self.args_frame = tk.Frame(self.root, width=700, height=30)
        self.args_frame.place(x=0, y=60)
        self.args_frame.pack_propagate(False)

    def _create_widgets(self):
        # 路径相关组件
        label_path = tk.Label(self.path_frame, text="路径：", anchor='e', width=10)
        label_path.pack(side="left")
        entry_path = tk.Entry(self.path_frame, width=85)
        entry_path.pack(side="left")
        self.entries["path"] = entry_path
        # 输入目标文件夹相关组件
        # 前缀输入
        frame_prefix = tk.Frame(self.args_frame)
        frame_prefix.pack(side="left", padx=(0, 10))
        label = tk.Label(frame_prefix, text="前缀：", anchor='e', width=10)
        label.pack(side="left")
        entry = tk.Entry(frame_prefix, width=15)
        entry.pack(side="left")
        self.entries["prefix"] = entry
        # 起始编号
        frame_number = tk.Frame(self.args_frame)
        frame_number.pack(side="left", padx=(0, 10))
        label = tk.Label(frame_number, text="起始编号：", anchor='e', width=15)
        label.pack(side="left")
        entry = tk.Entry(frame_number, width=15)
        entry.pack(side="left")
        self.entries["number"] = entry
        # 数量
        frame_count = tk.Frame(self.args_frame)
        frame_count.pack(side="left", padx=(0, 10))
        label = tk.Label(frame_count, text="数量：", anchor='e', width=10)
        label.pack(side="left")
        entry = tk.Entry(frame_count, width=15)
        entry.pack(side="left")
        self.entries["count"] = entry
        # 底部按钮
        button_ok = tk.Button(self.root, text="创建", width=10, command=self.start_create)
        button_ok.place(x=350, y=120, anchor="center")

    def start_create(self):
        path = self.entries["path"].get()
        prefix = self.entries["prefix"].get()
        number = self.entries["number"].get()
        count = self.entries["count"].get()
        create_dir(path, prefix, number, count)


if __name__ == '__main__':
    app = DirCreateApp()
