#!/bin/bash
# Android Studio CLI 安装脚本
# 将CLI工具添加到PATH

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="$HOME/.local/bin"

echo "=== Android Studio CLI 安装 ==="
echo

# 创建安装目录
mkdir -p "$INSTALL_DIR"

# 复制脚本
cp "$SCRIPT_DIR/android-cli.sh" "$INSTALL_DIR/android-cli"
chmod +x "$INSTALL_DIR/android-cli"

# 检查PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "添加 $INSTALL_DIR 到 PATH..."
    
    # 添加到 .bashrc
    if [ -f "$HOME/.bashrc" ]; then
        echo "" >> "$HOME/.bashrc"
        echo "# Android Studio CLI" >> "$HOME/.bashrc"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$HOME/.bashrc"
    fi
    
    # 添加到 .zshrc
    if [ -f "$HOME/.zshrc" ]; then
        echo "" >> "$HOME/.zshrc"
        echo "# Android Studio CLI" >> "$HOME/.zshrc"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$HOME/.zshrc"
    fi
    
    echo "请运行 'source ~/.bashrc' 或重新打开终端以使更改生效"
fi

echo
echo "安装完成！"
echo
echo "使用方法:"
echo "  android-cli adb devices"
echo "  android-cli emulator list-avds"
echo "  android-cli gradle build --variant debug"
echo "  android-cli repl"