"""
ppocr相关工具的可视化面板
集成所有ppocr工具
"""
from paddleocr.ppocrtools.panel_spilt_train_val_test import TrainValTestSplitterApp
from paddleocr.ppocrtools.panel_label2detrec import Label2DetRecApp
from paddleocr.ppocrtools.panel_merge_label import MergeLabelApp
from paddleocr.ppocrtools.panel_merge_rec_gt import MergeRecGtApp
from tkbuilder.main_panel import MainPanelApp


class PPOCRToolsApp:
    def __init__(self):
        MainPanelApp(
            title="ppocr工具助手",
            width=400,
            height=180,
            buttons={
                "训练集划分": TrainValTestSplitterApp,
                "Label文件中导出det或rec标注": Label2DetRecApp,
                "Label合并": MergeLabelApp,
                "rec_gt合并": MergeRecGtApp,
            },
            button_width=30,
        )
