@echo off
echo 正在构建重要信息管理器exe文件...
echo.

REM 激活conda环境
call conda activate info_manager
if errorlevel 1 (
    echo 错误: 无法激活conda环境
    pause
    exit /b 1
)

REM 清理之前的构建文件
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM 使用PyInstaller构建exe
echo 开始构建...
pyinstaller build_exe.spec

if errorlevel 1 (
    echo 构建失败!
    pause
    exit /b 1
)

echo.
echo 构建成功!
echo exe文件位置: dist\重要信息管理器.exe
echo.

REM 询问是否运行exe文件
set /p choice="是否立即运行exe文件? (y/n): "
if /i "%choice%"=="y" (
    echo 正在启动exe文件...
    start "" "dist\重要信息管理器.exe"
)

echo.
echo 构建完成!
pause
