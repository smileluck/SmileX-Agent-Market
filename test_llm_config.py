#!/usr/bin/env python3
"""
测试LLM配置是否正确
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import (
    LLM_TYPE, OPENAI_API_KEY, OPENAI_MODEL,
    VLLM_API_BASE, VLLM_API_KEY, VLLM_MODEL
)

def test_llm_config():
    """测试LLM配置是否正确加载"""
    print("=== LLM 配置测试 ===")
    print(f"LLM类型: {LLM_TYPE}")
    
    if LLM_TYPE == "openai":
        print(f"OpenAI模型: {OPENAI_MODEL}")
        print(f"OpenAI API Key: {'已配置' if OPENAI_API_KEY else '未配置'}")
    elif LLM_TYPE == "vllm":
        print(f"VLLM API地址: {VLLM_API_BASE}")
        print(f"VLLM模型: {VLLM_MODEL}")
        print(f"VLLM API Key: {VLLM_API_KEY}")
    else:
        print(f"未知的LLM类型: {LLM_TYPE}")
    
    print("\n=== 配置测试完成 ===")
    return True

if __name__ == "__main__":
    test_llm_config()
