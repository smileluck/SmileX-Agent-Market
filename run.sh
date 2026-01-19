#!/bin/bash
# 项目快速启动脚本（Linux/Mac）

echo "========================================"
echo "SmileX-Agent-Mark 快速启动脚本"
echo "========================================"
echo

# 检查uv是否安装
if ! command -v uv &> /dev/null; then
    echo "[错误] 未检测到UV，请先安装UV"
    echo "安装命令: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "[1/3] 同步项目依赖..."
uv sync --extra dev
if [ $? -ne 0 ]; then
    echo "[错误] 依赖同步失败"
    exit 1
fi

echo
echo "[2/3] 运行主程序..."
uv run python main.py

if [ $? -ne 0 ]; then
    echo
    echo "[错误] 程序运行失败"
    exit 1
fi

echo
echo "[3/3] 程序执行完成"
