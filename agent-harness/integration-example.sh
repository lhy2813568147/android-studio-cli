#!/bin/bash
# Android Studio CLI 集成示例

echo "=== Android Studio CLI 集成示例 ==="
echo

# 1. 使用便捷脚本
echo "1. 使用便捷脚本:"
echo "   ./android-cli.sh adb devices"
echo "   ./android-cli.sh emulator list-avds"
echo

# 2. 使用工作流脚本
echo "2. 使用工作流脚本:"
echo "   ./workflow.sh devices"
echo "   ./workflow.sh avds"
echo "   ./workflow.sh build debug"
echo "   ./workflow.sh test debug"
echo "   ./workflow.sh install debug"
echo

# 3. 使用Makefile
echo "3. 使用Makefile:"
echo "   make devices"
echo "   make avds"
echo "   make build"
echo "   make test"
echo "   make install"
echo "   make all"
echo

# 4. Git Hooks
echo "4. Git Hooks:"
echo "   pre-commit: 运行lint检查"
echo "   pre-push: 运行单元测试"
echo

# 5. CI/CD
echo "5. CI/CD:"
echo "   GitHub Actions: .github/workflows/android.yml"
echo "   GitLab CI: .gitlab-ci.yml"
echo

# 6. IDE集成
echo "6. IDE集成:"
echo "   Android Studio: External Tools"
echo "   VS Code: .vscode/tasks.json"
echo

echo "=== 示例完成 ==="