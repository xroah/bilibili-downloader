from ..CommonWidgets import Dialog

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QMainWindow,
    QDialog,
    QLabel
)

def create_settings_dialog(window: QMainWindow) -> QDialog:
    dialog = Dialog(
        parent=window,
        title="设置",
        content=QLabel("设置"),
        size=QSize(500, 300),
        show_cancel=True
    )
    dialog.open()

    return dialog