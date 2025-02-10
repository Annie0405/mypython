from labelme.labelme2COCO import polygon_verify


class Labelme2COCOSplit:
    def __init__(self, root_dir: str, split_scale: dict):
        self.root_dir = root_dir
        self.split_scale = split_scale

    @staticmethod
    def verify(labelme_dir):
        polygon_verify(labelme_dir)
