"""
修复日志编码问题的测试脚本
"""
import os
import sys
import logging
from utils.logger import setup_logger

# 测试日志编码
logger = setup_logger('test_encoding')
logger.info("测试中文日志，看看是否正常显示")
logger.info("这是一条包含中文的测试日志")

# 检查文件编码
log_file = 'logs/test_encoding.log'
if os.path.exists(log_file):
    # 尝试以不同编码读取文件
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
    
    print(f"\n检查日志文件 {log_file} 的编码:")
    for enc in encodings:
        try:
            with open(log_file, 'r', encoding=enc) as f:
                content = f.read()
            print(f"  ✅ 可以用 {enc} 编码读取")
            print(f"  内容预览: {content[-100:]}")
        except Exception as e:
            print(f"  ❌ 无法用 {enc} 编码读取: {e}")
