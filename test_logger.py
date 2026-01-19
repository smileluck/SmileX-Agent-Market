"""
测试日志功能
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import setup_logger

# 测试日志功能
logger = setup_logger("test_logger")

print("=== 开始测试日志功能 ===")
print(f"logger名称: {logger.name}")
print(f"logger级别: {logger.level}")
print(f"logger处理器数量: {len(logger.handlers)}")

for i, handler in enumerate(logger.handlers):
    print(f"\n处理器 {i+1}:")
    print(f"  类型: {type(handler).__name__}")
    print(f"  级别: {handler.level}")
    if hasattr(handler, 'baseFilename'):
        print(f"  文件路径: {handler.baseFilename}")

# 测试不同级别的日志输出
logger.debug("这是一条DEBUG级别的日志")
logger.info("这是一条INFO级别的日志")
logger.warning("这是一条WARNING级别的日志")
logger.error("这是一条ERROR级别的日志")
logger.critical("这是一条CRITICAL级别的日志")

print("\n=== 测试完成 ===")
