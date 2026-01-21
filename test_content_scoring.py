#!/usr/bin/env python3
"""
测试脚本：直接从存储中获取数据并进行内容评分
支持命令行参数，可灵活配置评估类型和数量
"""
import sys
import time
import argparse
from utils.logger import setup_logger
from data.storage import data_storage
from agent.evaluator import ContentEvaluator

logger = setup_logger(__name__)

def parse_args():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='从存储中获取数据并进行内容评分')
    parser.add_argument('--type', '-t', 
                        choices=['question', 'answer', 'all'], 
                        default='all',
                        help='要评估的内容类型 (默认: all)')
    parser.add_argument('--limit', '-l', 
                        type=int, 
                        default=10,
                        help='评估数量限制 (默认: 10)')
    parser.add_argument('--offset', '-o', 
                        type=int, 
                        default=0,
                        help='评估起始偏移量 (默认: 0)')
    parser.add_argument('--delay', '-d', 
                        type=float, 
                        default=2.0,
                        help='API调用间隔时间(秒) (默认: 2.0)')
    parser.add_argument('--verbose', '-v', 
                        action='store_true',
                        help='显示详细日志')
    parser.add_argument('--evaluation-type', '-e', 
                        choices=['comprehensive', 'english_article'], 
                        default='english_article',
                        help='评估类型 (默认: english_article)')
    return parser.parse_args()

def evaluate_content(evaluator, content_id, content_type, content_text, title, evaluation_type, delay):
    """
    评估单个内容并保存结果
    """
    try:
        if evaluation_type == 'english_article':
            # 英语学习文章评估
            evaluation_result = evaluator.evaluate_english_article(title, content_text)
            
            # 保存评估结果
            score_data = {
                'content_id': content_id,
                'content_type': content_type,
                'total_score': evaluation_result['total_score'],
                'english_article_score': evaluation_result['total_score'],
                'target_audience_score': evaluation_result['target_audience_score'],
                'product_relevance_score': evaluation_result['product_relevance_score'],
                'learning_advice_score': evaluation_result['learning_advice_score'],
                'grade': evaluation_result['grade'],
                'match_analysis': evaluation_result['match_analysis'],
                'core_pain_points': ','.join(evaluation_result['core_pain_points']),
                'evaluation_details': f"分级: {evaluation_result['grade']}, 匹配分析: {evaluation_result['match_analysis']}, 核心痛点: {','.join(evaluation_result['core_pain_points'])}"
            }
        else:
            # 综合评估
            evaluation_result = evaluator.evaluate_comprehensive(content_text)
            
            # 保存评估结果
            score_data = {
                'content_id': content_id,
                'content_type': content_type,
                'quality_score': evaluation_result['quality_score'],
                'spread_score': evaluation_result['spread_score'],
                'operation_score': evaluation_result['operation_score'],
                'total_score': evaluation_result['total_score'],
                'evaluation_details': evaluation_result['details']
            }
        
        saved = data_storage.save_content_score(score_data)
        
        if saved:
            return {
                'success': True,
                'result': evaluation_result
            }
        else:
            return {
                'success': False,
                'error': '评分保存失败'
            }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
    finally:
        # 添加延迟，避免API调用过快
        time.sleep(delay)

def main():
    """
    主函数：从存储中获取数据并进行内容评分
    """
    args = parse_args()
    logger.info("=== 从存储获取数据并进行内容评分测试 ===")
    logger.info(f"评估类型: {args.type}")
    logger.info(f"评估数量: {args.limit}")
    logger.info(f"起始偏移: {args.offset}")
    logger.info(f"API延迟: {args.delay}秒")
    logger.info(f"评估方式: {args.evaluation_type}")
    
    try:
        # 1. 初始化评估器
        logger.info("初始化内容评估器...")
        evaluator = ContentEvaluator()
        logger.info("✓ 内容评估器初始化成功")
        
        # 2. 获取要评估的数据
        logger.info("从数据库获取数据...")
        
        # 存储所有要评估的内容
        contents_to_evaluate = []
        
        # 根据类型获取数据
        if args.type in ['question', 'all']:
            questions = data_storage.get_zhihu_questions(
                limit=args.limit,
                offset=args.offset
            )
            for question in questions:
                content_text = f"标题: {question.title}\n描述: {question.excerpt if question.excerpt else ''}"
                contents_to_evaluate.append({
                    'id': question.question_id,
                    'type': 'question',
                    'text': content_text,
                    'title': question.title
                })
        
        if args.type in ['answer', 'all']:
            # 注：需要在data/storage.py中添加get_zhihu_answers方法
            # 这里假设该方法已存在，否则需要先实现
            try:
                answers = data_storage.get_zhihu_answers(
                    limit=args.limit,
                    offset=args.offset
                )
                for answer in answers:
                    content_text = f"回答内容: {answer.content}"
                    contents_to_evaluate.append({
                        'id': answer.answer_id,
                        'type': 'answer',
                        'text': content_text,
                        'title': f"回答 #{answer.answer_id}"
                    })
            except AttributeError:
                logger.warning("✗ 数据存储未实现get_zhihu_answers方法，跳过回答评估")
        
        if not contents_to_evaluate:
            logger.warning("未从数据库获取到可评估的内容")
            return 0
        
        logger.info(f"✓ 成功获取 {len(contents_to_evaluate)} 个待评估内容")
        
        # 3. 对内容进行评分
        logger.info("开始对内容进行评分...")
        scored_count = 0
        failed_count = 0
        
        for i, content in enumerate(contents_to_evaluate[:args.limit], 1):
            logger.info(f"\n--- 评估 {i}/{args.limit}: {content['title']} ({content['type']}) ---")
            
            # 打印待评估内容
            logger.info(f"待评估内容: {content['text']}...")
            logger.info(f"内容类型: {content['type']}")
            logger.info(f"内容ID: {content['id']}")
            
            result = evaluate_content(
                evaluator=evaluator,
                content_id=content['id'],
                content_type=content['type'],
                content_text=content['text'],
                title=content['title'],
                evaluation_type=args.evaluation_type,
                delay=args.delay
            )
            
            if result['success']:
                logger.info(f"✓ 评分成功，总分: {result['result']['total_score']:.2f}")
                # if args.verbose:
                if args.evaluation_type == 'english_article':
                        logger.info(f"  目标人群相关性: {result['result']['target_audience_score']:.2f}")
                        logger.info(f"  产品定位相关性: {result['result']['product_relevance_score']:.2f}")
                        logger.info(f"  学习建议与经历分享: {result['result']['learning_advice_score']:.2f}")
                        logger.info(f"  分级: {result['result']['grade']}")
                        logger.info(f"  匹配分析: {result['result']['match_analysis']}")
                        logger.info(f"  核心用户痛点: {result['result']['core_pain_points']}")
                else:
                    logger.info(f"  质量评分: {result['result']['quality_score']:.2f}")
                    logger.info(f"  传播潜力评分: {result['result']['spread_score']:.2f}")
                    logger.info(f"  运营价值评分: {result['result']['operation_score']:.2f}")
                    logger.info(f"  评估理由: {result['result']['details'][:100]}...")
                scored_count += 1
            else:
                logger.error(f"✗ 评分失败，错误: {result['error']}")
                failed_count += 1
        
        # 4. 输出测试结果汇总
        logger.info(f"\n=== 测试结果汇总 ===")
        logger.info(f"总评估数: {len(contents_to_evaluate[:args.limit])}")
        logger.info(f"成功评估: {scored_count}")
        logger.info(f"失败评估: {failed_count}")
        logger.info(f"成功率: {(scored_count / len(contents_to_evaluate[:args.limit])):.2%}")
        
        # 5. 展示最新评分结果
        logger.info(f"\n=== 最新评分结果 ===")
        scores = data_storage.get_content_scores(limit=10)
        
        if scores:
            for score in scores:
                logger.info(f"\n内容ID: {score.content_id} (类型: {score.content_type})")
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
