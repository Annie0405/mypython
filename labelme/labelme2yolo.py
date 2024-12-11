"""
labelme矩形标签转换为yolo标签
输入是labelme标签所在根目录
输出是一个图片目录和一个标签目录
可以一键转换根目录下所有labelme项目的标签
适应分批次标注的场景
该脚本不做校验，请确保根目录下只有纯净的labelme项目文件夹
请确保labelme标签都符合规范，没有空的标签
"""
import json
import os
import shutil

# global variable
# 输入
root_dir = r"/path/to/root"
# 输出
out_image_dir = r"/path/to/images/output"
out_label_dir = r"/path/to/labels/output"
# 文件类型
image_type = ".jpeg"
labelme_label_type = ".json"
yolo_label_type = ".txt"
# 创建标签的映射，可创建多个，以便多个项目同时进行时能够方便地切换
project0 = {
    'label0': 0,
    'label1': 1,
}
# 指定映射字典
mapping = project0


def labelme2yolo(image_path, labelme_label_path, new_image_path, yolo_label_path, mapping):
    # 复制图片
    shutil.copy(image_path, new_image_path)
    # 转换标签
    with (open(labelme_label_path, 'r', encoding='utf-8') as labelme_label,
          open(yolo_label_path, 'w', encoding='utf-8') as yolo_label):
        labelme_data = json.load(labelme_label)
        image_width = labelme_data['imageWidth']
        image_height = labelme_data['imageHeight']
        for shape in labelme_data['shapes']:
            # 提取标注框属性
            points = shape['points']
            x_min = min([point[0] for point in points])
            y_min = min([point[1] for point in points])
            box_width = abs(points[0][0] - points[1][0])
            box_height = abs(points[0][1] - points[1][1])
            # 转换
            x_center = (x_min + box_width / 2) / image_width
            y_center = (y_min + box_height / 2) / image_height
            box_width /= image_width
            box_height /= image_height
            # 写入
            yolo_label.write(f"{mapping[shape['label']]} {x_center} {y_center} {box_width} {box_height}\n")


# 遍历根目录下所有labelme项目
for project in os.listdir(root_dir):
    print(f"正在处理项目：{project}")
    labelme_dir = os.path.join(root_dir, project)

    # 遍历labelme项目下的所有图片
    for image_name in os.listdir(labelme_dir):
        if image_name.endswith(image_type):
            # 构造待转换的图片路径和标签路径
            labelme_label_name = image_name.replace(image_type, labelme_label_type)
            image_path = os.path.join(labelme_dir, image_name)
            labelme_label_path = os.path.join(labelme_dir, labelme_label_name)
            # 构造输出的图片路径和标签路径
            new_image_path = os.path.join(out_image_dir, image_name)
            yolo_label_path = os.path.join(out_label_dir, image_name.replace(image_type, yolo_label_type))
            # 转换
            labelme2yolo(image_path, labelme_label_path, new_image_path, yolo_label_path, mapping)

print("所有项目已处理完毕")
