from PySide6.QtWidgets import QApplication, QSystemTrayIcon
from PySide6.QtCore import Qt

from .main_window import MainWindow
from .Tray import create_tray
from .utils.decorators import singleton
from .settings import SettingsDialog


@singleton
class App(QApplication):
    def __init__(self):
        super().__init__()
        tray_avail = QSystemTrayIcon.isSystemTrayAvailable()
        self.main_win = MainWindow()
        self.settings_dialog = SettingsDialog(self.main_win)
        # Keyboard shortcuts on macOS are typically based on the Command
        # (or Cmd) keyboard modifier, represented by the ⌘ symbol.
        # For example, the ‘Copy’ action is Command+C (⌘+C).
        # To ease cross platform development Qt will
        # by default remap Command to the ControlModifier ,
        # to align with other platforms.
        # This allows creating keyboard shortcuts such as “Ctrl+J”,
        # which on macOS will then map to Command+J,
        # as expected by macOS users. The actual Control (or Ctrl)
        # modifier on macOS, represented by ⌃,
        # is mapped to MetaModifier .
        self.setAttribute(Qt.AA_MacDontSwapCtrlAndMeta, True)
        self.applicationStateChanged.connect(self.state_change)

        if tray_avail:
            self.tray = create_tray(self, self.main_win)

    def state_change(self, state):
        if (
                state == Qt.ApplicationActive and
                not self.main_win.isVisible() and
                self.tray is not None and
                # macos: if the window is hidden,
                # it will not show when click dock icon,
                # but the app state will be active
                # windows: tray right click will activate the app
                not self.tray.menu_visible
        ):
            self.tray.show_win()
