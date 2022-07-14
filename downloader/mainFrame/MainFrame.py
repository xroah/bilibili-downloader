import wx
from ..utils import utils


class MainFrame(wx.Frame):
    __min_w = 1080
    __min_h = 720

    def __init__(self, *args, **kwargs):
        size = wx.Size(self.__min_w, self.__min_h)
        super().__init__(*args, size=size, **kwargs)

        left_width = 180
        self.left_panel = wx.Panel(
            self,
            size=wx.Size(left_width, wx.EXPAND),
            pos=wx.Point(0, 0)
        )
        self.downloaded_panel = wx.Panel(
            self,
            size=wx.Size(wx.EXPAND, wx.EXPAND),
            pos=wx.Point(left_width, 0)
        )
        self.downloading_panel = wx.Panel(
            self,
            size=wx.Size(wx.EXPAND, wx.EXPAND),
            pos=wx.Point(left_width, 0)
        )
        icon = wx.Icon()
        icon.LoadFile(utils.get_resource_path("logo.png"), wx.BITMAP_TYPE_PNG)

        self.SetIcon(icon)
        self.SetMinSize(size)
        self.set_layout()
        self.set_nav()
        self.init_right()
        self.Show()

    def set_layout(self):
        self.left_panel.SetAutoLayout(True)
        self.downloaded_panel.SetAutoLayout(True)
        self.downloaded_panel.SetBackgroundColour(wx.Colour(0, 255, 255, 255))
        self.downloading_panel.SetAutoLayout(True)
        self.downloading_panel.SetBackgroundColour(
            wx.Colour(32, 178, 170, 255))
        self.downloaded_panel.Hide()

    def on_select(self, e: wx.CommandEvent):
        s = e.GetString()

        if s == "正在下载":
            self.downloaded_panel.Hide()
            self.downloading_panel.Show()
        elif s == "已下载":
            self.downloaded_panel.Show()
            self.downloading_panel.Hide()

    def set_nav(self):
        choices = ["正在下载", "已下载"]
        width = self.left_panel.GetSize().GetWidth()
        lb = wx.ListBox(
            self.left_panel,
            choices=choices,
            size=wx.Size(width, wx.EXPAND)
        )
        sizer = wx.BoxSizer()
        sizer.Add(lb)
        lb.Bind(wx.EVT_LISTBOX, self.on_select)
        lb.SetSelection(0)
        lb.SetBackgroundColour(wx.Colour(65, 105, 225, 128))
        self.left_panel.SetSizer(sizer)

    def init_right(self):
        sizer1 = wx.BoxSizer()
        sizer2 = wx.BoxSizer()
        st1 = wx.StaticText(self.downloading_panel, label="正在下载。。。")
        st2 = wx.StaticText(self.downloaded_panel, label="已下载。。。")
        sizer1.Add(st1)
        sizer2.Add(st2)

        self.downloading_panel.SetSizer(sizer1)
        self.downloaded_panel.SetSizer(sizer2)
