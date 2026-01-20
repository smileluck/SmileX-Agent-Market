#!/usr/bin/env python3
"""
测试脚本：直接从存储中获取数据并进行内容评分
"""
import sys
import time
from utils.logger import setup_logger
from data.storage import data_storage
from agent.evaluator import ContentEvaluator

logger = setup_logger(__name__)

def main():
    """
    主函数：从存储中获取数据并进行内容评分
    """
    logger.info("=== 从存储获取数据并进行内容评分测试 ===")
    
    try:
        # 1. 初始化评估器
        logger.info("初始化内容评估器...")
        evaluator = ContentEvaluator()
        logger.info("✓ 内容评估器初始化成功")
        
        # 2. 从数据库获取知乎问题
        logger.info("从数据库获取知乎问题...")
        questions = data_storage.get_zhihu_questions(limit=10)
        
        if not questions:
            logger.warning("未从数据库获取到知乎问题")
            return
        
        logger.info(f"✓ 成功获取 {len(questions)} 个知乎问题")
        
        # 3. 对每个问题进行评分
        logger.info("开始对问题进行评分...")
        scored_count = 0
        
        for question in questions:
            logger.info(f"\n--- 评估问题: {question.title} ---")
            
            try:
                # 构造评估内容
                content = f"标题: {question.title}\n描述: {question.excerpt if question.excerpt else ''}"
                
                # 综合评估
                evaluation_result = evaluator.evaluate_comprehensive(content)
                
                # 保存评估结果
                score_data = {
                    'content_id': question.question_id,
                    'content_type': 'question',
                    'quality_score': evaluation_result['quality_score'],
                    'spread_score': evaluation_result['spread_score'],
                    'operation_score': evaluation_result['operation_score'],
                    'total_score': evaluation_result['total_score'],
                    'evaluation_details': evaluation_result['details']
                }
                
                saved = data_storage.save_content_score(score_data)
                
                if saved:
                    logger.info(f"✓ 评分成功，总分: {evaluation_result['total_score']:.2f}")
                    logger.info(f"  质量评分: {evaluation_result['quality_score']:.2f}")
                    logger.info(f"  传播潜力评分: {evaluation_result['spread_score']:.2f}")
                    logger.info(f"  运营价值评分: {evaluation_result['operation_score']:.2f}")
                    scored_count += 1
                else:
                    logger.error(f"✗ 评分保存失败")
                
                # 添加延迟，避免API调用过快
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"✗ 评估问题失败，错误: {str(e)}")
        
        # 4. 输出测试结果
        logger.info(f"\n=== 测试结果汇总 ===")
        logger.info(f"成功评估 {scored_count} 个问题")
        logger.info(f"评估失败 {len(questions) - scored_count} 个问题")
        
        # 5. 获取并展示最新评分
        logger.info(f"\n=== 最新评分结果 ===")
        scores = data_storage.get_content_scores(content_type='question', limit=10)
        
        if scores:
            for score in scores:
                question = data_storage.get_zhihu_question_by_id(score.content_id)
                if question:
                    logger.info(f"问题: {question.title}")
                    logger.info(f"  总分: {score.total_score:.2f}")
                    logger.info(f"  质量评分: {score.quality_score:.2f}")
                    logger.info(f"  传播潜力评分: {score.spread_score:.2f}")
                    logger.info(f"  运营价值评分: {score.operation_score:.2f}")
                    logger.info(f"  评估时间: {score.evaluation_time}")
        
        logger.info("\n✅ 测试完成！")
        return 0
        
    except ValueError as e:
        logger.error(f"✗ 内容评估模块未初始化: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"✗ 测试失败，错误: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
