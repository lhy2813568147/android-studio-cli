#!/bin/bash
# Android 开发工作流脚本
# 使用方法: ./workflow.sh [命令]

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLI="python -m cli_anything.android_studio"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助
show_help() {
    echo "Android 开发工作流脚本"
    echo
    echo "使用方法: $0 [命令]"
    echo
    echo "可用命令:"
    echo "  devices          - 列出连接的设备"
    echo "  avds             - 列出可用的AVD"
    echo "  start <avd>      - 启动模拟器"
    echo "  stop <avd>       - 停止模拟器"
    echo "  build [variant]  - 构建项目"
    echo "  test [variant]   - 运行测试"
    echo "  install [variant]- 安装到设备"
    echo "  clean            - 清理项目"
    echo "  lint             - 代码检查"
    echo "  logcat           - 查看日志"
    echo "  shell <command>  - 运行shell命令"
    echo "  screenshot       - 截图"
    echo "  help             - 显示此帮助"
}

# 列出设备
cmd_devices() {
    print_info "列出连接的设备..."
    $CLI adb devices
}

# 列出AVD
cmd_avds() {
    print_info "列出可用的AVD..."
    $CLI emulator list-avds
}

# 启动模拟器
cmd_start() {
    if [ -z "$1" ]; then
        print_error "请指定AVD名称"
        echo "可用的AVD:"
        $CLI emulator list-avds
        return 1
    fi
    
    print_info "启动模拟器: $1"
    $CLI emulator start "$1"
}

# 停止模拟器
cmd_stop() {
    if [ -z "$1" ]; then
        print_warn "停止所有模拟器..."
        $CLI emulator stop
    else
        print_info "停止模拟器: $1"
        $CLI emulator stop "$1"
    fi
}

# 构建项目
cmd_build() {
    local variant=${1:-debug}
    print_info "构建项目 (variant: $variant)..."
    $CLI gradle build --variant "$variant"
}

# 运行测试
cmd_test() {
    local variant=${1:-debug}
    print_info "运行测试 (variant: $variant)..."
    $CLI gradle test --variant "$variant" --type unit
}

# 安装到设备
cmd_install() {
    local variant=${1:-debug}
    print_info "安装到设备 (variant: $variant)..."
    $CLI gradle install --variant "$variant"
}

# 清理项目
cmd_clean() {
    print_info "清理项目..."
    $CLI gradle clean
}

# 代码检查
cmd_lint() {
    local variant=${1:-debug}
    print_info "运行代码检查 (variant: $variant)..."
    $CLI gradle lint --variant "$variant"
}

# 查看日志
cmd_logcat() {
    print_info "查看设备日志 (按 Ctrl+C 退出)..."
    $CLI adb logcat
}

# 运行shell命令
cmd_shell() {
    if [ -z "$1" ]; then
        print_error "请指定shell命令"
        return 1
    fi
    
    print_info "运行shell命令: $*"
    $CLI adb shell "$*"
}

# 截图
cmd_screenshot() {
    local filename="screenshot_$(date +%Y%m%d_%H%M%S).png"
    print_info "截图保存到: $filename"
    # 需要先获取设备序列号
    $CLI adb shell "screencap -p /sdcard/$filename"
    $CLI adb pull "/sdcard/$filename" "$filename"
}

# 主函数
main() {
    cd "$SCRIPT_DIR"
    
    case "$1" in
        devices)
            cmd_devices
            ;;
        avds)
            cmd_avds
            ;;
        start)
            cmd_start "$2"
            ;;
        stop)
            cmd_stop "$2"
            ;;
        build)
            cmd_build "$2"
            ;;
        test)
            cmd_test "$2"
            ;;
        install)
            cmd_install "$2"
            ;;
        clean)
            cmd_clean
            ;;
        lint)
            cmd_lint "$2"
            ;;
        logcat)
            cmd_logcat
            ;;
        shell)
            shift
            cmd_shell "$@"
            ;;
        screenshot)
            cmd_screenshot
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            show_help
            ;;
    esac
}

main "$@"