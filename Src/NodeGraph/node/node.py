
import wx
from Src.NodeGraph.assets.bitmaps import ICON_IMAGE,ICON_BRUSH_CHECKERBOARD
from .socket import NodeSocket
from .utils import TruncateText
from ..constants import (NODE_DEFAULT_WIDTH, NODE_DEFAULT_HEIGHT,
                         NODE_HEADER_MUTED_COLOR,
                         SOCKET_INPUT, SOCKET_OUTPUT, NODE_THUMB_PADDING, NODE_Y_PADDING,
                         NODE_NORMAL_COLOR, NODE_MUTED_COLOR, NODE_THUMB_BORDER_COLOR,
                         NODE_BORDER_NORMAL_COLOR, NODE_BORDER_SELECTED_COLOR)

class NodePropertyDialog(wx.Dialog):

    """
    TODO  属性弹窗需要重新编辑 20260420


    """
    def __init__(self, parent, node):
        super().__init__(parent, title=f"编辑节点属性 - {node.label}", size=(600, 650))
        self.node = node
        self.property_controls = {}      # 属性值控件字典
        self.property_label_controls = {} # 属性名称控件字典

        self.InitUI()
        self.Centre()

    def InitUI(self):
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 基本信息区域（节点标签、ID、类型）
        info_box = wx.StaticBox(panel, label="基本信息")
        info_sizer = wx.StaticBoxSizer(info_box, wx.VERTICAL)

        # 节点标签（可编辑）
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_sizer.Add(wx.StaticText(panel, label="节点标签:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.label_ctrl = wx.TextCtrl(panel, value=self.node.label)
        label_sizer.Add(self.label_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        info_sizer.Add(label_sizer, 0, wx.EXPAND)

        # 节点ID（只读）
        id_sizer = wx.BoxSizer(wx.HORIZONTAL)
        id_sizer.Add(wx.StaticText(panel, label="节点ID:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        id_ctrl = wx.TextCtrl(panel, value=self.node.id, style=wx.TE_READONLY)
        id_sizer.Add(id_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        info_sizer.Add(id_sizer, 0, wx.EXPAND)

        # 节点类型（只读）
        type_sizer = wx.BoxSizer(wx.HORIZONTAL)
        type_sizer.Add(wx.StaticText(panel, label="节点类型:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        type_ctrl = wx.TextCtrl(panel, value=self.node.idname, style=wx.TE_READONLY)
        type_sizer.Add(type_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        info_sizer.Add(type_sizer, 0, wx.EXPAND)

        main_sizer.Add(info_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # 属性编辑区域（支持修改属性名称和值）
        if self.node.properties:
            prop_box = wx.StaticBox(panel, label="输入属性")
            prop_sizer = wx.StaticBoxSizer(prop_box, wx.VERTICAL)

            for prop_id, prop in self.node.properties.items():
                # 每个属性使用一个容器面板
                prop_panel = wx.Panel(panel)
                prop_grid_sizer = wx.FlexGridSizer(2, 2, 5, 5)  # 2行2列，便于布局
                prop_grid_sizer.AddGrowableCol(1, 1)

                # 属性名称标签（静态文本）
                name_label = wx.StaticText(prop_panel, label="属性名称:")
                prop_grid_sizer.Add(name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

                # 属性名称编辑框（可修改）
                name_ctrl = wx.TextCtrl(prop_panel, value=prop.label)
                prop_grid_sizer.Add(name_ctrl, 1, wx.EXPAND)


                prop_panel.SetSizer(prop_grid_sizer)
                prop_sizer.Add(prop_panel, 0, wx.EXPAND | wx.ALL, 3)

                # 保存控件引用

                self.property_label_controls[prop_id] = name_ctrl

            main_sizer.Add(prop_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # 按钮区域
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(panel, wx.ID_OK, "确定")
        cancel_btn = wx.Button(panel, wx.ID_CANCEL, "取消")
        btn_sizer.Add(ok_btn, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        panel.SetSizer(main_sizer)

    def GetUpdatedValues(self):
        """获取更新后的值，包括节点标签、属性名称和属性值"""
        values = {
            'label': self.label_ctrl.GetValue(),
            'properties': {},
            'property_labels': {}
        }

        for prop_id, ctrl in self.property_controls.items():
            try:
                if isinstance(ctrl, wx.SpinCtrl):
                    values['properties'][prop_id] = int(ctrl.GetValue())
                elif isinstance(ctrl, wx.CheckBox):
                    values['properties'][prop_id] = ctrl.GetValue()
                else:
                    values['properties'][prop_id] = ctrl.GetValue()
            except Exception as e:
                print(f"⚠ 获取属性 {prop_id} 的值时出错: {e}")
                values['properties'][prop_id] = ""

        for prop_id, name_ctrl in self.property_label_controls.items():
            try:
                values['property_labels'][prop_id] = name_ctrl.GetValue()
            except Exception as e:
                print(f"⚠ 获取属性 {prop_id} 的名称时出错: {e}")
                values['property_labels'][prop_id] = ""

        return values



class NodeBase(object):

    def __init__(self, nodegraph, id):
        self.nodegraph = nodegraph
        self.id = id
        self.idname = None
        self.pos = wx.Point(0, 0)
        self.size = wx.Size(NODE_DEFAULT_WIDTH, NODE_DEFAULT_HEIGHT)
        self.header_color = wx.Colour("#242424")

        self.expanded = False
        self.selected = False
        self.active = False
        self.muted = False
        self.is_output = False

        self.sockets = []
        self.properties = {}
        self.outputs = {}

        self.label = ""
        self.category = None
        self.has_thumbnail = False

        self.thumbnail = self.CreateEmptyBitmap()
        self.expandicon_bmp = ICON_IMAGE.GetBitmap()
        self.checkerboard_bmp = ICON_BRUSH_CHECKERBOARD.GetBitmap()


    @property
    def NodeGraph(self):
        return self.nodegraph

    @property
    def NodeDatatypes(self):
        return self.nodegraph.node_datatypes

    @property
    def NodeCategories(self):
        return self.nodegraph.node_categories

    @property
    def NodeImageDatatype(self):
        return self.nodegraph.image_datatype

    def Init(self, idname) -> None:
        self.InitSockets()
        self.InitHeaderColor()
        self.InitSize()
        self.InitLabel()
        self.SetIdName(idname)

    def CreateEmptyBitmap(self) -> wx.Bitmap:
        img = wx.Image(120, 120)
        img.SetMaskColour(0,0,0)
        img.InitAlpha()
        return img.ConvertToBitmap()

    def AddSocket(self, label, color, direction) -> None:
        self.ArrangeSockets()

    def HitTest(self, pos: wx.Point, event=None) -> None:
        # Handle expanding the node to show thumbnail hittest
        if self.HasThumbnail() and (event is None or wx.GetMouseState().LeftIsDown()):
            icon_rect = self.expandicon_rect.Inflate(10, 10)
            mouse_rect = wx.Rect(pos[0], pos[1], 2, 2)
            if mouse_rect.Intersects(icon_rect):
                self.ToggleExpand(event)

        # Handle socket hittest
        for socket in self.sockets:
            if socket.HitTest(pos - self.pos):
                return socket

    def EditConnection(self, socket_name, binding_node, binding_socket_name):
        """
        编辑节点连线关系
        :param socket_name: 当前节点的socket名称
        :param binding_node: 连接的源节点（None表示断开连接）
        :param binding_socket_name: 连接的源socket名称
        """
        # 在输出端口对象上存储连线信息，而不是替换整个对象
        if socket_name in self.outputs:
            output_obj = self.outputs[socket_name]
            if binding_node is not None and binding_socket_name is not None:
                # 在Output对象上添加连线信息属性
                output_obj.binding_node = binding_node
                output_obj.binding_socket = binding_socket_name
            else:
                # 断开连接时清除连线信息
                if hasattr(output_obj, 'binding_node'):
                    delattr(output_obj, 'binding_node')
                if hasattr(output_obj, 'binding_socket'):
                    delattr(output_obj, 'binding_socket')
        

    def InitHeaderColor(self) -> None:
        self.header_color = wx.Colour(self.NodeCategories[self.GetCategory()])

    def InitSockets(self) -> None:
        sockets = []
        ins = []
        outs = []

        # Create a list of input and output sockets with the format:
        # [(label, idname, datatype), ...]
        for prop_id in self.properties:
            prop = self.properties[prop_id]
            if prop.exposed and prop.can_be_exposed:
                ins.append((prop.label, prop.idname, prop.datatype))

        if self.IsOutputNode() is not True:
            for output_id in self.outputs:
                output = self.outputs[output_id]
                outs.append((output.label, output.idname, output.datatype))
                # If there is an image datatype then we know there 
                # should be a thumbnail for this node.
                if output.datatype == self.NodeImageDatatype:
                    self.has_thumbnail = True

        x, y, w, h = self.GetRect()
        x, y = self.pos
        w, h = self.size

        for i, p in enumerate(outs + ins):
            socket_type = SOCKET_INPUT  # Socket type IN
            x = 0  # socket margin
            if (p[0], p[1], p[2]) in outs:
                x = w - x - 1
                socket_type = SOCKET_OUTPUT  # Socket type OUT

            # We keep track of where the last socket is placed
            self.lastsocket_pos = 60 + 14 * i

            # 新建槽口
            socket = NodeSocket(label=p[0], idname=p[1], datatype=p[2],
                                node=self, direction=socket_type)
            socket.pos = wx.Point(x, int(45 + (19 * i)))
            socket.SetColor(self.NodeDatatypes[socket.datatype])
            sockets.append(socket)

        self.sockets = sockets

    def InitSize(self) -> None:
        # Calculate the normal size of the node to fit
        # the amount of sockets the node has. The expanded size
        # is calculated to be the normal size plus the image thumbnail size.
        calc_height = self.lastsocket_pos + self.thumbnail.Height + NODE_THUMB_PADDING * 2
        self.expanded_size = wx.Size(NODE_DEFAULT_WIDTH, calc_height)

        self.normal_size = wx.Size(NODE_DEFAULT_WIDTH,
                                   self.lastsocket_pos+(NODE_Y_PADDING*2))

        # Set the initial node size
        if self.IsExpanded():
            self.SetSize(self.expanded_size)
        else:
            self.SetSize(self.normal_size)

    def InitLabel(self):
        # Number of chars to truncate from the label is based on 
        # whether there is a toggle icon taking up space on this node.
        if self.HasThumbnail() == True:
            chars = 15
        else:
            chars = 20
        self.label = TruncateText(self.GetLabel(), chars)

    def HasThumbnail(self) -> bool:
        return self.has_thumbnail

    def IsOutputNode(self) -> bool:
        """ Override method to set whether the node is the output or not. """
        return self.is_output

    def GetLabel(self) -> str:
        """ Get the node label. """
        return self.label

    def GetCategory(self) -> str:
        """ Override method to set the node category. """
        return self.category

    def GetIdname(self) -> str:
        return self.idname

    def SetIdName(self, idname) -> None:
        self.idname = idname

    def GetPosition(self) -> wx.Point:
        return self.pos

    def SetPosition(self, x: int, y: int) -> None:
        self.pos = wx.Point(x, y)

    def GetSize(self) -> wx.Size:
        return (self.size[0], self.size[1])

    def SetSize(self, size: wx.Size) -> None:
        self.size = size

    def GetRect(self) -> wx.Rect:
        return wx.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def IsSelected(self) -> bool:
        return self.selected

    def SetSelected(self, selected=True) -> None:
        self.selected = selected

    def IsActive(self) -> bool:
        return self.active

    def SetActive(self, active=True) -> None:
        self.active = active

    def IsMuted(self) -> bool:
        return self.muted

    def SetMuted(self, muted=True) -> None:
        self.muted = muted
        self.SetExpanded(False)
        self.SetSize(self.normal_size)

    def IsExpanded(self) -> bool:
        return self.expanded

    def SetExpanded(self, expanded=True) -> None:
        self.expanded = expanded

    def ToggleExpand(self, event):
        """
        :param event: 鼠标事件
        """
        # 获取节点图对象（通过节点的 nodegraph 属性）
        if hasattr(self, 'nodegraph') and self.nodegraph:
            nodegraph = self.nodegraph
        else:
            # 如果没有直接引用，尝试通过 socket 获取
            if self.sockets:
                nodegraph = self.sockets[0].node.nodegraph
            else:
                return

        # 显示节点属性编辑对话框并处理后续逻辑
        self.ShowPropertyDialog(nodegraph)

    def ShowPropertyDialog(self, parent_window) -> bool:
        """
        TODO 20260421  更改节点属性
        显示节点属性编辑对话框，并在确认后更新节点及刷新视图
        :param parent_window: 父窗口（通常是节点图）
        :return: 如果用户点击确定返回True，否则返回False
        """
        dialog = NodePropertyDialog(parent_window, self)

        if dialog.ShowModal() == wx.ID_OK:
            updated_values = dialog.GetUpdatedValues()

            # 保存旧的属性名称映射（用于更新连线）
            old_property_labels = {}
            for prop_id, prop in self.properties.items():
                old_property_labels[prop_id] = prop.label

            # 更新节点标签
            self.label = updated_values['label']

            # 更新属性名称
            for prop_id, new_label in updated_values['property_labels'].items():
                if prop_id in self.properties:
                    prop = self.properties[prop_id]
                    # 如果属性名称发生变化，需要更新相关连线
                    if new_label and new_label != prop.label:
                        old_label = prop.label
                        prop.label = new_label

                        # 重要：如果有连线使用此socket，需要通知节点图更新
                        self._update_socket_connections(old_label, new_label, parent_window)

            # 更新属性值
            for prop_id, new_value in updated_values['properties'].items():
                if prop_id in self.properties:
                    prop = self.properties[prop_id]
                    try:
                        if hasattr(prop, 'datatype'):
                            if prop.datatype == "INTEGER":
                                converted_value = int(new_value)
                            elif prop.datatype == "FLOAT":
                                converted_value = float(new_value)
                            elif prop.datatype == "BOOLEAN":
                                converted_value = bool(new_value)
                            else:
                                converted_value = str(new_value)
                        else:
                            converted_value = new_value

                        if hasattr(prop, 'SetValue'):
                            prop.SetValue(converted_value)
                        else:
                            prop.value = converted_value
                    except Exception as e:
                        print(f"✗ 属性 {prop_id} 值更新失败: {e}")

            # 重要：因为属性名称可能改变，需要重新初始化 Sockets 和大小
            self.InitSockets()
            self.InitSize()  # 重新计算节点大小

            # 刷新节点图
            if parent_window:
                parent_window.UpdateNodeGraph()
                # 发送节点选择事件以更新属性面板
                parent_window.SendNodeSelectEvent()

            dialog.Destroy()
            return True

        dialog.Destroy()
        return False

    def _update_socket_connections(self, old_socket_name, new_socket_name, nodegraph):
        """
        当socket名称改变时，更新相关的连线信息
        :param old_socket_name: 旧的socket名称
        :param new_socket_name: 新的socket名称
        :param nodegraph: 节点图对象
        """
        if not nodegraph or not hasattr(nodegraph, 'wires'):
            return

        # 遍历所有连线，查找使用旧socket名称的连线并更新
        for wire in nodegraph.wires:
            # 检查源socket是否是需要更新的
            if hasattr(wire, 'srcsocket') and wire.srcsocket:
                if wire.srcsocket.node == self and wire.srcsocket.idname == old_socket_name:
                    wire.srcsocket.idname = new_socket_name
                    wire.srcsocket.label = new_socket_name

            
            # 检查目标socket是否是需要更新的
            if hasattr(wire, 'dstsocket') and wire.dstsocket:
                if wire.dstsocket.node == self and wire.dstsocket.idname == old_socket_name:
                    wire.dstsocket.idname = new_socket_name
                    wire.dstsocket.label = new_socket_name

        
        # 加长图框
        # if self.HasThumbnail():
        #     if self.IsExpanded() is True:
        #         self.SetExpanded(False)
        #         self.SetSize(self.normal_size)
        #     elif self.IsExpanded() is False:
        #         self.SetExpanded(True)
        #         self.SetSize(self.expanded_size)

    def GetSockets(self) -> list:
        return self.sockets

    def SetThumbnail(self, thumb) -> None:
        if self.HasThumbnail():
            self.thumbnail = thumb
            self.UpdateExpandSize()

    def UpdateExpandSize(self) -> None:
        calc_height = self.lastsocket_pos + self.thumbnail.Height + NODE_THUMB_PADDING * 2
        self.expanded_size = wx.Size(NODE_DEFAULT_WIDTH, calc_height)
        self.SetSize(self.expanded_size)

    def FindSocket(self, idname):
        """ Return the node socket with the given name.
        :param idname: the socket idname as a string
        :returns: Socket object
        """
        for socket in self.GetSockets():
            if socket.idname == idname:
                return socket

    def Draw(self, dc) -> None:
        # 绘制图框
        x, y = self.GetPosition()
        w, h = self.GetSize()

        # Node body and border
        if self.IsSelected() or self.IsActive():
            border_color = NODE_BORDER_SELECTED_COLOR
        else:
            border_color = NODE_BORDER_NORMAL_COLOR
        if self.IsMuted():
            node_color = NODE_MUTED_COLOR
        else:
            node_color = NODE_NORMAL_COLOR
        dc.SetPen(wx.Pen(wx.Colour(border_color), 3))
        dc.SetBrush(wx.Brush(wx.Colour(node_color)))
        dc.DrawRoundedRectangle(x, y, w, h, 3)

        # Node header
        dc.SetPen(wx.Pen(wx.TRANSPARENT_PEN))
        if self.IsMuted():
            header_color = wx.Colour(NODE_HEADER_MUTED_COLOR)
            bottom_color = wx.Colour(NODE_HEADER_MUTED_COLOR).ChangeLightness(80)
        else:
            header_color = wx.Colour(self.header_color).ChangeLightness(70)
            bottom_color = wx.Colour(self.header_color).ChangeLightness(55)
        dc.SetBrush(wx.Brush(header_color))
        dc.DrawRoundedRectangle(x+1, y+1, w-2, 25, 3)

        # Bottom border of the node header (to cover up the rounded bottom)
        dc.SetBrush(wx.Brush(bottom_color))
        dc.DrawRectangle(x+1, y+24, w-2, 2)

        # Node name label
        if self.IsMuted():
            color = wx.Colour('#fff').ChangeLightness(60)
        else:
            color = wx.Colour('#fff').ChangeLightness(85)
        dc.SetTextForeground(color)
        dc.DrawText(self.GetLabel(), x+10, y+1)

        # Node sockets
        [socket.Draw(dc) for socket in self.sockets]

        # Expand node thumbnail icon

        if self.HasThumbnail() == True and self.IsMuted() != True:
            self.expandicon_rect = wx.Rect(x+NODE_DEFAULT_WIDTH-28, y+5, 16, 16)
            dc.DrawBitmap(self.expandicon_bmp, self.expandicon_rect[0],
                        self.expandicon_rect[1], True)
        #
        # # Thumbnail
        # if self.IsExpanded() and self.HasThumbnail():
        #     # 我需要从此处修改为弹出结果查看，调用了两次
        #
        #     print("结果输出框")
        #     thumb_rect = wx.Rect(int(x+NODE_THUMB_PADDING/2),
        #                          int(y+self.lastsocket_pos+(NODE_Y_PADDING*2)),
        #                          NODE_DEFAULT_WIDTH-NODE_THUMB_PADDING,
        #                          self.thumbnail.Height)
        #
        #     # Draw thumbnail border and background
        #     dc.SetPen(wx.Pen(wx.Colour(NODE_THUMB_BORDER_COLOR), 1))
        #     dc.SetBrush(wx.Brush(self.checkerboard_bmp))
        #     dc.DrawRectangle(thumb_rect)
        #
        #     # Draw the thumbnail
        #     dc.DrawBitmap(self.thumbnail, thumb_rect[0], thumb_rect[1], True)
