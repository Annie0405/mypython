import tkinter as tk
from merge_dirs import gen_dir_list, merge_dirs


class DirMergeApp:
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
        self.root.title("文件夹合并")
        # 窗口大小和位置
        window_width = 700
        window_height = 150
        axis_x = int((screen_width - window_width) / 2)
        axis_y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    def _create_frames(self):
        # 源文件夹的 frame
        self.src_frame = tk.Frame(self.root, width=600, height=30)
        self.src_frame.place(x=50, y=20)
        self.src_frame.pack_propagate(False)
        # 目标文件夹的 frame
        self.dst_frame = tk.Frame(self.root, width=600, height=30)
        self.dst_frame.place(x=50, y=60)
        self.dst_frame.pack_propagate(False)

    def _create_widgets(self):
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
        button_ok = tk.Button(self.root, text="确定", width=10, command=self._ensure)
        button_ok.place(x=350, y=120, anchor="center")

    def _ensure(self):
        self.sub_win = tk.Tk()
        # 获取屏幕尺寸
        screen_width = self.sub_win.winfo_screenwidth()
        screen_height = self.sub_win.winfo_screenheight()
        # 添加窗口标题
        self.sub_win.title("文件夹合并")
        # 窗口大小和位置
        window_width = 250
        window_height = 300
        axis_x = int((screen_width - window_width) / 2)
        axis_y = int((screen_height - window_height) / 2)
        self.sub_win.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")
        # 提示
        label_tips = tk.Label(self.sub_win, text="合并以下文件夹：")
        label_tips.pack(pady=(20, 10))
        # 滑动显示文件夹列表
        frame_scroll = tk.Frame(self.sub_win)
        frame_scroll.pack()
        # 文件列表框
        listbox = tk.Listbox(frame_scroll, height=10)
        dir_list = self.get_dir_list()
        for dir in dir_list:
            listbox.insert(tk.END, dir)
        listbox.pack(side="left")
        # 滑动条
        scrollbar = tk.Scrollbar(frame_scroll)
        scrollbar["command"] = listbox.yview
        scrollbar.pack(side="right", fill="y")
        # 把滑动条绑定到文件列表框
        listbox.config(yscrollcommand=scrollbar.set)
        # 开始合并按钮
        button_merge = tk.Button(self.sub_win, text="开始合并", width=12, command=self.merge_start)
        button_merge.pack(pady=(20, 0))

    def get_dir_list(self):
        src_dir = self.entries["src_dir"].get()
        return gen_dir_list(src_dir)

    def merge_start(self):
        src_dir = self.entries["src_dir"].get()
        dst_dir = self.entries["dst_dir"].get()
        merge_dirs(src_dir, dst_dir)
        self.sub_win.destroy()
