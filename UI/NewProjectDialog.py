import wx
import os
import wx.adv
import gettext
_ = gettext.gettext


class NewProjectDialog(wx.Dialog):

    def __init__(self, parent, default_path):

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                           size=wx.Size(296, 314), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.default_path = default_path

        self.SetBackgroundColour(wx.Colour(199, 228, 227))

        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, _(u"新建项目"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        self.m_staticText3.SetFont(
            wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))

        bSizer11.Add(self.m_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_dirPicker2 = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition,
                                             wx.DefaultSize, wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        bSizer11.Add(self.m_dirPicker2, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticline3 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer11.Add(self.m_staticline3, 0, wx.EXPAND | wx.ALL, 5)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, _(u"项目名称："), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        fgSizer1.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.m_textCtrl1, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, _(u"项目类型："), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)

        fgSizer1.Add(self.m_staticText5, 0, wx.ALL, 5)

        m_comboBox1Choices = [_(u"默认")]
        self.m_comboBox1 = wx.ComboBox(self, wx.ID_ANY, _(u"默认"), wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox1Choices, 0)
        self.m_comboBox1.SetSelection(0)
        fgSizer1.Add(self.m_comboBox1, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, _(u"创建人："), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)

        fgSizer1.Add(self.m_staticText6, 0, wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, _(u"创建日期："), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)

        fgSizer1.Add(self.m_staticText7, 0, wx.ALL, 5)

        self.m_datePicker1 = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition,
                                                   wx.DefaultSize, wx.adv.DP_DROPDOWN)
        fgSizer1.Add(self.m_datePicker1, 0, wx.ALL | wx.EXPAND, 5)

        bSizer11.Add(fgSizer1, 0, wx.EXPAND, 5)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer11.Add(self.m_staticline2, 0, wx.EXPAND | wx.ALL, 5)

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize();

        bSizer11.Add(m_sdbSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer11)
        self.Layout()

        self.Centre(wx.BOTH)
        self.m_dirPicker2.SetPath(self.default_path)
        self.m_textCtrl1.Bind(wx.EVT_TEXT, self.on_project_name_changed)

    # 添加事件处理方法
    def on_project_name_changed(self, event):
        project_name = self.m_textCtrl1.GetValue().strip()
        if project_name:
            default_full_path = os.path.join(self.default_path, project_name)
            self.m_dirPicker2.SetPath(default_full_path)
        else:
            self.m_dirPicker2.SetPath(self.default_path)
        event.Skip()


    def __del__(self):
        pass


