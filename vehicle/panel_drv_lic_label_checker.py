import os
import json
import cv2
import re
import numpy as np
import tkinter as tk
from tkbuilder.panel_settings import setup_window

PLATE_NO = "PlateNo"
OTHER_18 = ["VehicleType", "Owner", "Address", "UseCharacter", "Model", "VIN", "EngineNo", "RegisterDate", "IssueDate",
            "FileNo", "APC", "GVW", "CVW", "GVWR", "LWH", "TM", "fuel", "ChipNo"]
TIMESTAMP = "timestamp"
PATTERN1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
            'W', 'X', 'Y', 'Z',
            '藏', '川', '鄂', '甘', '赣', '贵', '桂', '黑', '沪', '吉', '冀', '津', '晋', '京', '辽', '鲁', '蒙',
            '闽', '宁', '青', '琼', '陕', '苏', '皖', '湘', '新', '渝', '豫', '粤', '云', '浙',
            '港', '澳', '台', '警', '挂', '学']
PATTERN2 = r'^[\u4e00-\u9fff]+$'
PATTERN3 = r'[IOQ]'
PATTERN4 = r'[IO]'
PATTERN5 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ' ']
PATTERN6 = r'^[0-9X]+$'
PATTERN7 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '人']
PATTERN8 = r'\d+'
PATTERN9 = ['柴油', '汽油/电', '汽油', '天然气', '新能源/电', '混合动力', '汽油/天然气', '无']


class DrvLicLabelCheckerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self.outputs = {}
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        setup_window(self.root, "行驶证标注验证器", 720, 500)

    def _create_frames(self):
        # 输入文件路径的 Frame
        self.frame_path = tk.Frame(self.root, width=720, height=40)
        self.frame_path.pack(pady=(20, 0))
        # 功能按钮的 Frame
        self.frame_button = tk.Frame(self.root, width=720, height=50)
        self.frame_button.pack(pady=(10, 0))
        # 输出框的 Frame
        self.frame_output = tk.Frame(self.root, width=720, height=350)
        self.frame_output.pack()

    def _create_widgets(self):
        # region 输入文件路径的组件
        label = tk.Label(self.frame_path, text="路径: ")
        label.place(x=20, y=0)
        entry = tk.Entry(self.frame_path, width=90)
        entry.place(x=60, y=0)
        self.entries["path"] = entry
        label = tk.Label(self.frame_path, text="* 请输入 Label.txt 所在文件夹的路径，路径中不得有中文")
        label.place(x=60, y=20)
        # endregion
        # region 功能按钮的组件
        button = tk.Button(self.frame_button, text="关键词校验", width=10, command=lambda: self._check("key"))
        button.place(x=60, y=0)
        button = tk.Button(self.frame_button, text="转录校验", width=10, command=lambda: self._check("transcription"))
        button.place(x=160, y=0)
        button = tk.Button(self.frame_button, text="边框校验", width=10, command=lambda: self._check("bbox"))
        button.place(x=260, y=0)
        # endregion
        # region 输出框的组件
        text = tk.Text(self.frame_output, width=90, height=30)
        text.place(x=60, y=0)
        text.config(state=tk.DISABLED)
        self.outputs["output"] = text
        # endregion

    def _check(self, mode):
        mode_dict = {"key": "关键词", "transcription": "转录", "bbox": "边框"}
        flag = 1  # 校验标志
        checked_list = []  # 存储校验完毕的标签
        self.outputs["output"].config(state=tk.NORMAL)
        self.outputs["output"].delete(1.0, tk.END)

        path = self.entries["path"].get()
        if path:
            label_path = os.path.join(path, "Label.txt")
            output_dir = os.path.join(path, "check_bbox")
            os.makedirs(output_dir, exist_ok=True)

            with open(label_path, "r", encoding="utf-8") as f:
                label_list = [line.strip() for line in f.readlines()]
            for line in label_list:
                try:
                    image = line.split("\t")[0]
                    label = json.loads(line.split("\t")[1])
                    args: dict = {"path": path, "line": line, "image": image, "label": label, "flag": flag,
                                  "output_dir": output_dir}
                    if mode == "key":
                        self._check_key(args)
                    elif mode == "transcription":
                        ori_LWH, format_LWH = self._check_transcription(args)
                        # 格式化外廓尺寸
                        args["line"] = args["line"].replace(ori_LWH, format_LWH)
                        args["label"] = json.loads(args["line"].split("\t")[1])
                    elif mode == "bbox":
                        self._check_points(args)
                    flag = args["flag"]
                    checked_list.append(args["image"] + "\t" + json.dumps(args["label"], ensure_ascii=False))
                except Exception as e:
                    flag = 0
                    print(e)
                    print("错误项：", line)
            if flag:
                if mode == "key":
                    self.outputs["output"].insert(tk.END, f"关键词校验无误\n")
                elif mode == "transcription":
                    self.outputs["output"].insert(tk.END, f"转录校验完毕\n")
                elif mode == "bbox":
                    self.outputs["output"].insert(tk.END, f"边框绘制完毕，请至 {output_dir} 文件夹进行人工校验\n")
            # 把校验完毕的关键词写回到文件
            if not checked_list:
                checked_list = label_list
            with open(label_path, "w", encoding="utf-8") as f:
                f.write("\n".join(checked_list))
                f.write("\n")
        else:
            self.outputs["output"].insert(tk.END, "请输入 Label.txt 所在文件夹的路径\n")

        self.outputs["output"].config(state=tk.DISABLED)

    def _check_key(self, args):
        # region 关键词内容校验
        checked_label = []
        for item in args["label"]:
            key = item["key_cls"]
            if key in OTHER_18 or key == PLATE_NO:
                checked_label.append(item)
            elif key != TIMESTAMP:
                args["flag"] = 0
                self.outputs["output"].insert(tk.END, f"错误！{args["image"]}：存在不规范关键词：{key}\n")
                checked_label.append(item)
        args["label"] = checked_label
        # endregion
        # region 关键词数量校验
        if args["line"].count(PLATE_NO) > 2 or args["line"].count("GVW") > 2:
            args["flag"] = 0
            self.outputs["output"].insert(tk.END, f"错误！{args["image"]}：PlateNo或GVW出现次数不对\n")
        for KEY in OTHER_18:
            if args["line"].count(KEY) > 1 and KEY != "GVW":
                args["flag"] = 0
                self.outputs["output"].insert(tk.END, f"错误！{args["image"]}：{KEY}出现次数为 {args["line"].count(KEY)}\n")
        # endregion

    def _check_transcription(self, args):
        ori_LWH = ""
        format_LWH = ""
        for label in args["label"]:
            key = label["key_cls"]
            transcription = label["transcription"]

            # region 转录内容校验
            # 住址、品牌型号校验难度较大，故不做校验
            if key == "PlateNo":
                if transcription[0] not in PATTERN1[34:65]:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：车牌号中省份简称非法\n")
                else:
                    for c in transcription:
                        if c not in PATTERN1:
                            self.outputs["output"].insert(tk.END, f"错误！{args['image']}：车牌号中存在非法字符：{c}\n")
            elif key == "VehicleType" or key == "Owner" or key == "UseCharacter":   # 全为中文即可
                if re.match(PATTERN2, transcription) is None:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：{key} 有误：存在非中文字符\n")
            elif key == "VIN":  # 长度小于等于17，不含中文和I、O、Q，全为大写字母或数字
                if len(transcription) > 17:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：VIN长度超过17位\n")
                elif re.search(PATTERN2, transcription) is not None:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：VIN中存在中文字符\n")
                elif re.search(PATTERN3, transcription) is not None:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：VIN中存在I/O/Q\n")
                else:
                    for c in transcription:
                        if (not c.isdigit()) and (not (c.isupper() and c.isalpha())):
                            self.outputs["output"].insert(tk.END, f"错误！{args['image']}：VIN中存在非法字符：{c}\n")
            elif key == "EngineNo":     # 不含中文和I、O即可
                if re.search(PATTERN2, transcription) is not None:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：发动机号中存在中文字符\n")
                elif re.search(PATTERN4, transcription) is not None:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：发动机号中存在I/O\n")
            elif key == "RegisterDate" or key == "IssueDate":   # 只包含数字和连字符
                for c in transcription:
                    if c not in PATTERN5:
                        self.outputs["output"].insert(tk.END, f"错误！{args['image']}：{key} 有误：存在非法字符\n")
            elif key == "FileNo":   # 只包含数字
                if not transcription.isdigit():
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：档案编号有误：存在非法字符\n")
            elif key == "APC":      # 只包含数字、+、人
                for c in transcription:
                    if c not in PATTERN7:
                        self.outputs["output"].insert(tk.END, f"错误！{args['image']}：核定载人数有误：存在非法字符\n")
            elif key == "GVW" or key == "CVW" or key == "GVWR" or key == "TM":  # kg结尾，其他是数字
                if not transcription.endswith('kg'):
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：{key} 有误：结尾不是kg\n")
                else:
                    tmp_str = transcription[:-2]
                    if not tmp_str.isdigit():
                        self.outputs["output"].insert(tk.END, f"错误！{args['image']}：{key} 有误：存在非法字符\n")
            elif key == "LWH":  # mm结尾，3个数之间有分隔符，把分隔符替换为小写x
                item = re.findall(PATTERN8, transcription)
                if len(item) != 3:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：外廓尺寸有误\n")
                else:
                    ori_LWH = transcription
                    format_LWH = 'x'.join(item) + 'mm'
            elif key == "fuel":     # 必须在燃料类型列表里
                if transcription not in PATTERN9:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：燃料类型有误，或未在燃料列表中\n")
            elif key == "ChipNo":    # 13位， 只包含数字和X
                if len(transcription) != 13:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：证芯编号有误：长度不为13\n")
                elif re.search(PATTERN6, transcription) is None:
                    self.outputs["output"].insert(tk.END, f"错误！{args['image']}：证芯编号有误：存在非法字符\n")
            # endregion
        return ori_LWH, format_LWH

    def _check_points(self, args):
        image = os.path.basename(args["image"])
        image_path = os.path.join(args["path"], image)
        output_path = os.path.join(args["output_dir"], image)

        image = cv2.imread(image_path)

        for label in args["label"]:
            points = np.array(label["points"], np.int32)
            points = points.reshape((-1, 1, 2))
            cv2.polylines(image, [points], True, (0, 255, 0), 2)

            cv2.imwrite(output_path, image)
