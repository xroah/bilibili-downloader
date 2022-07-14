import wx
from downloader.mainFrame import MainFrame

app = wx.App()
frm = MainFrame(None, title="Bilibili下载器")

app.MainLoop()
