import os
import json


def get_label_list(folder):
    """遍历目录下的 JSON 文件，提取唯一的标签列表"""
    label_set = set()  # 使用集合去重，提高效率

    with os.scandir(folder) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".json"):
                labels = _extract_labels(entry.path)
                label_set.update(labels)  # 直接添加到集合去重

    return sorted(label_set)  # 返回排序后的列表


def _extract_labels(file_path):
    """从 JSON 文件中提取标签"""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return {shape["label"] for shape in data.get("shapes", [])}  # 使用集合去重
