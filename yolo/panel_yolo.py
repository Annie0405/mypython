from yolo.panel_train_data_split import TrainDataSplitApp
from yolo.panel_augment import AugmentApp
from tkbuilder.main_panel import MainPanelApp


class YOLOApp:
    def __init__(self):
        MainPanelApp(
            title="yolo工具助手",
            width=450,
            height=150,
            buttons={
                "训练集划分": TrainDataSplitApp,
                "数据增强": AugmentApp,
            },
            button_width=15,
        )
