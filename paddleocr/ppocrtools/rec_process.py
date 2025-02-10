import json
import os
import cv2
import numpy as np
import time


def get_rotate_crop_image(img, points):
    # Use Green's theory to judge clockwise or counterclockwise
    # author: biyanhua
    d = 0.0
    for index in range(-1, 3):
        d += -0.5 * (points[index + 1][1] + points[index][1]) * (
                points[index + 1][0] - points[index][0])
    if d < 0:  # counterclockwise
        tmp = np.array(points)
        points[1], points[3] = tmp[3], tmp[1]

    try:
        img_crop_width = int(
            max(
                np.linalg.norm(points[0] - points[1]),
                np.linalg.norm(points[2] - points[3])))
        img_crop_height = int(
            max(
                np.linalg.norm(points[0] - points[3]),
                np.linalg.norm(points[1] - points[2])))
        pts_std = np.float32([[0, 0], [img_crop_width, 0],
                              [img_crop_width, img_crop_height],
                              [0, img_crop_height]])
        M = cv2.getPerspectiveTransform(points, pts_std)
        dst_img = cv2.warpPerspective(
            img,
            M, (img_crop_width, img_crop_height),
            borderMode=cv2.BORDER_REPLICATE,
            flags=cv2.INTER_CUBIC)
        dst_img_height, dst_img_width = dst_img.shape[0:2]
        if dst_img_height * 1.0 / dst_img_width >= 1.5:
            dst_img = np.rot90(dst_img)
        return dst_img
    except Exception as e:
        print(e)


def label2rec(path):
    # 标签文件路径
    label_txt_path = os.path.join(path, "Label.txt")
    # rec标签存储
    rec_list = []
    # 裁切图片保存路径
    crop_img_dir = os.path.join(path, "crop_img_gen")
    os.makedirs(crop_img_dir, exist_ok=True)
    # 遍历标签文件，切割每一张图片上的标注框
    with open(label_txt_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            # 分别取出图片名和标签列表
            image_name, label_list = line.split("\t")
            image_name = os.path.basename(image_name)
            label_list = json.loads(label_list)
            # 读入图片，路径中不能包含中文字符
            image_path = os.path.join(path, image_name)
            image = cv2.imread(image_path)
            # 处理每一个标签
            for idx, label in enumerate(label_list):
                transcript = label["transcription"]
                points = label["points"]
                points = np.array(points, dtype=np.float32)
                # 裁切标注区域
                crop_img = get_rotate_crop_image(image, points)
                # 裁切图片命名
                crop_img_name = image_name.split(".")[0] + "_crop_" + str(idx) + ".jpg"
                # 保存裁切图片
                crop_img_path = os.path.join(crop_img_dir, crop_img_name)
                cv2.imwrite(crop_img_path, crop_img)
                # 构建标签
                rec_label = crop_img_name + '\t' + transcript
                rec_list.append(rec_label)
    # 保存rec标签
    with open(os.path.join(path, "rec_gt_gen.txt"), "w", encoding="utf-8") as f:
        f.write('\n'.join(rec_list))
        f.write("\n")
    # 打印成功信息
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{current_time}] rec标注导出完成！")


def merge_rec_gt(path):
    # 在路径下查找所有包含"rec_gt"的txt文件
    label_file_list = []
    for file in os.listdir(path):
        if "rec_gt" in file and file.endswith(".txt"):
            label_file_list.append(file)
    if label_file_list:
        merge_content = ""
        for file in label_file_list:
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                content = f.read()
            if not content.endswith("\n"):
                content += "\n"
            merge_content += content
        with open(os.path.join(path, "rec_gt.txt"), "w", encoding="utf-8") as f:
            f.write(merge_content)
        print(f"已将所有标签文件合并至 {path}/rec_gt.txt")
        # 删掉原来的文件
        for file in label_file_list:
            if file != "rec_gt.txt":
                os.remove(os.path.join(path, file))
    else:
        print(f"路径 {path} 下没有标签文件")
