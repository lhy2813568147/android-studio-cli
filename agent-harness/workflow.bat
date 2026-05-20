@echo off
REM Android 开发工作流脚本
REM 使用方法: workflow.bat [命令]

set SCRIPT_DIR=%~dp0
set CLI=python -m cli_anything.android_studio

if "%1"=="" goto show_help
if "%1"=="help" goto show_help
if "%1"=="--help" goto show_help
if "%1"=="-h" goto show_help

if "%1"=="devices" goto devices
if "%1"=="avds" goto avds
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="build" goto build
if "%1"=="test" goto test
if "%1"=="install" goto install
if "%1"=="clean" goto clean
if "%1"=="lint" goto lint
if "%1"=="logcat" goto logcat
if "%1"=="shell" goto shell
if "%1"=="screenshot" goto screenshot

echo 未知命令: %1
goto show_help

:show_help
echo Android 开发工作流脚本
echo.
echo 使用方法: %0 [命令]
echo.
echo 可用命令:
echo   devices          - 列出连接的设备
echo   avds             - 列出可用的AVD
echo   start ^<avd^>      - 启动模拟器
echo   stop ^<avd^>       - 停止模拟器
echo   build [variant]  - 构建项目
echo   test [variant]   - 运行测试
echo   install [variant]- 安装到设备
echo   clean            - 清理项目
echo   lint             - 代码检查
echo   logcat           - 查看日志
echo   shell ^<command^>  - 运行shell命令
echo   screenshot       - 截图
echo   help             - 显示此帮助
goto end

:devices
echo [INFO] 列出连接的设备...
%CLI% adb devices
goto end

:avds
echo [INFO] 列出可用的AVD...
%CLI% emulator list-avds
goto end

:start
if "%2"=="" (
    echo [ERROR] 请指定AVD名称
    echo 可用的AVD:
    %CLI% emulator list-avds
    goto end
)
echo [INFO] 启动模拟器: %2
%CLI% emulator start "%2"
goto end

:stop
if "%2"=="" (
    echo [WARN] 停止所有模拟器...
    %CLI% emulator stop
) else (
    echo [INFO] 停止模拟器: %2
    %CLI% emulator stop "%2"
)
goto end

:build
set variant=%2
if "%variant%"=="" set variant=debug
echo [INFO] 构建项目 (variant: %variant%)...
%CLI% gradle build --variant %variant%
goto end

:test
set variant=%2
if "%variant%"=="" set variant=debug
echo [INFO] 运行测试 (variant: %variant%)...
%CLI% gradle test --variant %variant% --type unit
goto end

:install
set variant=%2
if "%variant%"=="" set variant=debug
echo [INFO] 安装到设备 (variant: %variant%)...
%CLI% gradle install --variant %variant%
goto end

:clean
echo [INFO] 清理项目...
%CLI% gradle clean
goto end

:lint
set variant=%2
if "%variant%"=="" set variant=debug
echo [INFO] 运行代码检查 (variant: %variant%)...
%CLI% gradle lint --variant %variant%
goto end

:logcat
echo [INFO] 查看设备日志 (按 Ctrl+C 退出)...
%CLI% adb logcat
goto end

:shell
shift
if "%1"=="" (
    echo [ERROR] 请指定shell命令
    goto end
)
echo [INFO] 运行shell命令: %*
%CLI% adb shell "%*"
goto end

:screenshot
echo [INFO] 截图...
REM 需要先获取设备序列号
%CLI% adb shell "screencap -p /sdcard/screenshot.png"
%CLI% adb pull /sdcard/screenshot.png screenshot.png
goto end

:end