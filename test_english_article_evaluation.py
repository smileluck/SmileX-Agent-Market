#!/usr/bin/env python3
"""
测试英语学习文章评估功能
"""
from utils.logger import setup_logger
from agent.evaluator import ContentEvaluator

logger = setup_logger(__name__)

def test_english_article_evaluation():
    """
    测试英语学习文章评估功能
    """
    logger.info("开始测试英语学习文章评估功能...")
    
    try:
        # 初始化评估器
        evaluator = ContentEvaluator()
        logger.info("✓ ContentEvaluator初始化成功")
        
        # 测试数据
        test_title = "《每天10分钟看新闻，零基础也能轻松学英语》"
        test_content = "很多人说学英语难，其实是没找对方法。我不建议零基础的朋友一上来就背单词、刷语法，不如每天花10分钟看中文新闻，遇到高频词就自己试着翻译成英文……这样在日常阅读中积累，比死记硬背有效多了。评论区很多人说\"没时间专门学，这样的碎片化方式太适合了\"。"
        
        # 调用评估方法
        result = evaluator.evaluate_english_article(test_title, test_content)
        logger.info("✓ evaluate_english_article方法调用成功")
        
        # 打印评估结果
        logger.info("\n=== 英语学习文章评估结果 ===")
        logger.info(f"文章标题: {result['title']}")
        logger.info(f"目标人群相关性: {result['target_audience_score']}")
        logger.info(f"产品定位相关性: {result['product_relevance_score']}")
        logger.info(f"学习建议与经历分享: {result['learning_advice_score']}")
        logger.info(f"总分: {result['total_score']}")
        logger.info(f"分级: {result['grade']}")
        logger.info(f"核心相关点/不相关点分析: {result['match_analysis']}")
        logger.info(f"核心用户痛点: {result['core_pain_points']}")
        
        return True
    except Exception as e:
        logger.error(f"✗ 英语学习文章评估测试失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("=== 英语学习文章评估功能测试 ===")
    
    # 运行测试
    test_result = test_english_article_evaluation()
    
    logger.info("\n=== 测试结果汇总 ===")
    if test_result:
        logger.info("✅ 英语学习文章评估功能测试通过！")
        exit(0)
    else:
        logger.error("❌ 英语学习文章评估功能测试失败！")
        exit(1)
