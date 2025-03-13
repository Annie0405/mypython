import os
import shutil
import json
import cv2
import numpy as np
from paddleocr import get_rotate_crop_image


def labelme2det(input_path, output_path, selected_labels, is_crop):
    """
    此方法只支持单目标检测
    input_path: 文件夹路径，里面是图片和labelme标签
    output_path: 文件夹路径，需将图片复制到此处，并生成ppocr格式的det标签文件
    selected_labels: 要转换的标签类型，为空默认全部转换
    """
    def _copy(image_path):
        new_image_path = os.path.join(output_path, os.path.basename(image_path))
        shutil.copyfile(image_path, new_image_path)

    def _crop(image_path, key_cls, points, crop_cnt):
        image = cv2.imread(image_path)
        image_name = os.path.basename(image_path)
        points = np.array(points, dtype=np.float32)
        crop_img = get_rotate_crop_image(image, points)
        crop_img_name = image_name.split(".")[0] + str(crop_cnt) + key_cls + ".jpg"
        crop_dir = os.path.join(output_path, 'crop_img')
        os.makedirs(crop_dir, exist_ok=True)
        crop_img_path = os.path.join(crop_dir, crop_img_name)
        cv2.imwrite(crop_img_path, crop_img)

    def _convert(image_path):
        image_name = os.path.basename(image_path)
        label = image_name.split('.')[0] + '.json'
        with open(os.path.join(input_path, label), 'r') as f:
            content = json.load(f)
            shapes = content['shapes']
        annotations = []
        crop_cnt = 0
        for shape in shapes:
            key_cls = shape['label']
            if selected_labels and key_cls not in selected_labels:
                continue
            points = shape['points']
            points = [[int(point[0]), int(point[1])] for point in points]
            if shape['shape_type'] == 'polygon':
                pass
            elif shape['shape_type'] == 'rectangle':
                xmin = min(points[0][0], points[1][0])
                xmax = max(points[0][0], points[1][0])
                ymin = min(points[0][1], points[1][1])
                ymax = max(points[0][1], points[1][1])
                points = [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]
            else:
                raise ValueError('不支持的shape_type：{}'.format(shape['shape_type']))

            if is_crop:
                crop_cnt += 1
                _crop(image_path, key_cls, points, crop_cnt)

            annotation = {'transcription': "", 'points': points, 'key_cls': key_cls}
            annotations.append(annotation)
        det_label = image_name + '\t' + json.dumps(annotations, ensure_ascii=False)
        return det_label

    # 初始化det标签
    det_labels = []

    # 遍历输入文件夹中的所有图片
    with os.scandir(input_path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(('.jpg', '.png', '.jpeg')):
                try:
                    det_label = _convert(entry.path)  # 构造 det 标签
                    det_labels.append(det_label)
                    _copy(entry.path)  # 复制图片
                except Exception as e:
                    print(e)
                    continue

    # 生成det标签
    with open(os.path.join(output_path, 'Label.txt'), 'w') as f:
        f.write('\n'.join(det_labels))
        f.write("\n")

    # 转换完毕，打印信息
    return "det标注导出完成！"
