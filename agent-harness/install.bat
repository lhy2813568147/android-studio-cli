@echo off
REM Android Studio CLI 安装脚本
REM 将CLI工具添加到PATH

set SCRIPT_DIR=%~dp0
set INSTALL_DIR=%USERPROFILE%\AppData\Local\AndroidStudioCLI

echo === Android Studio CLI 安装 ===
echo.

REM 创建安装目录
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM 复制脚本
copy "%SCRIPT_DIR%android-cli.bat" "%INSTALL_DIR%\android-cli.bat" >nul
copy "%SCRIPT_DIR%android-cli.ps1" "%INSTALL_DIR%\android-cli.ps1" >nul

REM 检查PATH
echo %PATH% | findstr /C:"%INSTALL_DIR%" >nul
if errorlevel 1 (
    echo 添加 %INSTALL_DIR% 到 PATH...
    
    REM 使用setx添加到用户PATH
    setx PATH "%PATH%;%INSTALL_DIR%"
    
    echo 请重新打开命令提示符以使更改生效
)

echo.
echo 安装完成！
echo.
echo 使用方法:
echo   android-cli adb devices
echo   android-cli emulator list-avds
echo   android-cli gradle build --variant debug
echo   android-cli repl