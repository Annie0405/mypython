from labelme.panel_labelme2COCO import Labelme2COCOApp
from labelme.panel_labelme2COCO_split import Labelme2COCOSplitApp
from labelme.panel_labelme2det import Labelme2DetApp
from tkbuilder.main_panel import MainPanelApp


class LabelmeApp:
    def __init__(self):
        MainPanelApp(
            title="labelme工具助手",
            width=400,
            height=200,
            buttons={
                "labelme2COCO": Labelme2COCOApp,
                "labelme一键转COCO并划分": Labelme2COCOSplitApp,
                "labelme2det": Labelme2DetApp,
            },
            button_width=30,
        )
