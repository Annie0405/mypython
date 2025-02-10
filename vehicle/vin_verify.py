import tkinter as tk
from tkinter import messagebox


class VINVerifyApp:
    def __init__(self):
        # VIN码允许的字符列表
        self.chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                      'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
                      'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W',
                      'X', 'Y', 'Z']
        # 初始化字典和DataFrame
        self.lists = {
            "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
            "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9, "S": 2,
            "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
            "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        }
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("VIN 验证器")
        x, y = self.get_screen_size()
        self.root.geometry(f'250x130+{int(x / 2 - 125)}+{int(y / 2) - 65}')
        # 创建并放置标签和输入框
        label = tk.Label(self.root, text="请输入 VIN 号码:")
        label.pack(pady=10)
        self.entry = tk.Entry(self.root, width=20)
        self.entry.pack(pady=5)
        # 创建并放置按钮
        button = tk.Button(self.root, text="验证", command=self.check_vin)
        button.pack(pady=10)
        # 运行主循环
        self.root.mainloop()

    def get_screen_size(self):
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        return screen_width, screen_height

    def check_vin(self):
        text = self.entry.get()
        self.NUM(text)

    def NUM(self, text):
        num = [''] * 17
        if len(text) == 17:  # 判断它是否为17位数

            if text[9] in ['U', 'Z', '0']:
                messagebox.showinfo("异常", "VIN不符合规则：第十位非法")
                return

            for i in range(0, 17):
                if text[i] in self.chars:
                    if i == 8:
                        num[i] = text[i:i + 1]
                    else:
                        num[i] = self.lists.get(text[i:i + 1])
                else:
                    messagebox.showinfo("异常", "VIN不符合规则：存在不被允许的字符")

            check1 = num[0] * 8 + num[1] * 7 + num[2] * 6 + num[3] * 5 + num[4] * 4 + num[5] * 3 + num[6] * 2 + num[
                7] * 10  # 前8位的和
            check2 = num[9] * 9 + num[10] * 8 + num[11] * 7 + num[12] * 6 + num[13] * 5 + num[14] * 4 + num[15] * 3 + \
                     num[16] * 2  # 后8位的和
            check = (check1 + check2) % 11

            if (num[8].isdigit() and check == int(num[8])) or (num[8] == 'X' and check == 10):
                messagebox.showinfo("校验结果", "VIN 正确：" + text)
            elif (num[8].isdigit() and check != int(num[8])) or (num[8] == 'X' and check != 10):
                messagebox.showinfo("校验结果", "VIN 不符合规则：" + text)
            else:
                messagebox.showinfo("异常", "VIN不符合规则：校验位非法")

        else:
            messagebox.showinfo("异常", f"VIN不符合规则：VIN 位数不对：{len(text)}")
