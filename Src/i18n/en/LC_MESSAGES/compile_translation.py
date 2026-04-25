"""
编译 gsnodegraph 翻译文件的脚本
将 .po 文件编译为 .mo 文件
"""
import os
import sys

def compile_translation():
    """编译翻译文件"""
    # 设置路径 - 修正：脚本已在 LC_MESSAGES 目录下
    base_dir = os.path.dirname(os.path.abspath(__file__))

    parent_dir = os.path.dirname(base_dir)  # 获取父目录
    po_file = os.path.join(base_dir, 'en.po')
    mo_file = os.path.join(base_dir, 'en.mo')  # 父目录下的 en.mo

    
    # 检查源文件是否存在
    if not os.path.exists(po_file):
        print(f"错误: 找不到源文件 {po_file}")
        return False


    try:
        import polib
        po = polib.pofile(po_file)
        po.save_as_mofile(mo_file)
        print("✓ 翻译文件编译成功 (使用 polib)")
        print(f"  生成文件: {mo_file}")
        return True
    except ImportError:
        print("✗ 未安装 polib 库")
        print("  请运行: pip install polib")
        return False
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        return False

if __name__ == '__main__':
    success = compile_translation()
    sys.exit(0 if success else 1)