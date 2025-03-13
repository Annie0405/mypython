# 提供一些接口，以便一键创建tk面板
# tkbuilder/__init__.py
from .panel_settings import setup_window
from .common_panel import CommonPanelApp

__all__ = [
    # functions
    'setup_window',
    # classes
    'CommonPanelApp',
]
