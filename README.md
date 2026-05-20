# Android Studio CLI

基于 [CLI-Anything](https://github.com/HKUDS/CLI-Anything) 框架的 Android Studio CLI 工具，为 Android 开发提供命令行接口。

## ✨ 特性

- 🚀 **ADB 命令**: 设备管理、文件传输、应用安装/卸载、日志查看
- 🔨 **Gradle 命令**: 构建、测试、打包、依赖管理
- 📱 **模拟器命令**: AVD 管理、模拟器控制、截图/录屏
- 💻 **交互式 REPL**: 交互式命令行界面
- 📊 **JSON 输出**: 机器可读输出，适合 AI 代理使用
- 🔧 **开发流程集成**: Git Hooks、CI/CD、IDE 集成

## 📦 安装

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/lhy2813568147/android-studio-cli.git
cd android-studio-cli

# 安装依赖
pip install -e .
```

### 便捷脚本安装

```bash
# Linux/macOS
./install.sh

# Windows
install.bat
```

## 🚀 快速开始

### 使用便捷脚本

```bash
# Linux/macOS
./android-cli.sh adb devices
./android-cli.sh emulator list-avds
./android-cli.sh gradle build --variant debug

# Windows
android-cli.bat adb devices
android-cli.bat emulator list-avds
android-cli.bat gradle build --variant debug
```

### 使用工作流脚本

```bash
# Linux/macOS
./workflow.sh devices
./workflow.sh build debug
./workflow.sh test debug

# Windows
workflow.bat devices
workflow.bat build debug
workflow.bat test debug
```

### 使用 Makefile

```bash
make devices      # 列出设备
make avds         # 列出 AVD
make build        # 构建项目
make test         # 运行测试
make install      # 安装到设备
make all          # 完整构建流程
make help         # 显示帮助
```

## 📋 命令列表

### ADB 命令

```bash
# 列出连接的设备
android-cli adb devices

# 运行 shell 命令
android-cli adb shell "ls /sdcard"

# 安装 APK
android-cli adb install app.apk

# 卸载应用
android-cli adb uninstall com.example.app

# 文件传输
android-cli adb push local.txt /sdcard/
android-cli adb pull /sdcard/file.txt .

# 查看日志
android-cli adb logcat --lines 100
```

### 模拟器命令

```bash
# 列出可用的 AVD
android-cli emulator list-avds

# 列出可用的设备定义
android-cli emulator list-devices

# 列出已安装的 SDK 组件
android-cli emulator list-images

# 启动模拟器
android-cli emulator start Pixel_6_API_33

# 停止模拟器
android-cli emulator stop
```

### Gradle 命令

```bash
# 构建项目
android-cli gradle build --variant debug

# 运行测试
android-cli gradle test --variant debug --type unit

# 代码检查
android-cli gradle lint --variant debug

# 清理项目
android-cli gradle clean

# 安装到设备
android-cli gradle install --variant debug

# 创建 App Bundle
android-cli gradle bundle --variant release
```

## 🔧 集成方式

### Git Hooks

```bash
# 复制到项目
cp .git/hooks/pre-commit /path/to/your/project/.git/hooks/
cp .git/hooks/pre-push /path/to/your/project/.git/hooks/

# 添加执行权限
chmod +x /path/to/your/project/.git/hooks/pre-commit
chmod +x /path/to/your/project/.git/hooks/pre-push
```

- **pre-commit**: 提交前自动运行 lint 检查
- **pre-push**: 推送前自动运行测试

### CI/CD

#### GitHub Actions

复制 `.github/workflows/android.yml` 到你的项目。

#### GitLab CI

复制 `.gitlab-ci.yml` 到你的项目。

### IDE 集成

#### Android Studio

1. 打开 Android Studio
2. 进入 File → Settings → Tools → External Tools
3. 添加常用命令

#### VS Code

复制 `.vscode/tasks.json` 到你的项目。

## 📖 文档

- [README.md](README.md) - 主要文档
- [INTEGRATION.md](INTEGRATION.md) - 详细集成指南
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目总结

## 🛠️ 开发流程

### 日常开发

```bash
# 1. 启动模拟器
android-cli emulator start Pixel_6_API_33

# 2. 构建并安装
android-cli gradle build --variant debug
android-cli gradle install --variant debug

# 3. 查看日志
android-cli adb logcat

# 4. 运行测试
android-cli gradle test --variant debug --type unit
```

### 发布流程

```bash
# 1. 清理项目
android-cli gradle clean

# 2. 运行完整测试
android-cli gradle test --variant release --type unit

# 3. 代码检查
android-cli gradle lint --variant release

# 4. 构建 Release 版本
android-cli gradle build --variant release

# 5. 创建 App Bundle
android-cli gradle bundle --variant release
```

## 📁 项目结构

```
android-studio-cli/
├── agent-harness/
│   ├── cli_anything/
│   │   └── android_studio/
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       ├── android_studio_cli.py    # CLI 入口点
│   │       ├── core/
│   │       │   ├── __init__.py
│   │       │   ├── adb.py              # ADB 模块
│   │       │   ├── gradle.py           # Gradle 模块
│   │       │   └── emulator.py         # 模拟器模块
│   │       ├── skills/
│   │       │   └── SKILL.md            # AI 代理技能文件
│   │       └── tests/
│   │           ├── __init__.py
│   │           └── test_core.py        # 测试文件
│   ├── setup.py                        # 安装脚本
│   ├── android-cli.sh                  # Linux/macOS 启动脚本
│   ├── android-cli.bat                 # Windows 启动脚本
│   ├── android-cli.ps1                 # PowerShell 启动脚本
│   ├── workflow.sh                     # Linux/macOS 工作流脚本
│   ├── workflow.bat                    # Windows 工作流脚本
│   ├── Makefile                        # Makefile 构建配置
│   ├── .vscode/tasks.json              # VS Code 任务配置
│   ├── .github/workflows/              # GitHub Actions 配置
│   ├── .gitlab-ci.yml                  # GitLab CI 配置
│   └── .git/hooks/                     # Git Hooks
├── .gitignore
└── README.md
```

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目基于 Apache License 2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [CLI-Anything](https://github.com/HKUDS/CLI-Anything) - 框架基础
- [Android SDK](https://developer.android.com/studio) - Android 开发工具
- [Click](https://click.palletsprojects.com/) - Python CLI 框架