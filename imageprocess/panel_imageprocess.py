from imageprocess.panel_rotate import RotateApp
from tkbuilder.main_panel import MainPanelApp


class ImageProcessApp:
    def __init__(self):
        MainPanelApp(
            title="图片处理",
            width=400,
            height=100,
            buttons={
                "旋转": RotateApp,
            },
            button_width=10,
        )


if __name__ == "__main__":
    ImageProcessApp()
