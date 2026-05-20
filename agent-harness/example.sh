#!/bin/bash
# Android Studio CLI 使用示例

echo "=== Android Studio CLI 使用示例 ==="
echo

# 1. 列出连接的设备
echo "1. 列出连接的设备:"
python -m cli_anything.android_studio adb devices
echo

# 2. 列出可用的AVD
echo "2. 列出可用的AVD:"
python -m cli_anything.android_studio emulator list-avds
echo

# 3. 列出可用的设备定义
echo "3. 列出可用的设备定义:"
python -m cli_anything.android_studio emulator list-devices
echo

# 4. 列出已安装的SDK组件
echo "4. 列出已安装的SDK组件:"
python -m cli_anything.android_studio emulator list-images
echo

# 5. JSON输出示例
echo "5. JSON输出示例:"
python -m cli_anything.android_studio --json adb devices
echo

# 6. 交互式REPL模式
echo "6. 交互式REPL模式:"
echo "启动交互式模式: python -m cli_anything.android_studio repl"
echo

echo "=== 示例完成 ==="