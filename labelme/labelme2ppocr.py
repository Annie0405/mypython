import os
import shutil
import json
import time


def labelme2det(input_path, output_path):
    """
    此方法只支持单目标检测
    input_path: 文件夹路径，里面是图片和labelme标签
    output_path: 文件夹路径，需将图片复制到此处，并生成ppocr格式的det标签文件
    """
    def _copy(image):
        image_path = os.path.join(input_path, image)
        new_image_path = os.path.join(output_path, image)
        shutil.copyfile(image_path, new_image_path)

    def _convert(image):
        label = image.split('.')[0] + '.json'
        with open(os.path.join(input_path, label), 'r') as f:
            content = json.load(f)
            points = content['shapes'][0]['points']
        xmin = int(min(points[0][0], points[1][0]))
        xmax = int(max(points[0][0], points[1][0]))
        ymin = int(min(points[0][1], points[1][1]))
        ymax = int(max(points[0][1], points[1][1]))
        det_points = [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]
        det_label = image + '\t' + '[{"points": ' + str(det_points) + '}]'
        return det_label

    # 初始化det标签
    det_labels = []

    # 遍历输入文件夹中的所有图片
    for image in os.listdir(input_path):
        if image.endswith('.jpg') or image.endswith('.png') or image.endswith('.jpeg'):
            # 复制图片
            _copy(image)
            # 构造det标签
            det_label = _convert(image)
            det_labels.append(det_label)

    # 生成det标签
    with open(os.path.join(output_path, 'Label.txt'), 'w') as f:
        f.write('\n'.join(det_labels))
        f.write("\n")

    # 转换完毕，打印信息
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{current_time}] det标注导出完成！")
