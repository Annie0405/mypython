import os
import json
import shutil
import numpy as np
from shapely.geometry import Polygon


def polygon_verify(labelme_dir):
    # 初始化计数器
    count = {"error_format": 0, "missing_points": 0, "unclosed": 0, "illegal": 0}

    # 遍历所有 JSON 文件
    for json_file in os.listdir(labelme_dir):
        if json_file.endswith(".json"):
            json_path = os.path.join(labelme_dir, json_file)

            # 检查 JSON 文件是否有效
            try:
                with open(json_path, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                count["error_format"] += 1
                print(f"JSON格式错误: {json_path}")
                continue

            # 检查多边形
            for shapes in data["shapes"]:
                points = shapes["points"]

                # 检查多边形顶点数量是否大于3
                if len(points) < 3:
                    count["missing_points"] += 1
                    print(f"多边形顶点数量小于3: {json_path}")
                    continue

                # 检查多边形是否合法
                polygon = Polygon(points)
                if not polygon.is_valid or polygon.area <= 0:
                    count["illegal"] += 1
                    print(f"多边形不合法: {json_path}")
                    continue

    # 打印错误信息
    print("错误信息:")
    for key, value in count.items():
        if value > 0:
            print(f"{key}: {value}")


class Labelme2COCO:
    def __init__(self, labelme_dir, COCO_dir):
        self.labelme_dir = labelme_dir
        self.COCO_dir = COCO_dir

        self.labelme_json = self.get_labelme_json()
        self.categories = self.get_categories()
        self.images = []
        self.annotations = []
        self.process_labelme_json()
        self.save()

    def get_labelme_json(self):
        labelme_json = []
        for file in os.listdir(self.labelme_dir):
            if file.endswith(".json"):
                labelme_json.append(os.path.join(self.labelme_dir, file))
        return labelme_json

    def get_categories(self):
        categories_file = os.path.join(self.COCO_dir, "categories_file.json")
        with open(categories_file, "r") as f:
            data = json.load(f)
        return data["categories"]

    def get_category_map(self):
        category_map = {}
        for category in self.categories:
            category_map[category["name"]] = [category["id"], category["iscrowd"]]
        return category_map

    @staticmethod
    def get_bbox(points):
        polygons = np.array(points)  # 转换为 NumPy 数组以便操作
        x_min = np.min(polygons[:, 0])  # x 坐标的最小值
        y_min = np.min(polygons[:, 1])  # y 坐标的最小值
        x_max = np.max(polygons[:, 0])  # x 坐标的最大值
        y_max = np.max(polygons[:, 1])  # y 坐标的最大值
        return [x_min, y_min, x_max - x_min, y_max - y_min]

    @staticmethod
    def get_segmentation(points):
        # 检查多边形是否闭合
        if points[0] != points[-1]:
            points.append(points[0])
        return [list(np.asarray(points).flatten())]

    def process_labelme_json(self):
        image_id = 0
        annotation_id = 0
        category_map = self.get_category_map()

        for file in os.listdir(self.labelme_dir):
            if file.endswith(".json"):
                json_file = os.path.join(self.labelme_dir, file)
                with open(json_file, "r") as f:
                    data = json.load(f)

                # 提取labelme标注中的信息，构建COCO格式的标注信息
                image_id += 1
                height = data["imageHeight"]
                width = data["imageWidth"]
                file_name = data["imagePath"]
                self.images.append({"id": image_id, "file_name": file_name, "height": height, "width": width})

                for shape in data["shapes"]:
                    points = shape["points"]
                    polygon = Polygon(points)

                    annotation_id += 1
                    category_id = category_map[shape["label"]][0]
                    bbox = Labelme2COCO.get_bbox(points)
                    area = round(polygon.area, 6)
                    segmentation = Labelme2COCO.get_segmentation(points)
                    iscrowd = category_map[shape["label"]][1]
                    self.annotations.append(({"id": annotation_id, "image_id": image_id, "category_id": category_id,
                                              "bbox": bbox, "area": area, "segmentation": segmentation,
                                              "iscrowd": iscrowd}))

    def save(self):
        # 转换标签
        data = {
            "categories": self.categories,
            "images": self.images,
            "annotations": self.annotations
        }
        save_dir = os.path.join(self.COCO_dir, "annotations")
        os.makedirs(save_dir, exist_ok=True)
        annotations_coco = os.path.join(save_dir, "annotations_coco.json")
        with open(annotations_coco, "w") as f:
            json.dump(data, f, indent=4)

        # 复制图片
        dst_dir = os.path.join(self.COCO_dir, "images")
        os.makedirs(dst_dir, exist_ok=True)
        for file in os.listdir(self.labelme_dir):
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
                src_path = os.path.join(self.labelme_dir, file)
                dst_path = os.path.join(dst_dir, file)
                shutil.copy(src_path, dst_path)

        print("转换完成！")
