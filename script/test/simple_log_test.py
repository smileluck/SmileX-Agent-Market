import logging
import os

# 创建logs目录
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# 配置日志
logging.basicConfig(
    filename=os.path.join(log_dir, 'test_encoding.log'),
    encoding='utf-8-sig',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 写入中文日志
logging.info('测试中文日志信息')
logging.info('这是一条包含中文的测试日志')
logging.info('测试中文标点符号：，。！？；：')
logging.info('测试特殊字符：@#$%^&*()_+')

print('日志写入完成，文件路径：logs/test_encoding.log')