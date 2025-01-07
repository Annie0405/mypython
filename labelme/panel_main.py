from panel_labelme2COCO import Labelme2COCOApp
from tkbuilder.main_panel import MainPanelApp

MainPanelApp(
    title="labelme工具助手",
    width=400,
    height=200,
    buttons={
     "labelme2COCO": Labelme2COCOApp,
    },
    button_width=15,
)
