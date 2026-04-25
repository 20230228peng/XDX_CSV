# -*- coding: utf-8 -*-
import wx
import wx.xrc
import wx.lib.agw.ribbon as rb
import wx.aui

from Core.JSON_load import load_accelerator_config
import gettext
_ = gettext.gettext

class IndexFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=wx.Size(898, 734),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_ribbonBar1 = rb.RibbonBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                         wx.lib.agw.ribbon.RIBBON_BAR_DEFAULT_STYLE)
        self.m_ribbonPage1 = rb.RibbonPage(self.m_ribbonBar1, wx.ID_ANY, _(u"菜单"), wx.NullBitmap, 0)
        self.m_ribbonBar1.SetActivePage(self.m_ribbonPage1)
        self.m_ribbonPanel1 = rb.RibbonPanel(self.m_ribbonPage1, wx.ID_ANY, _(u"菜单"), wx.NullBitmap,
                                             wx.DefaultPosition, wx.DefaultSize,
                                             wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE)
        self.m_ribbonButtonBar1 = rb.RibbonButtonBar(self.m_ribbonPanel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                     0)
        self.m_ribbonButtonBar1.AddSimpleButton(6001, _(u"新建"), wx.Bitmap(u"./Image/Menu/新建.png", wx.BITMAP_TYPE_ANY),
                                                wx.EmptyString)
        self.m_ribbonButtonBar1.AddSimpleButton(6002, _(u"打开"), wx.Bitmap(u"./Image/Menu/打开.png", wx.BITMAP_TYPE_ANY),
                                                wx.EmptyString)
        self.m_ribbonButtonBar1.AddSimpleButton(6003, _(u"保存"), wx.Bitmap(u"./Image/Menu/保存.png", wx.BITMAP_TYPE_ANY),
                                                wx.EmptyString)
        self.m_ribbonButtonBar1.AddSimpleButton(6004, _(u"设置"), wx.Bitmap(u"./Image/Menu/设置.png", wx.BITMAP_TYPE_ANY),
                                                wx.EmptyString)
        self.m_ribbonPanel2 = rb.RibbonPanel(self.m_ribbonPage1, wx.ID_ANY, wx.EmptyString, wx.NullBitmap,
                                             wx.DefaultPosition, wx.DefaultSize,
                                             wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE | wx.lib.agw.ribbon.RIBBON_PANEL_STRETCH)
        self.m_ribbonGallery1 = rb.RibbonGallery(self.m_ribbonPanel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_ribbonGallery1.Append(wx.Bitmap(u"./Image/Ribbon/绘图工具.png", wx.BITMAP_TYPE_ANY), 6042)
        self.m_ribbonGallery1.Append(wx.Bitmap(u"./Image/Ribbon/绘图工具.png", wx.BITMAP_TYPE_ANY), 6043)
        self.m_ribbonPanel3 = rb.RibbonPanel(self.m_ribbonPage1, wx.ID_ANY, _(u"关于"), wx.NullBitmap,
                                             wx.DefaultPosition, wx.DefaultSize,
                                             wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE)
        self.m_ribbonToolBar1 = rb.RibbonToolBar(self.m_ribbonPanel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_ribbonToolBar1.AddSimpleTool(6010, wx.Bitmap(u"./Image/Ribbon/我的反馈.png", wx.BITMAP_TYPE_ANY),
                                            wx.EmptyString)
        self.m_ribbonToolBar1.AddSimpleTool(6011, wx.Bitmap(u"./Image/Ribbon/权限.png", wx.BITMAP_TYPE_ANY),
                                            wx.EmptyString)
        self.m_ribbonToolBar1.AddSimpleTool(6012, wx.Bitmap(u"./Image/Ribbon/问题.png", wx.BITMAP_TYPE_ANY),
                                            wx.EmptyString)
        self.m_ribbonPage2 = rb.RibbonPage(self.m_ribbonBar1, wx.ID_ANY, _(u"计算"), wx.NullBitmap, 0)

        self.m_ribbonPanel4 = rb.RibbonPanel(self.m_ribbonPage2, wx.ID_ANY, _(u"工具"), wx.NullBitmap,
                                             wx.DefaultPosition, wx.DefaultSize,
                                             wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE)
        self.m_ribbonButtonBar2 = rb.RibbonButtonBar(self.m_ribbonPanel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                     0)
        self.m_ribbonButtonBar2.AddSimpleButton(6020, _(u"绘图"), wx.Bitmap(u"./Image/Menu/绘图.png", wx.BITMAP_TYPE_ANY),
                                                wx.EmptyString)
        self.m_ribbonButtonBar2.AddSimpleButton(6021, _(u"自定义"),
                                                wx.Bitmap(u"./Image/Menu/自定义.png", wx.BITMAP_TYPE_ANY), wx.EmptyString)
        self.m_ribbonButtonBar2.AddSimpleButton(6022, _(u"测试"), wx.Bitmap(u"./Image/Menu/测试.png", wx.BITMAP_TYPE_ANY),
                                                wx.EmptyString)
        self.m_ribbonPanel5 = rb.RibbonPanel(self.m_ribbonPage2, wx.ID_ANY, _(u"计算"), wx.NullBitmap,
                                             wx.DefaultPosition, wx.DefaultSize,
                                             wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE | wx.lib.agw.ribbon.RIBBON_PANEL_STRETCH)
        self.m_ribbonToolBar3 = rb.RibbonToolBar(self.m_ribbonPanel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_ribbonToolBar3.AddSimpleTool(6030, wx.Bitmap(u"./Image/Ribbon/增加选项.png", wx.BITMAP_TYPE_ANY),
                                            wx.EmptyString)
        self.m_ribbonToolBar3.AddSimpleTool(6031, wx.Bitmap(u"./Image/Ribbon/增加选项.png", wx.BITMAP_TYPE_ANY),
                                            wx.EmptyString)
        self.m_ribbonPanel6 = rb.RibbonPanel(self.m_ribbonPage2, wx.ID_ANY, _(u"帮助"), wx.NullBitmap,
                                             wx.DefaultPosition, wx.DefaultSize,
                                             wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE)
        self.m_ribbonToolBar4 = rb.RibbonToolBar(self.m_ribbonPanel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_ribbonToolBar4.AddSimpleTool(6040, wx.Bitmap(u"./Image/Ribbon/文件夹配置.png", wx.BITMAP_TYPE_ANY),
                                            wx.EmptyString)
        self.m_ribbonToolBar4.AddSimpleTool(6041, wx.Bitmap(u"./Image/Ribbon/系统帮助.png", wx.BITMAP_TYPE_ANY),
                                            wx.EmptyString)
        self.m_ribbonBar1.Realize()

        bSizer2.Add(self.m_ribbonBar1, 0, wx.EXPAND, 5)

        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_notebook1 = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel1 = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_notebook1.AddPage(self.m_panel1, _(u"主页"), True)
        self.m_panel2 = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_notebook1.AddPage(self.m_panel2, _(u"自定义"), False)
        self.m_panel3 = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_notebook1.AddPage(self.m_panel3, _(u"测试"), False)

        bSizer3.Add(self.m_notebook1, 1, wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.m_statusBar1 = self.CreateStatusBar(5, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.m_statusBar1.SetStatusWidths([-4, -4, -2, -4, -1])  # 第5栏为伸缩栏
        self.Centre(wx.BOTH)

        # 调用快捷键
        self.load_id_select()
        # 处理快捷键函数
        self.setup_accelerators()

    def load_id_select(self, event=None):
        """
        工具栏函数点击事件函数表
        :param event:
        :return:
        """

        self.event_handlers = {
            6010: self.index_tool_6010,
            6011: self.index_tool_6011,
            6012: self.index_tool_6012,
            6030: self.index_tool_6030,
            6031: self.index_tool_6031,
            6040: self.index_tool_6040,
            6041: self.index_tool_6041

        }

        # 绑定工具栏按钮事件
        for tool_id, handler in self.event_handlers.items():
            self.Bind(rb.EVT_RIBBONTOOLBAR_CLICKED, handler, id=tool_id)

        self.event_dropdown_handlers = {
            6042: self.dropdown_6042,
        }

        for tool_dropdown_id, handler_dropdown in self.event_dropdown_handlers.items():
            self.Bind(rb.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, handler_dropdown, id=tool_dropdown_id)

        # 定义事件到函数的映射
        self.event_button_bindings = {
            6000: self.index_button_1,
            6001: self.index_button_2,
            6002: self.index_button_3,
            6003: self.index_button_4,
            6020: self.index_button_5,
            6021: self.index_button_6,
            6022: self.index_button_7,
        }

        # 绑定菜单栏按钮事件
        for event_id, handler in self.event_button_bindings.items():
            self.Bind(rb.EVT_RIBBONBUTTONBAR_CLICKED, handler, id=event_id)

    def setup_accelerators(self):
        """
        快捷键处理函数
        :return:
        """
        # 设置快捷键
        # 加载快捷键配置
        try:
            accelerator_entries = load_accelerator_config("Bin/Config/accelerators.json")
        except Exception as e:
            wx.LogError(f"加载快捷键配置失败: {str(e)}")
            accelerator_entries = []  # 可设置默认配置或退出

        # 创建加速器表
        accel_table = wx.AcceleratorTable(accelerator_entries)
        self.SetAcceleratorTable(accel_table)

        # 绑定事件处理（保持原有逻辑不变）
        for accel_button_tbl_id in self.event_handlers.keys():
            self.Bind(wx.EVT_MENU, self._on_button_accelerator, id=accel_button_tbl_id)

        for accel_tool_id in self.event_dropdown_handlers.keys():
            self.Bind(wx.EVT_MENU, self._on_tool_accelerator, id=accel_tool_id)

        for accel_item_id in self.event_button_bindings.keys():
            self.Bind(wx.EVT_MENU, self._on_item_accelerator, id=accel_item_id)

    def _on_item_accelerator(self, event):
        """
        调用需要进行相应的错误处理
        :param event:
        :return:

        """
        event_id = event.GetId()
        # 根据事件ID调用相应的方法
        handler = self.event_button_bindings.get(event_id)
        if handler:
            try:
                handler(event)
            except Exception as e:
                # 在这里处理异常，例如记录日志或显示错误消息
                wx.LogError(f"Error occurred in handler for event ID {event_id}: {e}")
        else:
            # 可选：如果处理函数不存在，也可以记录日志或显示警告
            wx.LogWarning(f"No handler found for event ID {event_id}")

    def _on_tool_accelerator(self, event):
        """
        调用需要进行相应的错误处理
        ID事件调用
        :param event:
        :return:

        """
        event_id = event.GetId()
        # 根据事件ID调用相应的方法
        handler = self.event_dropdown_handlers.get(event_id)
        if handler:
            try:
                handler(event)
            except Exception as e:
                # 在这里处理异常，例如记录日志或显示错误消息
                wx.LogError(f"Error occurred in handler for event ID {event_id}: {e}")
        else:
            # 可选：如果处理函数不存在，也可以记录日志或显示警告
            wx.LogWarning(f"No handler found for event ID {event_id}")

    def _on_button_accelerator(self, event):
        """
        调用需要进行相应的错误处理
        :param event:
        :return:
        """
        event_id = event.GetId()
        # 根据事件ID调用相应的方法
        handler = self.event_handlers.get(event_id)
        if handler:
            try:
                handler(event)
            except Exception as e:
                # 在这里处理异常，例如记录日志或显示错误消息
                wx.LogError(f"Error occurred in handler for event ID {event_id}: {e}")
        else:
            # 可选：如果处理函数不存在，也可以记录日志或显示警告
            wx.LogWarning(f"No handler found for event ID {event_id}")

    def index_tool_6010(self, event):

        event.Skip()

    def index_tool_6011(self, event):
        event.Skip()

    def index_tool_6012(self, event):
        event.Skip()
    def index_tool_6030(self, event):
        event.Skip()

    def index_tool_6031(self, event):
        event.Skip()

    def index_tool_6040(self, event):
        event.Skip()

    def index_tool_6041(self, event):
        event.Skip()

    def dropdown_6042(self, event):
        event.Skip()

    def index_button_1(self,event):
        event.Skip()

    def index_button_2(self,event):
        event.Skip()

    def index_button_3(self,event):
        event.Skip()

    def index_button_4(self,event):
        event.Skip()

    def index_button_5(self,event):
        event.Skip()

    def index_button_6(self,event):
        event.Skip()

    def index_button_7(self,event):
        event.Skip()

    def __del__(self):
        pass
