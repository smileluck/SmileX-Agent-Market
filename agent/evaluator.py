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
    COMPREHENSIVE_EVALUATION_PROMPT
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
            parsed_result = self._parse_quality_result(result)
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
            parsed_result = self._parse_spread_result(result)
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
            parsed_result = self._parse_operation_result(result)
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
            parsed_result = self._parse_comprehensive_result(result)
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
    
    def _get_default_comprehensive_evaluation(self) -> Dict[str, Any]:
        """
        获取默认综合评估结果
        
        Returns:
            Dict[str, Any]: 默认综合评估结果
        """
        return {
            "quality_score": 5.0,
            "spread_score": 5.0,
            "operation_score": 5.0,
            "total_score": 5.0,
            "details": "综合评估失败，使用默认评分"
        }
