from panel_split_train_data import TrainDataSpiltApp
from tkbuilder.main_panel import MainPanelApp

MainPanelApp(
    title="COCO工具助手",
    width=400,
    height=200,
    buttons={
     "训练集分割": TrainDataSpiltApp,
    },
    button_width=15,
)
