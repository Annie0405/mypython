from coco.panel_coco import COCOApp
from labelme.panel_labelme import LabelmeApp
from paddleocr.ppocrtools.panel_ppocrtools import PPOCRToolsApp
from yolo.panel_yolo import YOLOApp
from fileprocess.panel_fileprocess import FileProcessApp
from hash.panel_hash import HashApp
from imageprocess.panel_imageprocess import ImageProcessApp
from vehicle.panel_vehicle import VehicleApp
from tkbuilder.main_panel import MainPanelApp


MainPanelApp(
    title="主面板",
    width=450,
    height=350,
    buttons={
        "COCO工具助手": COCOApp,
        "labelme工具助手": LabelmeApp,
        "ppocr工具助手": PPOCRToolsApp,
        "yolo工具助手": YOLOApp,
        "文件操作": FileProcessApp,
        "文件去重": HashApp,
        "图片处理": ImageProcessApp,
        "车辆相关": VehicleApp,
    },
    button_width=15,
)
