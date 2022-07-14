import wx
from ..utils import utils


class MainFrame(wx.Frame):
    __min_w = 1024
    __min_h = 768

    def __init__(self, *args, **kwargs):
        size = wx.Size(self.__min_w, self.__min_h)

        super().__init__(*args, size=size, **kwargs)
        icon = wx.Icon()
        icon.LoadFile(utils.get_resource_path("logo.png"), wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        self.SetMinSize(size)
