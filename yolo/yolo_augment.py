"""
此文件用于数据增强
随机对图片进行裁剪、旋转、水平翻转，随机调整对比度、亮度
并且更新yolo标签
作用对象是yolo数据集
"""
import random
import cv2
import numpy as np
import os


def random_rotate(image, labels):
    """对图像和多边形进行随机旋转"""
    # 随机旋转图片
    center = (image.shape[1] // 2, image.shape[0] // 2)
    angle = random.randint(-5, 5)
    M = cv2.getRotationMatrix2D(center, angle, 1)
    rotate_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    # 更新yolo标签
    updated_labels = []
    image_shape = image.shape
    for label in labels:
        class_id, x_center, y_center, w, h = label
        # 将YOLO的归一化坐标转为图像像素坐标
        x_center_pixel = x_center * image_shape[1]
        y_center_pixel = y_center * image_shape[0]
        # 进行旋转变换
        new_center = np.dot(M, np.array([x_center_pixel, y_center_pixel, 1]))
        # 获取新的坐标
        new_x_center_pixel, new_y_center_pixel = new_center[0], new_center[1]
        # 将新的坐标转换为归一化的YOLO格式
        new_x_center = new_x_center_pixel / image_shape[1]
        new_y_center = new_y_center_pixel / image_shape[0]
        # 保持宽度和高度不变，YOLO标签的宽高不受旋转影响
        updated_labels.append([class_id, new_x_center, new_y_center, w, h])
    return rotate_image, updated_labels


def random_crop(image, labels):
    """随机裁剪图像，并更新多边形坐标"""
    # 图片尺寸
    image_height, image_width = image.shape[:2]
    # 标注范围
    min_label_x, max_label_x = 1, 0
    min_label_y, max_label_y = 1, 0
    for label in labels:
        _, x_c, y_c, w, h = label
        min_label_x = min(min_label_x, x_c - w / 2)
        max_label_x = max(max_label_x, x_c + w / 2)
        min_label_y = min(min_label_y, y_c - h / 2)
        max_label_y = max(max_label_y, y_c + h / 2)
    # 裁剪尺寸
    crop_attr = random.uniform(0.8, 0.95)
    new_w, new_h = int(image_width * crop_attr), int(image_height * crop_attr)
    # 裁剪范围
    crop_x_min = max(0, max_label_x - crop_attr)
    crop_x_max = min(min_label_x, 1 - crop_attr)
    crop_y_min = max(0, max_label_y - crop_attr)
    crop_y_max = min(max_label_y, 1 - crop_attr)
    # 防止 crop_x_min > crop_x_max 或 crop_y_min > crop_y_max 的异常
    if crop_x_min > crop_x_max or crop_y_min > crop_y_max:
        print("Invalid crop range. Returning original image and polygons.")
        return image, labels
    # 随机选择裁剪起点
    crop_x = random.uniform(crop_x_min, crop_x_max)
    crop_y = random.uniform(crop_y_min, crop_y_max)
    # 更新yolo标签
    for label in labels:
        label[1] = (label[1] - crop_x) / crop_attr
        label[2] = (label[2] - crop_y) / crop_attr
        label[3] = label[3] / crop_attr
        label[4] = label[4] / crop_attr
    # 裁剪图像
    crop_x = int(crop_x * image_width)
    crop_y = int(crop_y * image_height)
    crop_image = image[crop_y:crop_y + new_h, crop_x:crop_x + new_w]
    return crop_image, labels


def random_flip(image, labels):
    """随机水平翻转图像并更新多边形坐标"""
    if random.random() < 0.5:
        width = image.shape[1]
        image = cv2.flip(image, 1)
        # 修改x_center
        for label in labels:
            label[1] = 1 - label[1]
    return image, labels


def random_scale(image):
    """随机更改图像的亮度和对比度"""
    alpha = random.uniform(0.8, 1.2)
    beta = random.randint(-25, 25)
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image


def load_image_and_labels(image_path, label_path):
    """加载图像和标签"""
    image = cv2.imread(image_path)
    labels = []
    with open(label_path, 'r', encoding='utf-8') as f:
        for line in f:
            label = line.strip().split(' ')
            label = [label[0]] + list(map(float, label[1:]))
            labels.append(label)
    return image, labels


def save_augmented_image_and_labels(image, labels, file_name, out_image_dir, out_label_dir):
    """保存增强后的图像和标签"""
    # 保存图片
    output_image_path = os.path.join(out_image_dir, file_name + '.jpeg')
    cv2.imwrite(output_image_path, image)
    # 保存标签
    label_content = ''
    for label in labels:
        label_content = ' '.join(map(str, label)) + '\n'
    label_path = os.path.join(out_label_dir, file_name + '.txt')
    with open(label_path, 'w', encoding='utf-8') as f:
        f.write(label_content)


def augment_image_and_update_labels(image_path, label_path, out_image_dir, out_label_dir):
    """对图像和标签执行增强操作"""
    # 加载图像和标签
    image, labels = load_image_and_labels(image_path, label_path)
    # 随机增强图片并更新标签
    image, labels = random_crop(image, labels)
    image, labels = random_rotate(image, labels)
    image, labels = random_flip(image, labels)
    image = random_scale(image)

    # # 验证
    # height, width = image.shape[:2]
    # for label in labels:
    #     # 解析标签
    #     x_center, y_center, box_width, box_height = label[1:]
    #
    #     # 转换为像素坐标
    #     x_center *= width
    #     y_center *= height
    #     box_width *= width
    #     box_height *= height
    #
    #     # 计算矩形框的顶点坐标
    #     x_min = int(x_center - box_width / 2)
    #     y_min = int(y_center - box_height / 2)
    #     x_max = int(x_center + box_width / 2)
    #     y_max = int(y_center + box_height / 2)
    #
    #     # 绘制矩形框
    #     color = (0, 255, 0)  # 绿色框
    #     thickness = 2
    #     cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)
    # cv2.imshow('Augmented Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 构造新的文件名
    file_name = os.path.splitext(os.path.basename(image_path))[0] + '_aug'
    # 保存增强后的图片和标签
    save_augmented_image_and_labels(image, labels, file_name, out_image_dir, out_label_dir)


def process_directory(in_image_dir, in_label_dir, out_image_dir, out_label_dir):
    """处理输入目录下的所有图像和标签文件"""
    # 获取目录下所有符合条件的图像文件
    image_files = [f for f in os.listdir(in_image_dir) if f.endswith('.jpeg')]
    # 遍历每个图像文件
    for image_name in image_files:
        # 构造文件路径
        image_path = os.path.join(in_image_dir, image_name)
        label_path = os.path.join(in_label_dir, image_name.replace('.jpeg', '.txt'))
        # 调用增强图像和更新标签的处理函数
        augment_image_and_update_labels(image_path, label_path, out_image_dir, out_label_dir)


# 设置输入和输出目录（可以相同）
root_dir = r"/path/to/root"
in_image_dir = os.path.join(root_dir, 'in_image_dir')
in_label_dir = os.path.join(root_dir, 'in_label_dir')
out_image_dir = os.path.join(root_dir, 'out_image_dir')
out_label_dir = os.path.join(root_dir, 'out_label_dir')

# 执行数据增强
process_directory(in_image_dir, in_label_dir, out_image_dir, out_label_dir)
