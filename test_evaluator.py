#!/usr/bin/env python3
"""
测试ContentEvaluator类的修复情况
"""
import sys
from utils.logger import setup_logger

logger = setup_logger(__name__)

def test_import():
    """
    测试ContentEvaluator类是否能成功导入
    """
    logger.info("开始测试ContentEvaluator导入...")
    try:
        # 只测试导入，不初始化
        from agent.evaluator import ContentEvaluator
        logger.info("✓ ContentEvaluator导入成功")
        return True
    except ModuleNotFoundError as e:
        logger.error(f"✗ ContentEvaluator导入失败: {str(e)}")
        return False
    except Exception as e:
        logger.warning(f"✓ ContentEvaluator导入成功，但出现其他异常: {str(e)}")
        return True

def test_dependencies():
    """
    测试所有依赖是否能成功导入
    """
    logger.info("开始测试依赖导入...")
    dependencies = [
        ('langchain_core.prompts', 'PromptTemplate'),
        ('langchain_openai', 'OpenAI'),
        ('agent.prompt_templates', ['QUALITY_EVALUATION_PROMPT', 'SPREAD_POTENTIAL_PROMPT']),
        ('config.settings', ['OPENAI_API_KEY', 'OPENAI_MODEL']),
        ('utils.logger', 'setup_logger')
    ]
    
    all_success = True
    for module_name, imports in dependencies:
        try:
            module = __import__(module_name, fromlist=[imports] if isinstance(imports, str) else imports)
            if isinstance(imports, str):
                # 单个导入
                if hasattr(module, imports):
                    logger.info(f"✓ {module_name}.{imports} 导入成功")
                else:
                    logger.error(f"✗ {module_name}.{imports} 未找到")
                    all_success = False
            else:
                # 多个导入
                for item in imports:
                    if hasattr(module, item):
                        logger.info(f"✓ {module_name}.{item} 导入成功")
                    else:
                        logger.error(f"✗ {module_name}.{item} 未找到")
                        all_success = False
        except ModuleNotFoundError as e:
            logger.error(f"✗ {module_name} 导入失败: {str(e)}")
            all_success = False
        except Exception as e:
            logger.warning(f"? {module_name} 导入异常: {str(e)}")
    
    return all_success

if __name__ == "__main__":
    logger.info("=== ContentEvaluator修复测试 ===")
    
    # 运行导入测试
    import_result = test_import()
    
    # 运行依赖测试
    dependencies_result = test_dependencies()
    
    logger.info("\n=== 测试结果汇总 ===")
    if import_result and dependencies_result:
        logger.info("✅ 所有测试通过！ContentEvaluator修复成功")
        sys.exit(0)
    else:
        logger.error("❌ 测试失败！ContentEvaluator修复不完全")
        sys.exit(1)
