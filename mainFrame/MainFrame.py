import wx
from pathlib import Path


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        p = Path(f"{__file__}/../..")
        d = p.resolve()
        icon = wx.Icon()
        icon.LoadFile(f"{d}/resources/logo.png", wx.BITMAP_TYPE_PNG)

        self.SetIcon(icon)
        self.SetMinSize(wx.Size(1024, 768))
