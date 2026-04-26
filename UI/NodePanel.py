# -*- coding: utf-8 -*-
import wx
import wx.aui
import gettext

from Src.NodeGraph import NodeGraphBase, EVT_GSNODEGRAPH_ADDNODEBTN
from Src.NodeGraph.sample.example import InputNode, RMSNode, ActiveNode, IdleNode, OutputNode, ConditionalNode

_ = gettext.gettext


class NodePanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super(NodePanel, self).__init__(parent, *args, **kw)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel6 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        node_registry = {
            "input_node": InputNode,
            "rms_node": RMSNode,
            "active_node": ActiveNode,
            "idle_node": IdleNode,
            "output_node": OutputNode,
            "conditional_node": ConditionalNode,
        }

        # 定义配置字典 (config)
        config = {
            "image_datatype": "DEFAULT",
            "node_datatypes": {
                "DEFAULT": "#C6C62D",  # 黄色
                "INTEGER": "#A0A0A0",  # 灰色
                "FLOAT": "#A0A0A0",  # 灰色
            },
            "input_nodes_categories": ["INPUT"],
            "node_categories": {  # 节点分类的配色方案
                "INPUT": "#E64555",  # 红色系
                "OUTPUT": "#558333",  # 绿色系
                "ACTIVE": "#54FFEC",  # 青色系
                "IDLE": "#6856FF",  # 浅蓝
                "UNDEFINED": "#FFB54D",  # 橙色系
                "RMS": "#FDFF52",  # 黄色系
            }
        }

        # 初始化 NodeGraphBase 控件
        self.node_graph = NodeGraphBase(self.m_panel6, registry=node_registry, config=config)

        # 为 m_panel6 设置布局，使 node_graph 填满整个面板
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(self.node_graph, 1, wx.EXPAND)
        self.m_panel6.SetSizer(panel_sizer)
        self.m_panel6.Layout()

        bSizer10.Add(self.m_panel6, 1, wx.EXPAND, 5)

        self.m_auiToolBar1 = wx.aui.AuiToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                               wx.aui.AUI_TB_HORZ_LAYOUT | wx.aui.AUI_TB_VERTICAL)
        self.m_tool1 = self.m_auiToolBar1.AddTool(7000, _(u"tool"), wx.Bitmap(u"./Image/Ribbon/绘图工具.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                                  wx.EmptyString, wx.EmptyString, None)

        self.m_tool2 = self.m_auiToolBar1.AddTool(7001, _(u"tool"), wx.Bitmap(u"./Image/Ribbon/绘图工具.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                                  wx.EmptyString, wx.EmptyString, None)

        self.m_tool3 = self.m_auiToolBar1.AddTool(7002, _(u"tool"), wx.Bitmap(u"./Image/Ribbon/绘图工具.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                                  wx.EmptyString, wx.EmptyString, None)

        self.m_tool4 = self.m_auiToolBar1.AddTool(7003, _(u"tool"), wx.Bitmap(u"./Image/Ribbon/绘图工具.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                                  wx.EmptyString, wx.EmptyString, None)

        self.m_tool5 = self.m_auiToolBar1.AddTool(7004, _(u"tool"), wx.Bitmap(u"./Image/Ribbon/绘图工具.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                                  wx.EmptyString, wx.EmptyString, None)

        self.m_tool6 = self.m_auiToolBar1.AddTool(7005, _(u"tool"), wx.Bitmap(u"./Image/Ribbon/绘图工具.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                                  wx.EmptyString, wx.EmptyString, None)

        self.m_tool7 = self.m_auiToolBar1.AddTool(7006, _(u"tool"), wx.Bitmap(u"./Image/Ribbon/绘图工具.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                                  wx.EmptyString, wx.EmptyString, None)

        self.m_auiToolBar1.Realize()

        bSizer10.Add(self.m_auiToolBar1, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer10)
        self.Layout()

        # 绑定事件
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.node_graph.Bind(EVT_GSNODEGRAPH_ADDNODEBTN, self.OnAddNodeMenuBtn)
        self.Bind(wx.EVT_TOOL, self.tool_event_1, id =7000)

        # 刷新界面
        self.node_graph.Refresh()


    def tool_event_1(self, event):
        print("tool_event_1")

    def OnAddNodeMenuBtn(self, event):
        """
        增加节点事件 - 控制AUI工具条的显示/隐藏
        :param event:
        :return:
        """

        # 切换工具条的可见性
        if self.m_auiToolBar1.IsShown():
            self.m_auiToolBar1.Hide()
        else:
            self.m_auiToolBar1.Show()

        self.Layout()

    def OnSize(self, event):
        """窗口大小改变事件"""
        event.Skip()
        self.node_graph.Refresh()


    def __del__(self):
        pass
