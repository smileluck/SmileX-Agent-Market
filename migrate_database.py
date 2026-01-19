"""
数据库迁移脚本，用于更新表结构
"""
import sqlite3
import os
from config.settings import DATABASE_URL
from utils.logger import setup_logger

logger = setup_logger(__name__)


def migrate_database():
    """
    执行数据库迁移，添加缺失的列
    """
    # 从DATABASE_URL中提取数据库文件路径
    db_path = DATABASE_URL.replace('sqlite:///', '')
    
    if not os.path.exists(db_path):
        logger.error(f"数据库文件不存在: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查zhihu_answers表的列
        cursor.execute("PRAGMA table_info(zhihu_answers)")
        columns = [column[1] for column in cursor.fetchall()]
        logger.info(f"zhihu_answers表当前列: {columns}")
        
        # 需要添加的列及其定义
        columns_to_add = {
            'create_time': 'DATETIME',
            'title_raw': 'TEXT',
            'content_raw': 'TEXT',
            'excerpt_raw': 'TEXT',
            'metrics_raw': 'TEXT',
            'rank_raw': 'TEXT'
        }
        
        # 添加缺失的列
        for column_name, column_type in columns_to_add.items():
            if column_name not in columns:
                try:
                    alter_sql = f"ALTER TABLE zhihu_answers ADD COLUMN {column_name} {column_type}"
                    cursor.execute(alter_sql)
                    logger.info(f"成功添加列: {column_name}")
                except Exception as e:
                    logger.warning(f"添加列 {column_name} 失败: {str(e)}")
            else:
                logger.info(f"列 {column_name} 已存在，跳过")
        
        # 检查zhihu_questions表的列
        cursor.execute("PRAGMA table_info(zhihu_questions)")
        columns = [column[1] for column in cursor.fetchall()]
        logger.info(f"zhihu_questions表当前列: {columns}")
        
        # zhihu_questions表需要添加的列
        columns_to_add_questions = {
            'title_raw': 'TEXT',
            'excerpt_raw': 'TEXT',
            'metrics_raw': 'TEXT',
            'rank_raw': 'TEXT'
        }
        
        # 添加缺失的列
        for column_name, column_type in columns_to_add_questions.items():
            if column_name not in columns:
                try:
                    alter_sql = f"ALTER TABLE zhihu_questions ADD COLUMN {column_name} {column_type}"
                    cursor.execute(alter_sql)
                    logger.info(f"成功添加列: {column_name}")
                except Exception as e:
                    logger.warning(f"添加列 {column_name} 失败: {str(e)}")
            else:
                logger.info(f"列 {column_name} 已存在，跳过")
        
        conn.commit()
        conn.close()
        
        logger.info("数据库迁移完成")
        return True
        
    except Exception as e:
        logger.error(f"数据库迁移失败: {str(e)}")
        return False


if __name__ == "__main__":
    migrate_database()
