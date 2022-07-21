from glob import glob
from tkinter.messagebox import NO
from ..CommonWidgets import Dialog

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QMainWindow,
    QDialog,
    QLabel
)

_dialog: Dialog | None = None

def close():
    global _dialog
    if _dialog is not None:
        _dialog.close()
        _dialog = None

def create_settings_dialog(window: QMainWindow) -> None:
    global _dialog

    if _dialog is not None:
        close()

    _dialog = Dialog(
        parent=window,
        title="设置",
        content=QLabel("设置"),
        size=QSize(500, 300),
        show_cancel=True,
        is_modal=False
    )
    _dialog.open_()
    _dialog.finished.connect(close)


    return _dialog
