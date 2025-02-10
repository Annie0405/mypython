import json
import os
import time


def label2det(path):
    new_label = []

    label_path = os.path.join(path, "Label.txt")
    with open(label_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            part0 = line.split('\t')[0]
            part0 = os.path.basename(part0)
            part1 = line.split('\t')[1]
            part1 = json.loads(part1)
            part1 = [{"points": part1[0]["points"]}]
            new_line = part0 + "\t" + json.dumps(part1)
            new_label.append(new_line)

    with open(os.path.join(path, "Label_gen.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(new_label))
        f.write("\n")

    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{current_time}] det标注导出完成！")


def merge_label(path):
    # 在路径下查找所有包含"Label"的txt文件
    label_file_list = []
    for file in os.listdir(path):
        if "Label" in file and file.endswith(".txt"):
            label_file_list.append(file)
    if label_file_list:
        merge_content = ""
        for file in label_file_list:
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                content = f.read()
            if not content.endswith("\n"):
                content += "\n"
            merge_content += content
        with open(os.path.join(path, "Label.txt"), "w", encoding="utf-8") as f:
            f.write(merge_content)
        print(f"已将所有标签文件合并至 {path}/Label.txt")
        # 删掉原来的文件
        for file in label_file_list:
            if file != "Label.txt":
                os.remove(os.path.join(path, file))
    else:
        print(f"路径 {path} 下没有标签文件")
