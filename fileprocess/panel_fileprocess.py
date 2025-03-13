from fileprocess.panel_file_counter import FileCounterApp
from fileprocess.panel_rand_move import panel_rand_move
from fileprocess.panel_merge_dir import DirMergeApp
from fileprocess.panel_copy_files import CopyFilesApp
from fileprocess.panel_rename_files import RenameFilesApp
from fileprocess.panel_create_dir import DirCreateApp
from tkbuilder.main_panel import MainPanelApp


class FileProcessApp:
    def __init__(self):
        MainPanelApp(
            title="文件操作",
            width=400,
            height=200,
            buttons={
                "统计": FileCounterApp,
                "随机移动文件": panel_rand_move,
                "文件夹合并": DirMergeApp,
                "文件复制": CopyFilesApp,
                "文件重命名": RenameFilesApp,
                "创建文件夹": DirCreateApp,
            },
            button_width=15,
        )
