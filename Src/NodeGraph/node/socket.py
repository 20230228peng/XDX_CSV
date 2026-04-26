
import math
import wx

from ..constants import (SOCKET_BORDER_COLOR, SOCKET_INPUT, SOCKET_HIT_RADIUS, 
                         SOCKET_RADIUS, SOCKET_BORDER_COLOR)


class NodeSocket(object):
    """

    Node socket showing the datatypes and flow of the node relative to
    the graph. Wires are dropped into the socket to connect nodes.

    """
    def __init__(self, label, idname, datatype, node, direction):
        """
        槽口属性详情
        :param label: 名称(外显)
        :param idname: 槽口名称（隐藏）
        :param datatype: 属性 （未使用）
        :param node: 坐标
        :param direction: 方位

        """
        self.label = label
        self.idname = idname
        self.node = node
        self.direction = direction
        self.datatype = datatype

        self.wires = []
        self.pos = wx.Point(0, 0)
        self.color = wx.Colour("#fff")
        self.tdc = wx.WindowDC(wx.GetApp().GetTopWindow())


        #self.SetColorByDataType(self.datatype)

    def GetWires(self) -> list:
        """ Get the wires for this socket. """
        return self.wires

    def SetColor(self, color) -> None:
        """ Set the socket base color based on the datatype. """
        self.color = wx.Colour(color)  

    def CurrentSocketPos(self) -> wx.Point:
        """ Return the current coords of the node socket. """
        return self.pos + self.node.pos
      
    def HitTest(self, pos) -> bool:
        """ Returns True if the node socket was hit. """
        pnt = pos - self.pos
        distance = math.sqrt(math.pow(pnt.x, 2) + math.pow(pnt.y, 2))

        # Socket hit radius
        if math.fabs(distance) < SOCKET_HIT_RADIUS:
            return True

    def Draw(self, dc) -> None:
        """
        绘制槽口
        """
        pos = self.CurrentSocketPos()
        w, h = self.tdc.GetTextExtent(self.label)

        # Set the socket color
        dc.SetPen(wx.Pen(wx.Colour(SOCKET_BORDER_COLOR), 1))
        dc.SetBrush(wx.Brush(self.color))

        # Draw the socket
        dc.DrawCircle(pos.x, pos.y, SOCKET_RADIUS)

        # Socket label margin
        if self.direction == SOCKET_INPUT:
            x = int(pos.x + 12)
        else:
            x = int(pos.x - w - 12)

        # Draw the label
        dc.DrawText(self.label, x, int(pos.y - h / 2))
