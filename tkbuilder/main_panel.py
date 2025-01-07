import tkinter as tk


class MainPanelApp:
    def __init__(self, title: str, width: int, height: int, buttons: dict, button_width: int):
        self.root = tk.Tk()
        self.title = title
        self.width = width
        self.height = height
        self.buttons = buttons
        self.button_width = button_width
        self._build()
        self.root.mainloop()

    def _build(self):
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # 添加窗口标题
        self.root.title(self.title)
        # 窗口大小和位置
        axis_x = int((screen_width - self.width) / 2)
        axis_y = int((screen_height - self.height) / 2)
        self.root.geometry(f"{self.width}x{self.height}+{axis_x}+{axis_y}")
        # 按钮创建
        button_num = len(self.buttons)
        # 创建网格
        for i in range(button_num+2):
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)  # 居中列
        # 创建按钮
        for i, (text, command) in enumerate(self.buttons.items()):
            button = tk.Button(self.root, text=text, command=lambda: command(), width=self.button_width)
            button.grid(row=i+1, column=0)
