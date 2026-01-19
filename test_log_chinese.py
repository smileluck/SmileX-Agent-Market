"""
测试日志中文显示是否正常
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logger

# 测试日志
def test_log_chinese():
    """
    测试中文日志是否能正常显示
    """
    logger = setup_logger('test_chinese')
    
    # 输出各种中文日志
    logger.info("测试中文日志信息")
    logger.debug("测试中文调试信息")
    logger.warning("测试中文警告信息")
    logger.error("测试中文错误信息")
    
    # 包含特殊字符的中文
    logger.info("测试中文日志：包含特殊字符！@#$%^&*()_+")
    logger.info("测试中文日志：包含中文标点符号，。！？；：")
    
    print("测试完成，日志已写入 logs/test_chinese.log")
    print("请查看日志文件，确认中文是否正常显示")

if __name__ == "__main__":
    test_log_chinese()
