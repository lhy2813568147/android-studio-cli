# Android Studio CLI 集成指南

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/HKUDS/CLI-Anything.git
cd CLI-Anything/android-studio-cli

# 安装依赖
pip install -e .
```

### 使用

```bash
# 列出设备
android-cli adb devices

# 列出AVD
android-cli emulator list-avds

# 构建项目
android-cli gradle build --variant debug

# 运行测试
android-cli gradle test --variant debug --type unit
```

## 集成方式

### 1. 便捷脚本

```bash
# Linux/macOS
./android-cli.sh adb devices

# Windows
android-cli.bat adb devices

# PowerShell
.\android-cli.ps1 adb devices
```

### 2. 工作流脚本

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

### 3. Makefile

```bash
make devices
make avds
make build
make test
make install
make all
```

### 4. Git Hooks

```bash
# 复制hooks到项目
cp .git/hooks/pre-commit /path/to/your/project/.git/hooks/
cp .git/hooks/pre-push /path/to/your/project/.git/hooks/

# 添加执行权限
chmod +x /path/to/your/project/.git/hooks/pre-commit
chmod +x /path/to/your/project/.git/hooks/pre-push
```

### 5. CI/CD

#### GitHub Actions

复制 `.github/workflows/android.yml` 到你的项目。

#### GitLab CI

复制 `.gitlab-ci.yml` 到你的项目。

### 6. IDE集成

#### Android Studio

1. 打开 Android Studio
2. 进入 File → Settings → Tools → External Tools
3. 添加以下工具：
   - ADB Devices: `android-cli adb devices`
   - Build Project: `android-cli gradle build --variant debug`
   - Run Tests: `android-cli gradle test --variant debug --type unit`

#### VS Code

复制 `.vscode/tasks.json` 到你的项目。

## 常用命令

### ADB命令

```bash
# 列出设备
android-cli adb devices

# 安装应用
android-cli adb install app.apk

# 卸载应用
android-cli adb uninstall com.example.app

# 查看日志
android-cli adb logcat

# 文件传输
android-cli adb push local.txt /sdcard/
android-cli adb pull /sdcard/file.txt .
```

### 模拟器命令

```bash
# 列出AVD
android-cli emulator list-avds

# 列出设备定义
android-cli emulator list-devices

# 列出SDK组件
android-cli emulator list-images

# 启动模拟器
android-cli emulator start Pixel_6_API_33

# 停止模拟器
android-cli emulator stop
```

### Gradle命令

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

# 创建App Bundle
android-cli gradle bundle --variant release
```

## 开发流程

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

# 4. 构建Release版本
android-cli gradle build --variant release

# 5. 创建App Bundle
android-cli gradle bundle --variant release
```

## 文件结构

```
android-studio-cli/
├── android-cli.sh          # Linux/macOS启动脚本
├── android-cli.bat         # Windows启动脚本
├── android-cli.ps1         # PowerShell启动脚本
├── workflow.sh             # Linux/macOS工作流脚本
├── workflow.bat            # Windows工作流脚本
├── Makefile                # Makefile
├── .vscode/tasks.json      # VS Code配置
├── .github/workflows/      # GitHub Actions
├── .gitlab-ci.yml          # GitLab CI
├── .git/hooks/             # Git Hooks
├── INTEGRATION.md          # 集成文档
└── README.md               # 本文档
```

## 许可证

Apache License 2.0