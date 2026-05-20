# Android Studio CLI Makefile

.PHONY: build test lint clean install devices avds start stop logcat all help

# 构建项目
build:
	python -m cli_anything.android_studio gradle build --variant debug

# 运行测试
test:
	python -m cli_anything.android_studio gradle test --variant debug --type unit

# 代码检查
lint:
	python -m cli_anything.android_studio gradle lint --variant debug

# 清理项目
clean:
	python -m cli_anything.android_studio gradle clean

# 安装到设备
install:
	python -m cli_anything.android_studio gradle install --variant debug

# 列出设备
devices:
	python -m cli_anything.android_studio adb devices

# 列出AVD
avds:
	python -m cli_anything.android_studio emulator list-avds

# 列出设备定义
devices-list:
	python -m cli_anything.android_studio emulator list-devices

# 列出SDK组件
images:
	python -m cli_anything.android_studio emulator list-images

# 启动模拟器
start:
	python -m cli_anything.android_studio emulator start Pixel_6_API_33

# 停止模拟器
stop:
	python -m cli_anything.android_studio emulator stop

# 查看日志
logcat:
	python -m cli_anything.android_studio adb logcat

# 截图
screenshot:
	python -m cli_anything.android_studio adb shell "screencap -p /sdcard/screenshot.png"
	python -m cli_anything.android_studio adb pull /sdcard/screenshot.png .

# 完整构建流程
all: clean build test lint install

# 帮助
help:
	@echo "可用命令:"
	@echo "  make build        - 构建项目"
	@echo "  make test         - 运行测试"
	@echo "  make lint         - 代码检查"
	@echo "  make clean        - 清理项目"
	@echo "  make install      - 安装到设备"
	@echo "  make devices      - 列出设备"
	@echo "  make avds         - 列出AVD"
	@echo "  make devices-list - 列出设备定义"
	@echo "  make images       - 列出SDK组件"
	@echo "  make start        - 启动模拟器"
	@echo "  make stop         - 停止模拟器"
	@echo "  make logcat       - 查看日志"
	@echo "  make screenshot   - 截图"
	@echo "  make all          - 完整构建流程"