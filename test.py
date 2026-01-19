#!/usr/bin/env python3
"""
总测试文件
调用所有测试模块并检查配置完整性
"""

import os
import sys
import subprocess

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    CRAWLER_CONFIG
)

def check_config():
    """
    检查配置项是否完整
    返回：bool - 配置是否完整
    """
    print("=== 检查配置完整性 ===")
    
    missing_configs = []
    
    # 检查大模型配置
    if not OPENAI_API_KEY:
        missing_configs.append("OPENAI_API_KEY")
    
    if not OPENAI_MODEL:
        missing_configs.append("OPENAI_MODEL")
    
    # 检查爬虫配置
    for platform, config in CRAWLER_CONFIG.items():
        if platform == "ZHIHU":
            if not config.get("COOKIE"):
                missing_configs.append(f"CRAWLER_CONFIG.ZHIHU.COOKIE")
    
    # 输出检查结果
    if missing_configs:
        print("[错误] 发现以下配置项缺失：")
        for config_item in missing_configs:
            print(f"  - {config_item}")
        return False
    else:
        print("[成功] 所有配置项完整")
        return True

def run_test_file(test_file_path):
    """
    运行单个测试文件
    参数：test_file_path - 测试文件路径
    返回：bool - 测试是否通过
    """
    print(f"\n=== 运行测试：{os.path.basename(test_file_path)} ===")
    try:
        result = subprocess.run(
            [sys.executable, test_file_path],
            check=True,
            capture_output=True,
            text=True
        )
        print("[成功] 测试通过")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[错误] 测试失败，返回码：{e.returncode}")
        print("错误输出：")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"[错误] 测试执行出错：{str(e)}")
        return False

def main():
    """
    主函数
    """
    # 解析命令行参数
    import argparse
    parser = argparse.ArgumentParser(description='总测试文件')
    parser.add_argument('--check-config-only', action='store_true', 
                       help='仅检查配置完整性，不运行测试')
    args = parser.parse_args()
    
    # 检查配置
    config_ok = check_config()
    
    # 如果只需要检查配置，直接退出
    if args.check_config_only:
        if config_ok:
            sys.exit(0)
        else:
            sys.exit(1)
    
    # 定义测试文件路径
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script", "test")
    test_files = [
        os.path.join(test_dir, "test_module.py"),
        os.path.join(test_dir, "test_search.py")
    ]
    
    # 运行测试
    print("\n=== 开始执行测试 ===")
    test_results = []
    
    for test_file in test_files:
        if os.path.exists(test_file):
            result = run_test_file(test_file)
            test_results.append(result)
        else:
            print(f"\n[错误] 测试文件不存在：{test_file}")
            test_results.append(False)
    
    # 汇总结果
    print("\n=== 测试结果汇总 ===")
    total_tests = len(test_results)
    passed_tests = sum(test_results)
    
    if passed_tests == total_tests:
        print(f"[成功] 所有 {total_tests} 个测试通过")
        if config_ok:
            print("[成功] 配置完整，所有测试通过！")
            sys.exit(0)
        else:
            print("[警告] 所有测试通过，但配置存在缺失")
            sys.exit(1)
    else:
        print(f"[错误] {passed_tests}/{total_tests} 个测试通过，{total_tests - passed_tests} 个测试失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
