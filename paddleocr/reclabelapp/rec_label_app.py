import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkbuilder.panel_settings import setup_window


class MergeLabelApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.entries = {}
        self.output = None
        self._state_manager()
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self._bind_shotcuts()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "REC 标注软件", 1000, 600)

    def _create_frames(self):
        # 顶部菜单栏
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        # 主框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.88)
        # 左侧文件列表栏
        self.left_frame = tk.Frame(self.main_frame, bd=2, relief="groove")
        self.left_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        # 中间画布区域
        self.canvas_frame = tk.Frame(self.main_frame, bd=2, relief="groove")
        self.canvas_frame.place(relx=0.2, rely=0, relwidth=0.6, relheight=1)
        # 右侧标注和输出区域
        self.right_frame = tk.Frame(self.main_frame, bd=2, relief="groove")
        self.right_frame.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)

    def _create_widgets(self):
        # region 顶部菜单栏
        self.open_button = tk.Button(self.menu_frame, text="打开目录", font=20, width=10, height=2,
                                     command=self._open_dir)
        self.open_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.prev_button = tk.Button(self.menu_frame, text="下一张", font=20, width=10, height=2,
                                     command=self._next_image)
        self.prev_button.pack(side=tk.RIGHT, padx=10, pady=10)
        self.next_button = tk.Button(self.menu_frame, text="上一张", font=20, width=10, height=2,
                                     command=self._prev_image)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10)
        label1 = tk.Label(self.menu_frame, text="快捷键：\nctrl+滚轮：缩放图片",
                          font=("Arial", 10), height=2, anchor="w", justify="left")
        label1.pack(side=tk.LEFT, padx=(10, 0), pady=10)
        label2 = tk.Label(self.menu_frame, text="\n↑：上一张",
                          font=("Arial", 10), height=2, anchor="w", justify="left")
        label2.pack(side=tk.LEFT, padx=(10, 0), pady=10)
        label3 = tk.Label(self.menu_frame, text="\n↓ 或 回车：下一张",
                          font=("Arial", 10), height=2, anchor="w", justify="left")
        label3.pack(side=tk.LEFT, padx=(10, 0), pady=10)
        # endregion

        # region 左侧文件列表栏
        self.status_label = tk.Label(self.left_frame, text="当前图片: 0/0", font=20, width=20, height=1)
        self.status_label.pack()
        self.file_list_frame = tk.Frame(self.left_frame)
        self.file_list_frame.pack(fill=tk.BOTH, expand=True)
        v_scrollbar = tk.Scrollbar(self.file_list_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = tk.Scrollbar(self.file_list_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.file_listbox = tk.Listbox(
            self.file_list_frame,
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set,
            selectbackground="white",
            selectforeground="black",
            background="white",
            activestyle="none",
        )
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)
        v_scrollbar.config(command=self.file_listbox.yview)
        h_scrollbar.config(command=self.file_listbox.xview)
        # endregion

        # region 中间画布区域
        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # endregion

        # region 右侧标注和输出区域
        self.annotation_entry = tk.Entry(self.right_frame)
        self.annotation_entry.pack(fill=tk.X, padx=5, pady=5)
        self.output_text = tk.Text(self.right_frame, height=10, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # endregion

    def _bind_shotcuts(self):
        self.file_listbox.bind("<Left>", lambda e: "break")  # 禁止 Listbox 响应 ←
        self.file_listbox.bind("<Right>", lambda e: "break")  # 禁止 Listbox 响应 →
        self.root.bind("<Control-MouseWheel>", self._zoom_image)
        self.root.bind("<Up>", self._prev_image)
        self.root.bind("<Down>", self._next_image)
        self.root.bind("<Return>", self._next_image)

    def _state_manager(self):
        self.image_files = []
        self.current_image_index = -1
        self.current_image = None
        self.photo_image = None
        self.image_scale = 1.0
        self.label_dict = {}
        self.color_state = []

    def _open_dir(self):
        initial_path = os.getcwd()
        directory = filedialog.askdirectory(initialdir=initial_path)
        if not directory:
            return

        # 获取目录下的图片文件
        self.image_files = [entry.path for entry in os.scandir(directory)
                            if entry.is_file() and entry.name.lower().endswith((".jpg", ".png", ".jpeg"))]
        self.image_files.sort()
        self.current_image_index = 0 if self.image_files else -1

        # 读取标签文件
        rec_gt_path = os.path.join(directory, "rec_gt.txt")
        open(rec_gt_path, 'a').close()  # 如果文件不存在，则创建

        self.label_dict = {}  # 存储 {image_name: transcription}
        with open(rec_gt_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    image_name, transcription = line.split("\t")
                    self.label_dict[image_name] = transcription  # 存入字典
                except ValueError:
                    self.output_text.insert(tk.END, "标注文件格式有误\n")

        # 更新文件列表框
        self.file_listbox.delete(0, tk.END)
        for idx, file in enumerate(self.image_files):
            filename = os.path.basename(file)
            self.file_listbox.insert(tk.END, filename)
            if filename in self.label_dict:  # 该文件有标签
                self.color_state.append(('#D9E1F4', '#D9E1F4'))
            else:
                self.color_state.append(('white', 'white'))

        # 更新视图（状态栏 + 选中高亮 + 加载图片）
        self.update_view()

    def update_view(self, first_load=True):
        """更新状态栏和图像显示，并高亮当前选中项"""
        total = len(self.image_files)
        current = self.current_image_index + 1 if self.current_image_index >= 0 else 0
        self.status_label.config(text=f"当前图片: {current}/{total}")

        # 高亮当前图片对应的列表项，取消之前的高亮
        if self.current_image_index >= 0:
            for idx, color in enumerate(self.color_state):
                if color[1] == 'lightgray':
                    self.color_state[idx] = (color[0], color[0])
            color = self.color_state[self.current_image_index]
            self.color_state[self.current_image_index] = (color[1], 'lightgray')
            self.file_listbox.see(self.current_image_index)  # 自动滚动到可见范围
        # 更新列表项颜色
        for idx, color in enumerate(self.color_state):
            self.file_listbox.itemconfig(idx, {'bg': color[1]})

        if 0 <= self.current_image_index < total:
            # 加载并显示图片
            image_path = self.image_files[self.current_image_index]
            self.current_image = Image.open(image_path)
            self.display_image(first_load)

            # 加载并显示标签
            image_name = os.path.basename(image_path)
            if image_name in self.label_dict:
                transcription = self.label_dict[image_name]
                self.annotation_entry.delete(0, tk.END)
                self.annotation_entry.insert(0, transcription)
            else:
                self.annotation_entry.delete(0, tk.END)

    def display_image(self, first_load=True):
        if self.current_image is None:
            return

        img_w, img_h = self.current_image.size

        # 如果是首次加载，并且图片大于画布，则调整缩放比例
        if first_load:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if img_w > canvas_width or img_h > canvas_height:
                scale_w = canvas_width / img_w
                scale_h = canvas_height / img_h
                self.image_scale = min(scale_w, scale_h)  # 只在首次加载时修改 self.image_scale

        # 计算缩放后的尺寸（后续缩放由 self.image_scale 控制）
        new_w, new_h = int(img_w * self.image_scale), int(img_h * self.image_scale)
        resized_image = self.current_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(resized_image)

        # 计算居中坐标
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        x = (canvas_width - new_w) // 2
        y = (canvas_height - new_h) // 2

        # 清空画布并绘制图片
        self.canvas.delete("all")
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo_image)

    def _next_image(self, event=None):
        if self.current_image_index < len(self.image_files) - 1:
            self._confirm()     # 切换图片之前缓存
            self.current_image_index += 1
            self.update_view()

    def _prev_image(self, event=None):
        if self.current_image_index > 0:
            self._confirm()  # 切换图片之前缓存
            self.current_image_index -= 1
            self.update_view()

    def _confirm(self):
        image_name = os.path.basename(self.image_files[self.current_image_index])
        transcription = self.annotation_entry.get()
        if not (image_name and transcription):
            return
        self.label_dict[image_name] = transcription
        color = self.color_state[self.current_image_index]
        self.color_state[self.current_image_index] = (color[1], '#E3F2D9')
        self.output_text.config(state=tk.NORMAL)  # 允许插入
        self.output_text.insert(tk.END, f"图片 {image_name} 的标注已缓存\n")
        self.output_text.config(state=tk.DISABLED)  # 重新禁用编辑
        self.output_text.see(tk.END)  # 滚动到底部

    def _zoom_image(self, event):
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self.image_scale *= scale_factor
        self.display_image(first_load=False)

    def _save_annotation(self, event=None):
        if not self.label_dict:
            return

        try:
            output = []
            output_path = os.path.join(os.path.dirname(self.image_files[0]), "rec_gt.txt")
            for image_name, transcription in self.label_dict.items():
                output.append(f"{image_name}\t{transcription}")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(output))
            self.output_text.config(state=tk.NORMAL)  # 允许插入
            self.output_text.insert(tk.END, f"所有标注已保存到 rec_gt.txt\n")
            self.output_text.config(state=tk.DISABLED)  # 重新禁用编辑
            self.output_text.see(tk.END)  # 滚动到底部
        except:
            self.output_text.config(state=tk.NORMAL)  # 允许插入
            self.output_text.insert(tk.END, f"保存失败\n")
            self.output_text.config(state=tk.DISABLED)  # 重新禁用编辑
            self.output_text.see(tk.END)  # 滚动到底部

    def on_file_select(self, event):
        try:
            selection = event.widget.curselection()
            if selection:
                self.file_listbox.selection_clear(0, tk.END)    # 取消 Tkinter 默认选中状态
                self.current_image_index = selection[0]
                self.update_view()
        except:
            pass

    def _on_closing(self):
        """窗口关闭前执行保存操作"""
        try:
            self._confirm()     # 调用缓存函数
            self._save_annotation()  # 调用保存函数
        except:
            pass
        finally:
            self.root.destroy()  # 关闭窗口


if __name__ == '__main__':
    try:
        app = MergeLabelApp()
    except:
        pass
