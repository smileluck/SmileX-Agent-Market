@echo off
REM 项目快速启动脚本（Windows）

echo ========================================
echo SmileX-Agent-Mark 快速启动脚本
echo ========================================
echo.

REM 检查uv是否安装
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到UV，请先安装UV
    echo 安装命令: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 ^| iex"
    pause
    exit /b 1
)

echo [1/3] 同步项目依赖...
uv sync --extra dev
if %errorlevel% neq 0 (
    echo [错误] 依赖同步失败
    pause
    exit /b 1
)

echo.
echo [2/3] 运行主程序...
uv run python main.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 程序运行失败
    pause
    exit /b 1
)

echo.
echo [3/3] 程序执行完成
pause
