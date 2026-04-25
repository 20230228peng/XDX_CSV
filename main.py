
import wx
from UI.IndexUI import IndexFrame



if __name__ == '__main__':
    app = wx.App()
    frame = IndexFrame(None,"XDX_CSV Cal")
    frame.Show()
    app.MainLoop()