from vehicle.vin_verify import VINVerifyApp
from tkbuilder.main_panel import MainPanelApp


class VehicleApp:
    def __init__(self):
        MainPanelApp(
            title="车辆相关",
            width=450,
            height=100,
            buttons={
                "VIN码验证器": VINVerifyApp,
            },
            button_width=15,
        )
