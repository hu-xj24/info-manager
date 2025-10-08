@echo off
echo 启动重要信息管理器...
echo.

REM 检查exe文件是否存在
if not exist "dist\重要信息管理器.exe" (
    echo 错误: 找不到exe文件
    echo 请先运行 build.bat 构建exe文件
    pause
    exit /b 1
)

REM 运行exe文件
echo 正在启动程序...
start "" "dist\重要信息管理器.exe"

echo 程序已启动!
