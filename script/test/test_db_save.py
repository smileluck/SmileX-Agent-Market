"""
测试数据库保存功能
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.storage import data_storage
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)


def test_save_answers():
    """
    测试保存知乎回答功能
    
    Returns:
        bool: 测试是否成功
    """
    logger.info("=== 开始测试数据库保存功能 ===")
    
    try:
        # 创建测试数据
        test_answers = [
            {
                'url': 'https://www.zhihu.com/answer/123456789',
                'question_url': 'https://www.zhihu.com/question/987654321',
                'question_id': '987654321',
                'title': '测试回答标题1',
                'author': '测试作者1',
                'content': '这是测试回答的内容1',
                'vote_up_count': 100,
                'comment_count': 50,
                'crawl_time': datetime.now()
            },
            {
                'url': 'https://www.zhihu.com/answer/987654321',
                'question_url': 'https://www.zhihu.com/question/123456789',
                'question_id': '123456789',
                'title': '测试回答标题2',
                'author': '测试作者2',
                'content': '这是测试回答的内容2',
                'vote_up_count': 200,
                'comment_count': 80,
                'crawl_time': '2026-01-19 12:00:00'  # 测试字符串格式
            }
        ]
        
        logger.info(f"准备保存 {len(test_answers)} 条测试数据")
        
        # 保存测试数据
        saved_count = data_storage.save_zhihu_answers(test_answers)
        
        logger.info(f"成功保存 {saved_count} 条数据")
        
        if saved_count == len(test_answers):
            logger.info("✅ 数据库保存功能测试通过")
            return True
        else:
            logger.warning(f"⚠️ 期望保存 {len(test_answers)} 条，实际保存 {saved_count} 条")
            return False
            
    except Exception as e:
        logger.error(f"❌ 数据库保存功能测试失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_save_answers()
    
    if success:
        print("\n✅ 测试成功！")
        sys.exit(0)
    else:
        print("\n❌ 测试失败！")
        sys.exit(1)
