from PIL import Image
import os


def batch_rotate(image_dir, angle):
    angle = int(angle)
    with os.scandir(image_dir) as entries:
        for entry in entries:
            if entry.is_file():
                file_path = entry.path

                with Image.open(file_path) as image:
                    image = image.rotate(angle, expand=True)
                    image.save(file_path)   # 覆盖原文件

    return "所有图片已成功旋转！"
