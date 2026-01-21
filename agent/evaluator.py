"""
内容评估模块，实现基于大模型的内容评估功能
"""
import re
from typing import Dict, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from agent.prompt_templates import (
    QUALITY_EVALUATION_PROMPT,
    SPREAD_POTENTIAL_PROMPT,
    OPERATION_VALUE_PROMPT,
    COMPREHENSIVE_EVALUATION_PROMPT,
    ENGLISH_ARTICLE_EVALUATION_PROMPT
)
from config.settings import OPENAI_API_KEY, OPENAI_MODEL, LLM_TYPE, VLLM_API_BASE, VLLM_API_KEY, VLLM_MODEL
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ContentEvaluator:
    """
    内容评估器，用于评估内容的质量、传播潜力和运营价值
    """
    
    def __init__(self):
        """
        初始化内容评估器
        """
        # 根据配置选择LLM类型
        if LLM_TYPE == "vllm":
            # 使用本地VLLM部署的模型
            logger.info(f"使用VLLM模型: {VLLM_MODEL}，API地址: {VLLM_API_BASE}")
            self.llm = ChatOpenAI(
                model=VLLM_MODEL,
                api_key=VLLM_API_KEY,
                base_url=VLLM_API_BASE,
                temperature=0.3,
                max_tokens=500
            )
        else:
            # 使用OpenAI模型
            if not OPENAI_API_KEY:
                raise ValueError("OpenAI API密钥未配置，请在环境变量中设置OPENAI_API_KEY")
            logger.info(f"使用OpenAI模型: {OPENAI_MODEL}")
            self.llm = ChatOpenAI(
                model=OPENAI_MODEL,
                api_key=OPENAI_API_KEY,
                temperature=0.3,
                max_tokens=500
            )
        
        # 初始化评估提示模板
        self._init_evaluation_prompts()
    
    def _init_evaluation_prompts(self):
        """
        初始化各种评估提示模板
        """
        # 内容质量评估提示
        self.quality_prompt = PromptTemplate(
            input_variables=["content"],
            template=QUALITY_EVALUATION_PROMPT
        )
        
        # 传播潜力评估提示
        self.spread_prompt = PromptTemplate(
            input_variables=["content"],
            template=SPREAD_POTENTIAL_PROMPT
        )
        
        # 运营价值评估提示
        self.operation_prompt = PromptTemplate(
            input_variables=["content"],
            template=OPERATION_VALUE_PROMPT
        )
        
        # 综合评估提示
        self.comprehensive_prompt = PromptTemplate(
            input_variables=["content"],
            template=COMPREHENSIVE_EVALUATION_PROMPT
        )
        
        # 英语学习文章评估提示
        self.english_article_prompt = PromptTemplate(
            input_variables=["title", "content"],
            template=ENGLISH_ARTICLE_EVALUATION_PROMPT
        )
    
    def evaluate_quality(self, content: str) -> Dict[str, Any]:
        """
        评估内容质量
        
        Args:
            content (str): 待评估的内容
        
        Returns:
            Dict[str, Any]: 评估结果
        """
        logger.info("开始评估内容质量")
        
        try:
            # 生成完整提示
            prompt = self.quality_prompt.format(content=content)
            # 调用LLM
            result = self.llm.invoke(prompt)
            # 提取AIMessage中的内容
            result_content = result.content if hasattr(result, 'content') else str(result)
            parsed_result = self._parse_quality_result(result_content)
            logger.info("内容质量评估完成")
            return parsed_result
        except Exception as e:
            logger.error(f"内容质量评估失败，错误: {str(e)}")
            return self._get_default_evaluation("quality")
    
    def evaluate_spread_potential(self, content: str) -> Dict[str, Any]:
        """
        评估内容传播潜力
        
        Args:
            content (str): 待评估的内容
        
        Returns:
            Dict[str, Any]: 评估结果
        """
        logger.info("开始评估内容传播潜力")
        
        try:
            # 生成完整提示
            prompt = self.spread_prompt.format(content=content)
            # 调用LLM
            result = self.llm.invoke(prompt)
            # 提取AIMessage中的内容
            result_content = result.content if hasattr(result, 'content') else str(result)
            parsed_result = self._parse_spread_result(result_content)
            logger.info("内容传播潜力评估完成")
            return parsed_result
        except Exception as e:
            logger.error(f"内容传播潜力评估失败，错误: {str(e)}")
            return self._get_default_evaluation("spread")
    
    def evaluate_operation_value(self, content: str) -> Dict[str, Any]:
        """
        评估内容运营价值
        
        Args:
            content (str): 待评估的内容
        
        Returns:
            Dict[str, Any]: 评估结果
        """
        logger.info("开始评估内容运营价值")
        
        try:
            # 生成完整提示
            prompt = self.operation_prompt.format(content=content)
            # 调用LLM
            result = self.llm.invoke(prompt)
            # 提取AIMessage中的内容
            result_content = result.content if hasattr(result, 'content') else str(result)
            parsed_result = self._parse_operation_result(result_content)
            logger.info("内容运营价值评估完成")
            return parsed_result
        except Exception as e:
            logger.error(f"内容运营价值评估失败，错误: {str(e)}")
            return self._get_default_evaluation("operation")
    
    def evaluate_comprehensive(self, content: str) -> Dict[str, Any]:
        """
        综合评估内容
        
        Args:
            content (str): 待评估的内容
        
        Returns:
            Dict[str, Any]: 综合评估结果
        """
        logger.info("开始综合评估内容")
        
        try:
            # 生成完整提示
            prompt = self.comprehensive_prompt.format(content=content)
            # 调用LLM
            result = self.llm.invoke(prompt)
            # 提取AIMessage中的内容
            result_content = result.content if hasattr(result, 'content') else str(result)
            parsed_result = self._parse_comprehensive_result(result_content)
            logger.info("内容综合评估完成")
            return parsed_result
        except Exception as e:
            logger.error(f"内容综合评估失败，错误: {str(e)}")
            return self._get_default_comprehensive_evaluation()
    
    def _parse_quality_result(self, result: str) -> Dict[str, Any]:
        """
        解析质量评估结果
        
        Args:
            result (str): LLM返回的评估结果
        
        Returns:
            Dict[str, Any]: 解析后的评估结果
        """
        return self._parse_single_dimension_result(result, "质量")
    
    def _parse_spread_result(self, result: str) -> Dict[str, Any]:
        """
        解析传播潜力评估结果
        
        Args:
            result (str): LLM返回的评估结果
        
        Returns:
            Dict[str, Any]: 解析后的评估结果
        """
        return self._parse_single_dimension_result(result, "传播潜力")
    
    def _parse_operation_result(self, result: str) -> Dict[str, Any]:
        """
        解析运营价值评估结果
        
        Args:
            result (str): LLM返回的评估结果
        
        Returns:
            Dict[str, Any]: 解析后的评估结果
        """
        return self._parse_single_dimension_result(result, "运营价值")
    
    def _parse_single_dimension_result(self, result: str, dimension: str) -> Dict[str, Any]:
        """
        解析单维度评估结果
        
        Args:
            result (str): LLM返回的评估结果
            dimension (str): 评估维度
        
        Returns:
            Dict[str, Any]: 解析后的评估结果
        """
        parsed = {
            "dimension": dimension,
            "score": 0.0,
            "sub_scores": {},
            "reason": ""
        }
        
        # 提取总体评分
        total_score_match = re.search(rf'总体{dimension}评分：\s*(\d+\.?\d*)', result)
        if total_score_match:
            parsed["score"] = float(total_score_match.group(1))
        
        # 提取评估理由
        reason_match = re.search(r'评估理由：\s*(.+)$', result, re.DOTALL)
        if reason_match:
            parsed["reason"] = reason_match.group(1).strip()
        
        # 提取子维度评分
        sub_score_pattern = re.compile(r'(.+?)：\s*(\d+\.?\d*)')
        sub_scores = sub_score_pattern.findall(result)
        
        for sub_dimension, score in sub_scores:
            if sub_dimension not in [f"总体{dimension}评分", "评估理由"]:
                parsed["sub_scores"][sub_dimension] = float(score)
        
        return parsed
    
    def _parse_comprehensive_result(self, result: str) -> Dict[str, Any]:
        """
        解析综合评估结果
        
        Args:
            result (str): LLM返回的评估结果
        
        Returns:
            Dict[str, Any]: 解析后的评估结果
        """
        parsed = {
            "quality_score": 0.0,
            "spread_score": 0.0,
            "operation_score": 0.0,
            "total_score": 0.0,
            "details": ""
        }
        
        # 提取各维度评分
        quality_match = re.search(r'内容质量评分：\s*(\d+\.?\d*)', result)
        if quality_match:
            parsed["quality_score"] = float(quality_match.group(1))
        
        spread_match = re.search(r'传播潜力评分：\s*(\d+\.?\d*)', result)
        if spread_match:
            parsed["spread_score"] = float(spread_match.group(1))
        
        operation_match = re.search(r'运营价值评分：\s*(\d+\.?\d*)', result)
        if operation_match:
            parsed["operation_score"] = float(operation_match.group(1))
        
        total_match = re.search(r'综合总评分：\s*(\d+\.?\d*)', result)
        if total_match:
            parsed["total_score"] = float(total_match.group(1))
        
        # 提取评估详情
        details_match = re.search(r'评估详情：\s*(.+)$', result, re.DOTALL)
        if details_match:
            parsed["details"] = details_match.group(1).strip()
        
        return parsed
    
    def _get_default_evaluation(self, dimension: str) -> Dict[str, Any]:
        """
        获取默认评估结果
        
        Args:
            dimension (str): 评估维度
        
        Returns:
            Dict[str, Any]: 默认评估结果
        """
        return {
            "dimension": dimension,
            "score": 5.0,
            "sub_scores": {},
            "reason": "评估失败，使用默认评分"
        }
    
    def evaluate_english_article(self, title: str, content: str) -> Dict[str, Any]:
        """
        评估英语学习文章
        
        Args:
            title (str): 文章标题
            content (str): 文章内容
        
        Returns:
            Dict[str, Any]: 评估结果
        """
        logger.info("开始评估英语学习文章")
        
        try:
            # 生成完整提示
            prompt = self.english_article_prompt.format(title=title, content=content)
            # 调用LLM
            result = self.llm.invoke(prompt)
            # 提取AIMessage中的内容
            result_content = result.content if hasattr(result, 'content') else str(result)
            # 打印原始评估结果，用于调试
            logger.debug(f"原始评估结果: {result_content}")
            parsed_result = self._parse_english_article_result(result_content)
            logger.info("英语学习文章评估完成")
            return parsed_result
        except Exception as e:
            logger.error(f"英语学习文章评估失败，错误: {str(e)}")
            # 打印原始评估结果，用于调试
            logger.debug(f"原始评估结果: {result_content if 'result_content' in locals() else '未获取到结果'}")
            return self._get_default_english_article_evaluation()
    
    def _parse_english_article_result(self, result: str) -> Dict[str, Any]:
        """
        解析英语学习文章评估结果
        
        Args:
            result (str): LLM返回的评估结果
        
        Returns:
            Dict[str, Any]: 解析后的评估结果
        """
        parsed = {
            "title": "",
            "target_audience_score": 0.0,
            "product_relevance_score": 0.0,
            "learning_advice_score": 0.0,
            "total_score": 0.0,
            "grade": "",
            "match_analysis": "",
            "core_pain_points": []
        }
        
        # 提取文章标题
        title_match = re.search(r'文章标题：(.+)', result)
        if title_match:
            parsed["title"] = title_match.group(1).strip()
        
        # 提取各维度评分
        target_audience_match = re.search(r'目标人群相关性：\s*(\d+\.?\d*)', result)
        if target_audience_match:
            parsed["target_audience_score"] = float(target_audience_match.group(1))
        
        product_relevance_match = re.search(r'产品定位相关性：\s*(\d+\.?\d*)', result)
        if product_relevance_match:
            parsed["product_relevance_score"] = float(product_relevance_match.group(1))
        
        learning_advice_match = re.search(r'学习建议实用性：\s*(\d+\.?\d*)', result)
        if learning_advice_match:
            parsed["learning_advice_score"] = float(learning_advice_match.group(1))
        else:
            # 若未提取到学习建议实用性，使用默认值5分
            parsed["learning_advice_score"] = 5.0
        
        # 提取总分
        total_match = re.search(r'总分：\s*(\d+\.?\d*)', result)
        if total_match:
            parsed["total_score"] = float(total_match.group(1))
        else:
            # 若未提取到总分，自行计算
            parsed["total_score"] = (
                parsed["target_audience_score"] * 0.5 + 
                parsed["product_relevance_score"] * 0.3 + 
                parsed["learning_advice_score"] * 0.2
            )
        
        # 提取分级
        grade_match = re.search(r'分级：\s*([SABC]级)', result)
        if grade_match:
            parsed["grade"] = grade_match.group(1)
        else:
            # 若未提取到分级，根据总分自行计算
            if parsed["total_score"] >= 9:
                parsed["grade"] = "S级"
            elif parsed["total_score"] >= 7:
                parsed["grade"] = "A级"
            elif parsed["total_score"] >= 5:
                parsed["grade"] = "B级"
            else:
                parsed["grade"] = "C级"
        
        # 提取核心相关点/不相关点分析
        match_analysis_match = re.search(r'核心相关点/不相关点分析：\s*(.+)', result)
        if match_analysis_match:
            parsed["match_analysis"] = match_analysis_match.group(1).strip()
        else:
            # 尝试另一种格式
            match_analysis_match = re.search(r'核心相关点分析：\s*(.+)', result)
            if match_analysis_match:
                parsed["match_analysis"] = match_analysis_match.group(1).strip()
            else:
                # 兼容旧格式
                match_analysis_match = re.search(r'核心匹配点/不匹配点分析：\s*(.+)', result)
                if match_analysis_match:
                    parsed["match_analysis"] = match_analysis_match.group(1).strip()
                else:
                    match_analysis_match = re.search(r'核心匹配点分析：\s*(.+)', result)
                    if match_analysis_match:
                        parsed["match_analysis"] = match_analysis_match.group(1).strip()
        
        # 提取核心用户痛点
        pain_points_match = re.search(r'核心用户痛点：\s*(.+)', result)
        if pain_points_match:
            pain_points_text = pain_points_match.group(1).strip()
            # 分割痛点，处理不同格式
            if '、' in pain_points_text:
                parsed["core_pain_points"] = [point.strip() for point in pain_points_text.split('、')]
            elif ',' in pain_points_text:
                parsed["core_pain_points"] = [point.strip() for point in pain_points_text.split(',')]
            else:
                parsed["core_pain_points"] = [pain_points_text]
        
        return parsed
    
    def _get_default_english_article_evaluation(self) -> Dict[str, Any]:
        """
        获取默认英语学习文章评估结果
        
        Returns:
            Dict[str, Any]: 默认评估结果
        """
        return {
            "title": "",
            "target_audience_score": 5.0,
            "product_relevance_score": 5.0,
            "learning_advice_score": 5.0,
            "total_score": 5.0,
            "grade": "B级",
            "match_analysis": "评估失败，使用默认评分",
            "core_pain_points": []
        }
