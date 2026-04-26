import os
import wx

from Src.Event.IndexMenu import IndexMenuEvent
# from UI.IndexUI import IndexFrame



if __name__ == '__main__':
    app = wx.App()

    # 图标和启动画面...
    icon_path = "XDX.ico"

    if os.path.exists(icon_path):
        app_icon = wx.Icon(icon_path, wx.BITMAP_TYPE_ICO)
    else:
        app_icon = wx.ArtProvider.GetIcon(wx.ART_INFORMATION)


    frame = IndexMenuEvent(None,"XDX_CSV Cal")
    frame.Show()
    app.MainLoop()