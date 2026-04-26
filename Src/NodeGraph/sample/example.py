
from Src.NodeGraph import NodeBase

# ---------- 1. 定义辅助类 ----------
class Output(object):
    """
    输出端口定义
    """

    def __init__(self, idname, datatype, label, visible=True):
        self.idname = idname
        self.datatype = datatype
        self.label = label
        self.visible = visible

class Input(object):
    """
    输入基类 (用作输入端口)
    """

    def __init__(self, idname, default=None, label="Input", exposed=True,
                 can_be_exposed=True, visible=True):
        self.idname = idname
        self.label = label
        self.default = default
        self.exposed = exposed
        self.can_be_exposed = can_be_exposed
        self.visible = visible
        self.binding = None
        self.datatype = "DEFAULT"
        self.value = default

    def GetValue(self):
        return self.value

    def SetValue(self, value):
        self.value = value

# ---------- 2. 定义自定义节点 ----------
class InputNode(NodeBase):
    """
    输入节点 - 只有输出端口
    """

    def __init__(self, nodegraph, _id):
        NodeBase.__init__(self, nodegraph, _id)

        self.label = "输入节点"
        self.category = "INPUT"

        # 定义输出端口
        self.outputs = {
            "output_1": Output(idname="inBase", datatype="DEFAULT", label="基准（10）"),
            "output_2": Output(idname="inMalfunction", datatype="DEFAULT", label="故障（50）")
        }

        # 定义节点属性（此处为空表示无输入）
        self.properties = {}

class RMSNode(NodeBase):
    """
    幅值节点 - 有输入属性和输出端口
    """

    def __init__(self, nodegraph, _id):
        NodeBase.__init__(self, nodegraph, _id)

        self.label = "幅值节点"
        self.category = "RMS"

        # 定义输出端口
        self.outputs = {
            "output_3": Output(idname="RMSCondition", datatype="DEFAULT", label="条件判别"),
            "output_4": Output(idname="RMSOutput", datatype="DEFAULT", label="输出复用")
        }

        # 定义输入属性（这些会显示为输入端口）（左侧）
        self.properties = {
            "input_1": Input("RMSInputID1", label="计算ID1"),
            "input_2": Input("RMSInputID2", label="计算ID2")
        }

class ActiveNode(NodeBase):
    """
    有功节点 - 有输入属性和输出端口
    """

    def __init__(self, nodegraph, _id):
        NodeBase.__init__(self, nodegraph, _id)

        self.label = "有功节点"
        self.category = "ACTIVE"

        # 定义输出端口
        self.outputs = {
            "output_5": Output(idname="output1", datatype="DEFAULT", label="条件判别"),
            "output_6": Output(idname="output2", datatype="DEFAULT", label="输出复用")
        }

        # 定义输入属性（这些会显示为输入端口）（左侧）
        self.properties = {
            "input_3": Input("input_socketid", label="计算ID1"),
            "input_4": Input("input_socketid1", label="计算ID2")
        }

class IdleNode(NodeBase):
    """
    无功节点 - 有输入属性和输出端口
    """

    def __init__(self, nodegraph, _id):
        NodeBase.__init__(self, nodegraph, _id)

        self.label = "无功节点"
        self.category = "IDLE"

        # 定义输出端口
        self.outputs = {
            "output_7": Output(idname="output1", datatype="DEFAULT", label="条件判别"),
            "output_8": Output(idname="output2", datatype="DEFAULT", label="输出复用")
        }

        # 定义输入属性（这些会显示为输入端口）（左侧）
        self.properties = {
            "input_5": Input("input_socketid", label="计算ID"),
            "input_6": Input("input_socketid1", label="复用输入")
        }


class ConditionalNode(NodeBase):
    """
    条件判别节点 - 有输入属性和输出端口
    """

    def __init__(self, nodegraph, _id):
        NodeBase.__init__(self, nodegraph, _id)

        self.label = "条件判别节点"
        self.category = "UNDEFINED"

        # 定义输出端口
        self.outputs = {
            "output_11": Output(idname="output1", datatype="DEFAULT", label="大于"),
            "output_12": Output(idname="output2", datatype="DEFAULT", label="小于"),
            "output_13": Output(idname="output2", datatype="DEFAULT", label="等于")
        }

        # 定义输入属性（这些会显示为输入端口）（左侧）
        self.properties = {
            "input_9": Input("input_socketid", label="0.5"),
            "input_10": Input("input_socketid1", label="120")
        }

class OutputNode(NodeBase):
    """
    输出节点 - 只有输入属性
    """

    def __init__(self, nodegraph, _id):
        NodeBase.__init__(self, nodegraph, _id)

        self.label = "输出节点"
        self.category = "OUTPUT"
        self.is_output = True  # 标记为输出节点

        # 没有输出端口
        self.outputs = {}

        # 定义输入属性
        self.properties = {
            "input_11": Input("执行计算", label="结果（双击计算）")
        }