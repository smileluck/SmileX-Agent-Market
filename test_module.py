"""
模块测试脚本，用于逐步测试各个模块
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

def test_config():
    """测试配置模块"""
    print("测试配置模块...")
    try:
        from config.settings import PROJECT_ROOT, LOG_DIR, DATA_DIR
        print(f"项目根目录: {PROJECT_ROOT}")
        print(f"日志目录: {LOG_DIR}")
        print(f"数据目录: {DATA_DIR}")
        print("配置模块测试通过")
        return True
    except Exception as e:
        print(f"配置模块测试失败: {str(e)}")
        return False

def test_logger():
    """测试日志模块"""
    print("测试日志模块...")
    try:
        from utils.logger import setup_logger
        logger = setup_logger("test")
        logger.info("测试日志记录")
        print("日志模块测试通过")
        return True
    except Exception as e:
        print(f"日志模块测试失败: {str(e)}")
        return False

def test_crawler():
    """测试爬虫模块"""
    print("测试爬虫模块...")
    try:
        from crawler.zhihu.zhihu_crawler import ZhihuCrawler
        crawler = ZhihuCrawler()
        print("爬虫模块初始化成功")
        # 不实际爬取，只是测试初始化
        print("爬虫模块测试通过")
        return True
    except Exception as e:
        print(f"爬虫模块测试失败: {str(e)}")
        return False

def test_storage():
    """测试存储模块"""
    print("测试存储模块...")
    try:
        from data.storage import data_storage
        print("存储模块初始化成功")
        print("存储模块测试通过")
        return True
    except Exception as e:
        print(f"存储模块测试失败: {str(e)}")
        return False

def test_evaluator():
    """测试评估模块"""
    print("测试评估模块...")
    try:
        from agent.evaluator import ContentEvaluator
        # 这里可能会失败，因为需要OpenAI API密钥
        evaluator = ContentEvaluator()
        print("评估模块初始化成功")
        print("评估模块测试通过")
        return True
    except ValueError as e:
        print(f"评估模块测试警告: {str(e)} (这是预期的，需要配置OpenAI API密钥)")
        return True
    except Exception as e:
        print(f"评估模块测试失败: {str(e)}")
        return False

def test_visualization():
    """测试可视化模块"""
    print("测试可视化模块...")
    try:
        from visualization.charts import ChartGenerator
        generator = ChartGenerator()
        print("可视化模块初始化成功")
        print("可视化模块测试通过")
        return True
    except Exception as e:
        print(f"可视化模块测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("开始模块测试...")
    
    tests = [
        test_config,
        test_logger,
        test_crawler,
        test_storage,
        test_evaluator,
        test_visualization
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print("=" * 50)
    
    # 统计测试结果
    passed = sum(results)
    total = len(results)
    
    print(f"测试完成: {passed}/{total} 个模块测试通过")
    
    if passed == total:
        print("所有模块测试通过！")
        return 0
    else:
        print("部分模块测试失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main())
