import tkinter as tk
from labelme2COCO import polygon_verify, Labelme2COCO
from tkbuilder.panel_settings import setup_window


class Labelme2COCOApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "labelme格式标注转换为COCO格式", 720, 200)

    def _create_frames(self):
        # labelme标注路径的 frame
        self.frame_labelme = tk.Frame(self.root, width=600, height=30)
        self.frame_labelme.place(x=50, y=20)
        self.frame_labelme.pack_propagate(False)
        # COCO标注存放路径的 frame
        self.frame_COCO = tk.Frame(self.root, width=600, height=30)
        self.frame_COCO.place(x=50, y=60)
        self.frame_COCO.pack_propagate(False)
        # 提示框的 frame
        self.frame_tips = tk.Frame(self.root, width=600, height=40)
        self.frame_tips.place(x=50, y=100)
        # 按钮的 frame
        self.frame_button = tk.Frame(self.root, width=600, height=30)
        self.frame_button.place(x=50, y=150)

    def _create_widgets(self):
        # labelme标注路径的组件
        label_labelme = tk.Label(self.frame_labelme, text="labelme标注路径：", anchor='e', width=20)
        label_labelme.pack(side="left")
        entry_labelme = tk.Entry(self.frame_labelme, width=70)
        entry_labelme.pack(side="left")
        self.entries["labelme"] = entry_labelme
        # COCO标注存放路径相关组件
        label_COCO = tk.Label(self.frame_COCO, text="COCO标注存放路径：", anchor='e', width=20)
        label_COCO.pack(side="left")
        entry_COCO = tk.Entry(self.frame_COCO, width=70)
        entry_COCO.pack(side="left")
        self.entries["COCO"] = entry_COCO
        # 提示框
        label_tips = tk.Label(self.frame_tips,
                              text="*先构建好categories，保存在COCO路径下的categories_file.json文件中\n"
                                   + "categories需包含属性id, name, supercategory, iscrowd")
        label_tips.place(relx=0.5, rely=0.5, anchor="center")
        # 底部按钮
        button_verify = tk.Button(self.frame_button, text="校验", width=10, command=self._verify)
        button_verify.place(relx=0.4, rely=0.5, anchor="center")
        button_convert = tk.Button(self.frame_button, text="转换", width=10, command=self._convert)
        button_convert.place(relx=0.6, rely=0.5, anchor="center")

    def _verify(self):
        labelme_path = self.entries["labelme"].get()
        polygon_verify(labelme_path)

    def _convert(self):
        labelme_path = self.entries["labelme"].get()
        COCO_path = self.entries["COCO"].get()
        Labelme2COCO(labelme_path, COCO_path)
