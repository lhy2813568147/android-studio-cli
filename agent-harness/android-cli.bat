@echo off
REM Android Studio CLI 便捷启动脚本
REM 使用方法: android-cli.bat [命令]

set SCRIPT_DIR=%~dp0
set CLI_DIR=%SCRIPT_DIR%

REM 设置Android SDK环境变量
if not defined ANDROID_HOME set ANDROID_HOME=%USERPROFILE%\AppData\Local\Android\Sdk
set PATH=%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\emulator;%ANDROID_HOME%\cmdline-tools\latest\bin;%PATH%

REM 运行CLI
cd /d "%CLI_DIR%"
python -m cli_anything.android_studio %*