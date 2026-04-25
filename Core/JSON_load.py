import json
import wx

# 加载快捷键
def load_accelerator_config(config_path):
    """
    通过外部JSON文件
    加载外部快捷键设置
    :param config_path:加载目录
    :return:
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"快捷键配置文件 {config_path} 未找到")
    except json.JSONDecodeError:
        raise RuntimeError(f"配置文件 {config_path} 格式错误")

    accelerator_entries = []
    modifier_flags = {
        "ctrl": wx.ACCEL_CTRL,
        "alt": wx.ACCEL_ALT,
        "shift": wx.ACCEL_SHIFT
    }

    for accel in config.get("accelerators", []):
        # 解析修饰键
        flags = 0
        for modifier in accel.get("modifiers", []):
            flags |= modifier_flags.get(modifier.lower(), 0)

        # 解析键值
        key_str = accel["key"]
        # key_code = None

        # 尝试解析为特殊功能键 (WXK_*)
        if hasattr(wx, f"WXK_{key_str.upper()}"):
            key_code = getattr(wx, f"WXK_{key_str.upper()}")
        # 尝试解析为字符键
        elif len(key_str) == 1:
            key_code = ord(key_str.upper())
        else:
            raise ValueError(f"无效的键值: {key_str}")

        accelerator_entries.append(
            (flags, key_code, accel["id"])
        )

    return accelerator_entries