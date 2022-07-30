from ..common_widgets import Dialog

import __main__

import sys
from PySide6 import __version__
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QMainWindow,
)


def get_python_ver():
    ver = sys.version_info
    return "{0}.{1}.{2}".format(ver.major, ver.minor, ver.micro)


def create_about_dialog(window: QMainWindow) -> None:
    dialog = Dialog(
        window,
        QSize(260, 200),
        "关于"
    )
    template = """
        <div style="font-size: 16px; line-height: 1.5;">
            <div><strong>Bilibili下载器</strong></div>
            <div>版本: {ver}</div>
            <div>
                <a style="text-decoration: none;" href="https://www.qt.io/">
                    PySide6:
                </a>
                {pyside_ver}
            </div>
            <div>
                <a style="text-decoration: none;" href="https://www.python.org">
                    Python:
                </a>
                {python_ver}
            </div>
        </div>
    """

    text = template.format(
        ver=__main__.__version__,
        pyside_ver=__version__,
        python_ver=get_python_ver()
    )

    w = QWidget(dialog.body)
    about = QLabel()
    layout = QVBoxLayout()
    about.setText(text)
    about.setOpenExternalLinks(True)
    layout.addWidget(about)
    w.setLayout(layout)
    dialog.set_content(w)

    dialog.open()
