import tkinter as tk
from abc import ABC, abstractmethod
from tkbuilder.panel_settings import setup_window


class CommonPanelApp(ABC):
    """所有面板的基类，封装通用逻辑"""
    def __init__(self, title, width=720, height=200, enable_output=True):
        self.root = tk.Tk()
        self.entries = {}
        self.outputs = {}
        self.title = title  # 标题
        self.enable_output = enable_output

        self._setup_window(width, height)
        self._setup_common_layout()
        self._create_frames()   # 必须由子类实现
        self._create_widgets()  # 必须由子类实现

        self.root.mainloop()

    def _setup_window(self, width, height):
        """设置窗口属性"""
        setup_window(self.root, self.title, width, height)

    def _setup_common_layout(self):
        """创建 frameA（主面板）和可选的 frameB（用于输出信息）"""
        self.frameA = tk.Frame(self.root)  # 主内容框架
        self.frameA.pack(fill=tk.BOTH, expand=True)

        if self.enable_output:
            self.frameB = tk.Frame(self.root)  # 输出信息框架
            self.frameB.pack(fill=tk.X, side=tk.BOTTOM)
            self.text_output = tk.Text(self.frameB, height=5)
            self.text_output.pack(fill=tk.BOTH, expand=True, padx=50, pady=(10, 20))
            self.outputs["output"] = self.text_output

    @abstractmethod
    def _create_frames(self):
        """创建布局框架"""
        pass

    @abstractmethod
    def _create_widgets(self):
        """创建输入框、按钮等组件"""
        pass
