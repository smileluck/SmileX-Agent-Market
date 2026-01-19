"""
日志工具模块
"""
import logging
import os
from config.settings import LOG_DIR, LOG_LEVEL, LOG_FORMAT


def setup_logger(name: str) -> logging.Logger:
    """
    初始化并返回一个logger实例
    
    Args:
        name (str): logger名称
    
    Returns:
        logging.Logger: 配置好的logger实例
    """
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    # 关闭logger的传播，避免日志被重复处理
    logger.propagate = False
    
    # 检查是否已经有控制台handler和文件handler
    has_console_handler = any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers)
    has_file_handler = any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)
    
    # 创建控制台handler，确保控制台输出也能正确显示中文
    if not has_console_handler:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        formatter = logging.Formatter(LOG_FORMAT)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    # 创建文件handler，确保使用UTF-8编码
    if not has_file_handler:
        log_file = os.path.join(LOG_DIR, f"{name}.log")
        # 使用utf-8-sig编码，解决Windows下UTF-8文件的BOM问题
        file_handler = logging.FileHandler(log_file, encoding='utf-8-sig')
        file_handler.setLevel(LOG_LEVEL)
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
