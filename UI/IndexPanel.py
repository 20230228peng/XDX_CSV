import wx
import wx.xrc
import wx.dataview


class IndexPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super(IndexPanel, self).__init__(parent, *args, **kw)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_dataViewTreeCtrl1 = wx.dataview.DataViewTreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_dataViewTreeCtrl1.SetMinSize(wx.Size(150, -1))
        self.m_dataViewTreeCtrl1.SetMaxSize(wx.Size(200, -1))

        bSizer5.Add(self.m_dataViewTreeCtrl1, 1, wx.ALL | wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)

        bSizer3.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.m_filePicker1 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, _(u"Select a file"), _(u"*.*"),
                                               wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        bSizer3.Add(self.m_filePicker1, 1, wx.ALL, 5)

        bSizer8.Add(bSizer3, 0, wx.EXPAND, 5)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer1.Add(self.m_panel1, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel2 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer1.Add(self.m_panel2, 1, wx.EXPAND | wx.ALL, 5)

        bSizer8.Add(gSizer1, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)

        fgSizer1.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        bSizer4.Add(fgSizer1, 1, wx.EXPAND, 5)

        bSizer8.Add(bSizer4, 1, wx.EXPAND, 5)

        bSizer5.Add(bSizer8, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer5)
        self.Layout()

    def __del__(self):
        pass
