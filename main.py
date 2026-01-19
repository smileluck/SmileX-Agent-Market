"""
运营增长Agent项目主入口
"""
import time
import pandas as pd
from config.settings import PROJECT_ROOT
from utils.logger import setup_logger
from crawler.zhihu.zhihu_crawler import ZhihuCrawler
from data.storage import data_storage
from agent.evaluator import ContentEvaluator
from visualization.charts import ChartGenerator

# 初始化日志
logger = setup_logger(__name__)


def main():
    """
    项目主函数，实现完整的工作流程
    """
    logger.info("=== 运营增长Agent系统启动 ===")
    logger.info(f"项目根目录: {PROJECT_ROOT}")
    
    try:
        # 1. 初始化各个模块
        logger.info("初始化系统模块...")
        zhihu_crawler = ZhihuCrawler()
        chart_generator = ChartGenerator()
        
        # 2. 爬取知乎热门问题
        logger.info("开始爬取知乎热门问题...")
        questions = zhihu_crawler.get_hot_questions(limit=20)
        
        if not questions:
            logger.warning("未爬取到知乎热门问题")
            return
        
        # 3. 保存问题到数据库
        logger.info("保存知乎热门问题到数据库...")
        saved_count = data_storage.save_zhihu_questions(questions)
        logger.info(f"成功保存 {saved_count} 个知乎热门问题")
        
        # 4. 对问题进行评估（如果配置了OpenAI API）
        try:
            evaluator = ContentEvaluator()
            
            for question in questions:
                logger.info(f"评估问题: {question['title']}")
                
                # 构造评估内容
                content = f"标题: {question['title']}\n描述: {question.get('excerpt', '')}"
                
                # 综合评估
                evaluation_result = evaluator.evaluate_comprehensive(content)
                
                # 保存评估结果
                score_data = {
                    'content_id': question['question_id'],
                    'content_type': 'question',
                    'quality_score': evaluation_result['quality_score'],
                    'spread_score': evaluation_result['spread_score'],
                    'operation_score': evaluation_result['operation_score'],
                    'total_score': evaluation_result['total_score'],
                    'evaluation_details': evaluation_result['details']
                }
                
                data_storage.save_content_score(score_data)
                
                # 添加延迟，避免API调用过快
                time.sleep(2)
        except ValueError as e:
            logger.warning(f"内容评估模块未初始化: {str(e)}")
        except Exception as e:
            logger.error(f"内容评估失败: {str(e)}")
        
        # 5. 生成可视化图表
        logger.info("生成数据可视化图表...")
        
        # 获取保存的数据
        saved_questions = data_storage.get_zhihu_questions(limit=20)
        
        if saved_questions:
            # 转换为DataFrame
            questions_df = pd.DataFrame([{
                '标题': q.title,
                '排名': q.rank,
                '热度': q.metrics,
                '爬取时间': q.crawl_time
            } for q in saved_questions])
            
            # 生成热门问题排名柱状图
            chart_generator.generate_bar_chart(
                data=questions_df,
                x_col='标题',
                y_col='排名',
                title='知乎热门问题排名',
                filename='zhihu_hot_questions_rank.png',
                ylabel='排名'
            )
        
        # 获取内容评分数据
        content_scores = data_storage.get_content_scores(content_type='question', limit=20)
        
        if content_scores:
            # 转换为DataFrame
            scores_df = pd.DataFrame([{
                '内容ID': score.content_id,
                '质量评分': score.quality_score,
                '传播潜力评分': score.spread_score,
                '运营价值评分': score.operation_score,
                '总评分': score.total_score
            } for score in content_scores])
            
            # 生成评分对比柱状图
            chart_generator.generate_bar_chart(
                data=scores_df,
                x_col='内容ID',
                y_col='总评分',
                title='内容综合评分',
                filename='content_comprehensive_scores.png',
                ylabel='评分'
            )
            
            # 生成评分热力图（相关性分析）
            correlation_data = scores_df[['质量评分', '传播潜力评分', '运营价值评分', '总评分']].corr()
            chart_generator.generate_heatmap(
                data=correlation_data,
                title='评分维度相关性热力图',
                filename='scores_correlation_heatmap.png'
            )
        
        logger.info("=== 运营增长Agent系统运行完成 ===")
        
    except Exception as e:
        logger.error(f"系统运行出错: {str(e)}")
        logger.exception("完整错误堆栈:")
        # 不立即抛出，继续执行后续清理操作
        pass
    finally:
        logger.info("=== 运营增长Agent系统关闭 ===")


if __name__ == "__main__":
    main()
