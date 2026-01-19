"""
测试知乎搜索功能
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.zhihu.zhihu_crawler import ZhihuCrawler
from data.storage import data_storage
from utils.logger import setup_logger

logger = setup_logger(__name__)


def test_search_functionality():
    """
    测试知乎搜索功能
    
    Returns:
        bool: 测试是否成功
    """
    logger.info("=== 开始测试知乎搜索功能 ===")
    
    try:
        # 初始化爬虫
        crawler = ZhihuCrawler()
        logger.info("爬虫初始化成功")
        
        # 测试搜索功能
        query = "英语学习"
        max_pages = 2
        limit = 10
        
        logger.info(f"开始搜索，关键词: {query}，最大页数: {max_pages}，每页限制: {limit}")
        
        # 执行搜索
        search_results = crawler.search_content(
            query=query,
            max_pages=max_pages,
            limit=limit
        )
        
        if not search_results:
            logger.warning("未获取到搜索结果")
            return False
        
        logger.info(f"搜索完成，共获取 {len(search_results)} 条结果")
        
        # 打印前3条结果
        for i, result in enumerate(search_results[:3], 1):
            logger.info(f"\n=== 结果 {i} ===")
            logger.info(f"标题: {result.get('title', 'N/A')}")
            logger.info(f"作者: {result.get('author', 'N/A')}")
            logger.info(f"点赞数: {result.get('vote_up_count', 0)}")
            logger.info(f"评论数: {result.get('comment_count', 0)}")
            logger.info(f"回答链接: {result.get('url', 'N/A')}")
            logger.info(f"问题链接: {result.get('question_url', 'N/A')}")
            logger.info(f"内容预览: {result.get('content', 'N/A')[:100]}...")
        
        # 保存搜索结果到数据库
        logger.info("\n开始保存搜索结果到数据库...")
        
        # 1. 保存搜索任务
        search_task_id = data_storage.save_search_task(
            keyword=query,
            page_count=max_pages,
            total_results=len(search_results)
        )
        
        if not search_task_id:
            logger.error("保存搜索任务失败")
            return False
        
        # 2. 保存搜索结果，关联搜索任务ID
        saved_count = data_storage.save_zhihu_answers(search_results, search_task_id)
        logger.info(f"成功保存 {saved_count} 条搜索结果到数据库，关联搜索任务ID: {search_task_id}")
        
        # 关闭爬虫
        crawler.close()
        
        logger.info("=== 测试完成 ===")
        return True
        
    except Exception as e:
        logger.error(f"测试失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_search_functionality()
    
    if success:
        print("\n✅ 搜索功能测试成功！")
        sys.exit(0)
    else:
        print("\n❌ 搜索功能测试失败！")
        sys.exit(1)
