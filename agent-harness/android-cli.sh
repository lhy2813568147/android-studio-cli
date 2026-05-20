#!/bin/bash
# Android Studio CLI 便捷启动脚本
# 使用方法: android-cli [命令]

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLI_DIR="$SCRIPT_DIR"

# 设置Android SDK环境变量
export ANDROID_HOME="${ANDROID_HOME:-$HOME/AppData/Local/Android/Sdk}"
export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH"

# 运行CLI
cd "$CLI_DIR"
python -m cli_anything.android_studio "$@"