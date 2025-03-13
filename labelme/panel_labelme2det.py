import time
import tkinter as tk
from tkinter import ttk
from tkbuilder import CommonPanelApp, setup_window
from labelme import get_label_list
from labelme.labelme2ppocr import labelme2det


class Labelme2DetApp(CommonPanelApp):
    def __init__(self):
        self.selected_labels = []
        self.save_vars = {}
        super().__init__(
            title="labelme格式转为ppocr的det格式",
            width=720,
            height=280,
        )

    def _create_frames(self):
        # 提示的 frame
        self.frame_tips = tk.Frame(self.frameA)
        self.frame_tips.pack(pady=10)
        # 输入文件夹的 frame
        self.frame_input = tk.Frame(self.frameA)
        self.frame_input.pack(pady=(0, 10))
        # 输出文件夹的 frame
        self.frame_output = tk.Frame(self.frameA)
        self.frame_output.pack(pady=(0, 10))
        # 选择标签的 frame
        self.frame_select = tk.Frame(self.frameA)
        self.frame_select.pack(pady=(0, 10))
        # 选择是否裁切 & 开始转换 的 frame
        self.frame_button = tk.Frame(self.frameA)
        self.frame_button.pack()

    def _create_widgets(self):
        # 提示的组件
        label_tips = tk.Label(self.frame_tips, text="如需裁切，路径中不得出现中文")
        label_tips.pack()
        # 输入文件夹的组件
        label_input = tk.Label(self.frame_input, text="输入文件夹的路径：", anchor='e', width=15)
        label_input.pack(side="left")
        entry_input = tk.Entry(self.frame_input, width=70)
        entry_input.pack(side="left")
        self.entries["input_path"] = entry_input
        # 输出文件夹的组件
        label_output = tk.Label(self.frame_output, text="输出文件夹的路径：", anchor='e', width=15)
        label_output.pack(side="left")
        entry_output = tk.Entry(self.frame_output, width=70)
        entry_output.pack(side="left")
        self.entries["output_path"] = entry_output
        # 选择标签的组件
        button = tk.Button(self.frame_select, text="选择标签", width=10, command=self._select_label)
        button.pack(side=tk.LEFT, padx=10)
        text = tk.Text(self.frame_select, width=40, height=1, font=("Arial", 16))
        text.pack(expand=True)
        self.outputs["labels"] = text
        # 选择是否裁切 & 开始转换的组件
        label = tk.Label(self.frame_button, text="是否裁切：", anchor='e', width=10)
        label.pack(side=tk.LEFT)
        is_crop = tk.StringVar()
        combo = ttk.Combobox(self.frame_button, textvariable=is_crop, width=10)
        combo['values'] = ('裁切', '不裁切')
        combo.current(0)    # 默认选中第一个
        combo.pack(side=tk.LEFT)
        self.entries["is_crop"] = combo
        button = tk.Button(self.frame_button, text="开始转换", width=10, command=self._convert)
        button.pack(expand=True, padx=(50, 100))

    def _select_label(self):
        input_path = self.entries["input_path"].get()
        if not input_path:
            return
        label_list = get_label_list(input_path)

        self.new_win = tk.Toplevel(self.root)
        setup_window(self.new_win, "选择标签", 300, 400)

        # 全选按钮
        self.select_all_var = tk.BooleanVar(master=self.root)
        button_select_all = tk.Checkbutton(self.new_win, text="全选", variable=self.select_all_var, command=self._toggle_all)
        button_select_all.pack(anchor="w", padx=10, pady=5)

        # 创建多选框
        self.check_buttons = []
        for label in label_list:
            var = tk.BooleanVar(master=self.root)
            btn_chk = tk.Checkbutton(self.new_win, text=label, variable=var)
            btn_chk.pack(anchor="w", padx=20)
            self.save_vars[label] = var
            self.check_buttons.append(btn_chk)

        # 确认按钮
        button_confirm = tk.Button(self.new_win, text="确认", command=self._confirm_selection)
        button_confirm.pack(side=tk.BOTTOM, pady=10)

    def _toggle_all(self):
        """全选/取消全选"""
        select_all = self.select_all_var.get()
        for var in self.save_vars.values():
            var.set(select_all)

    def _confirm_selection(self):
        """获取选中的标签"""
        self.selected_labels = [label for label, var in self.save_vars.items() if var.get()]
        string = ', '.join(self.selected_labels)
        self.outputs["labels"].delete(1.0, tk.END)
        self.outputs["labels"].insert(tk.END, string)
        self.new_win.destroy()

    def _convert(self):
        input_path = self.entries["input_path"].get()
        output_path = self.entries["output_path"].get()
        is_crop = self.entries["is_crop"].get()
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if input_path and output_path:
            info = labelme2det(input_path, output_path, self.selected_labels, is_crop)
            self.outputs["output"].insert(tk.END, f"[{current_time}] {info}")
        else:
            self.outputs["output"].insert(tk.END, f"[{current_time}] 警告：文件夹路径不得为空！\n")


if __name__ == '__main__':
    app = Labelme2DetApp()
