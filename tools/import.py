#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析脚本（简化版） - 不依赖pandas
提取公众号名称并将其他列用|连接
使用方法: python analyze_data_simple.py
输出: data/processed_output.txt
"""

import os
import sys


def process_text_file(file_path: str) -> list:
    """处理制表符分隔的文本文件"""
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                # 按制表符分割
                parts = line.split('\t')
                
                # 确保至少有两列（序号和公众号名称）
                if len(parts) >= 2:
                    # 第二列是公众号名称（索引1）
                    public_name = parts[1].strip()
                    # 后面的列用|连接
                    other_columns = [p.strip() for p in parts[2:] if p.strip()]
                    
                    if public_name:
                        if other_columns:
                            result = f"{public_name}|{'|'.join(other_columns)}"
                        else:
                            result = public_name
                        results.append(result)
                else:
                    print(f"警告: 第{line_num}行数据格式不正确，跳过")
        
        return results
    except Exception as e:
        print(f"读取文件失败 {file_path}: {e}")
        return []


def import_mps(data_file:str="data/data.txt"):
    if not os.path.exists(data_file):
        print(f"错误: 未找到数据文件: {data_file}")
        print("请确保data目录下存在data.txt文件")
        sys.exit(1)
    
    print(f"正在处理文件: data.txt")
    print("=" * 50)
    
    # 处理数据
    results = process_text_file(data_file)
    
    if results:
        print(f"\n处理成功，共 {len(results)} 条记录")
        print("\n前10条结果:")
        for i, result in enumerate(results[:10], 1):
            print(f"{i}. {result}")
        
        if len(results) > 10:
            print(f"... 还有 {len(results) - 10} 条记录未显示")
        
    else:
        print("未生成任何结果")


if __name__ == '__main__':
    import_mps()
