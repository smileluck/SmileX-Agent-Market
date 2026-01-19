"""
简单测试日志输出
"""
import logging

# 直接配置根日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 控制台输出
        logging.FileHandler('simple_test.log', encoding='utf-8')  # 文件输出
    ]
)

logger = logging.getLogger("simple_test")

print("=== 开始测试简单日志功能 ===")
print(f"logger名称: {logger.name}")
print(f"logger级别: {logger.level}")
print(f"logger处理器数量: {len(logger.handlers)}")

# 测试不同级别的日志输出
logger.debug("这是一条DEBUG级别的日志")
logger.info("这是一条INFO级别的日志")
logger.warning("这是一条WARNING级别的日志")
logger.error("这是一条ERROR级别的日志")
logger.critical("这是一条CRITICAL级别的日志")

print("\n=== 测试完成 ===")
