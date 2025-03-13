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
            new_part1 = []
            for field in part1:
                new_field = {"transcription": field["transcription"], "points": field["points"]}
                new_part1.append(new_field)
            new_line = part0 + "\t" + json.dumps(new_part1, ensure_ascii=False)
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


def check_det_labels(image_dir, label_file):
    info = ""

    # 获取图片目录下所有的图片文件名（不含路径）
    image_files = set(os.listdir(image_dir))

    # 读取标签文件，并解析每一行的图片名
    with open(label_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    label_dict = {}  # 用于存储标签信息
    for line in lines:
        parts = line.strip().split('\t', 1)  # 仅分割一次，获取图片名和标签
        if len(parts) < 2:
            continue  # 如果格式异常，跳过
        image_name = parts[0]
        label_dict[image_name] = line.strip()  # 保留原始行内容

    label_files = set(label_dict.keys())  # 标签文件中的所有图片名

    # 1. 删除只存在于 `image_dir` 而不在 `label_file` 中的图片
    images_to_remove = image_files - label_files
    for img in images_to_remove:
        img_path = os.path.join(image_dir, img)
        os.remove(img_path)
        info += f"删除不存在于标签文件中的图片: {img_path}\n"

    # 2. 删除只存在于 `label_file` 而不在 `image_dir` 中的图片标签
    labels_to_keep = [label_dict[img] for img in label_files if img in image_files]

    # 重新写入 `label_file`
    with open(label_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(labels_to_keep) + "\n")

    info += "校验完成，已同步图片和标签文件。"

    return info
