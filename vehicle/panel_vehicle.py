from vehicle.vin_verify import VINVerifyApp
from vehicle.panel_drv_lic_label_checker import DrvLicLabelCheckerApp
from tkbuilder.main_panel import MainPanelApp


class VehicleApp:
    def __init__(self):
        MainPanelApp(
            title="车辆相关",
            width=450,
            height=150,
            buttons={
                "VIN码验证器": VINVerifyApp,
                "行驶证标注验证器": DrvLicLabelCheckerApp,
            },
            button_width=15,
        )
