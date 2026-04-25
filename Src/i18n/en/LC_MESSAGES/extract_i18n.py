#!/usr/bin/env python3
# extract_i18n_custom.py

import os
import ast
import sys
from pathlib import Path

# ========== 配置区域 ==========
SOURCE_DIR = "../../../../UI/"          # 要扫描的源代码目录
OUTPUT_POT = "./en.po"                  # 输出的 .po 文件路径
DOMAIN = "en"                            # 翻译域名
ENCODING = "utf-8"                          # 源文件编码
FUNC_NAMES = {"_"}                          # 需要提取的翻译函数名
EXCLUDE_DIRS = {"__pycache__", ".git", "venv", "env", "dist", "build"}  # 排除目录
# =================================

def extract_strings_from_file(file_path, func_names):
    """使用 AST 从单个文件中提取所有 func_names 调用中的字符串。
       返回列表，元素为 (msgid, lineno, file_path)"""
    results = []
    try:
        with open(file_path, 'r', encoding=ENCODING) as f:
            source = f.read()
        tree = ast.parse(source, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"跳过文件 {file_path}: {e}", file=sys.stderr)
        return results

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in func_names:
            # 支持 Python 3.7 的 ast.Str 和 3.8+ 的 ast.Constant
            arg = node.args[0] if node.args else None
            if arg and isinstance(arg, ast.Str):
                msgid = arg.s
                lineno = node.lineno
                results.append((msgid, lineno, str(file_path)))
            elif arg and isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                msgid = arg.value
                lineno = node.lineno
                results.append((msgid, lineno, str(file_path)))
    return results

def generate_pot(extracted, output_file, domain, source_root):
    """根据提取结果生成 .pot 文件，位置注释使用相对于 source_root 的路径"""
    from datetime import datetime

    # 去重并保留第一次出现的位置
    unique = {}
    for msgid, lineno, filepath in extracted:
        if msgid not in unique:
            unique[msgid] = (lineno, filepath)

    # 准备写入
    with open(output_file, 'w', encoding='utf-8') as pot:
        # 头部信息
        pot.write('# SOME DESCRIPTIVE TITLE.\n')
        pot.write('# Copyright (C) YEAR ORGANIZATION\n')
        pot.write('# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.\n')
        pot.write('#\n')
        pot.write('msgid ""\n')
        pot.write('msgstr ""\n')
        pot.write(f'"Project-Id-Version: {domain} 1.0\\n"\n')
        pot.write(f'"POT-Creation-Date: {datetime.now().strftime("%Y-%m-%d %H:%M%z")}\\n"\n')
        pot.write('"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n')
        pot.write('"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n')
        pot.write('"Language-Team: LANGUAGE <LL@li.org>\\n"\n')
        pot.write('"MIME-Version: 1.0\\n"\n')
        pot.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
        pot.write('"Content-Transfer-Encoding: 8bit\\n"\n')
        pot.write('"Generated-By: custom_py_extractor\\n"\n')
        pot.write('\n')

        # 写入每个条目
        for msgid, (lineno, filepath) in sorted(unique.items()):
            # 计算相对路径：相对于 source_root 的路径，并添加 source_root 的目录名作为前缀
            abs_path = Path(filepath).resolve()
            rel_path = abs_path.relative_to(source_root)          # 例: Calculate\gsnodegraph\graph\base.py
            display_path = Path(source_root.name) / rel_path      # 例: Public\Calculate\...
            # 转换为反斜杠字符串（Windows 风格）
            display_path_str = str(display_path).replace('/', '\\')
            pot.write(f'#: {display_path_str}:{lineno}\n')
            pot.write(f'msgid "{escape(msgid)}"\n')
            pot.write('msgstr ""\n')
            pot.write('\n')

def escape(s):
    """转义字符串中的双引号和反斜杠，符合 gettext 格式"""
    return s.replace('\\', '\\\\').replace('"', '\\"')

def scan_directory(root_dir, func_names):
    """扫描目录，返回所有提取的字符串信息"""
    root_path = Path(root_dir).resolve()
    all_extracted = []
    py_files = []

    for path in root_path.rglob("*.py"):
        # 检查是否在排除目录中（精确匹配部件）
        if any(excluded in path.parts for excluded in EXCLUDE_DIRS):
            continue
        py_files.append(path)

    print(f"发现 {len(py_files)} 个 Python 文件")
    for py_file in py_files:
        results = extract_strings_from_file(py_file, func_names)
        if results:
            all_extracted.extend(results)
            print(f"  {py_file} : {len(results)} 个字符串")
        else:
            print(f"  {py_file} : 无匹配")

    return all_extracted

if __name__ == "__main__":
    # 检查源目录是否存在
    if not os.path.isdir(SOURCE_DIR):
        print(f"错误：源目录不存在 - {SOURCE_DIR}", file=sys.stderr)
        sys.exit(1)

    # 确保输出目录存在
    output_dir = os.path.dirname(OUTPUT_POT)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 计算 source_root 的绝对路径（用于后续相对路径计算）
    source_abs = Path(SOURCE_DIR).resolve()
    print(f"源目录绝对路径: {source_abs}")

    print(f"开始扫描 {SOURCE_DIR} ...")
    extracted = scan_directory(SOURCE_DIR, FUNC_NAMES)
    if not extracted:
        print("未找到任何需要翻译的字符串。")
        sys.exit(0)

    generate_pot(extracted, OUTPUT_POT, DOMAIN, source_abs)
    unique_count = len({msgid for msgid, _, _ in extracted})
    print(f"✅ 已生成 {OUTPUT_POT}，共包含 {unique_count} 个唯一字符串。")
    print("完成。")