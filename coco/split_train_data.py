import os
import json
import random
import shutil


class TrainDataSplit:
    def __init__(self, root_dir: str, split_scale: dict):
        self.root_dir = root_dir
        self.split_scale = split_scale
        self.categories = []
        self.images = []
        self.annotations = []

        self.read_annotations()

        self.train = {"categories": self.categories, "images": [], "annotations": []}
        self.val = {"categories": self.categories, "images": [], "annotations": []}
        self.test = {"categories": self.categories, "images": [], "annotations": []}
        self.split_sets = {"train": self.train,
                           "val": self.val,
                           "test": self.test}

        self.split_train_data()
        self.save()

    def read_annotations(self):
        # 读入标签文件
        annotations = os.path.join(self.root_dir, "1_original_data_COCO", "annotations", "annotations_coco.json")
        with open(annotations, "r") as f:
            data = json.load(f)
        self.categories = data["categories"]
        self.images = data["images"]
        self.annotations = data["annotations"]

    def split_train_data(self):
        # 10个一组划分 images 列表
        group_num = 10
        group_list = [self.images[i:i + group_num] for i in range(0, len(self.images), group_num)]
        train = int(self.split_scale["train"])
        val = int(self.split_scale["val"])
        if self.split_scale["test"]:
            test = int(self.split_scale["test"])
        else:
            test = 0

        # 分组遍历标签列表
        for group in group_list:

            # 随机划分
            random.shuffle(group)

            train_group = group[:train]
            self.data_process(train_group, "train")

            val_group = group[train:train + val]
            self.data_process(val_group, "val")

            if test:
                test_group = group[train + val:]
                self.data_process(test_group, "test")

    def data_process(self, group, mode):
        # 更新 images 属性
        self.split_sets[mode]["images"] += group

        # 更新 annotations 属性
        for annotation in self.annotations:
            if annotation["image_id"] in [image["id"] for image in group]:
                self.split_sets[mode]["annotations"].append(annotation)

    def save(self):
        # 标签保存目录
        annotations_dir = os.path.join(self.root_dir, "2_labels", "annotations")
        os.makedirs(annotations_dir, exist_ok=True)

        for mode, data in self.split_sets.items():
            if mode == "test":
                if not data["images"]:
                    continue

            # 保存标签
            file_path = os.path.join(annotations_dir, mode + "_labels.json")
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

            # 复制图片
            for image in data["images"]:
                image_path = os.path.join(self.root_dir, "1_original_data_COCO", "images", image["file_name"])
                new_image_path = os.path.join(self.root_dir, "2_labels", mode + "_images", image["file_name"])
                os.makedirs(os.path.dirname(new_image_path), exist_ok=True)
                shutil.copy(image_path, new_image_path)

        print("划分完成！")
