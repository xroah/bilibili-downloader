import wx
from mainFrame.MainFrame import MainFrame


app = wx.App()
frm = MainFrame(None, title="BiliBili下载器")

frm.Show()
app.MainLoop()
