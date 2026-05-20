# Android Studio CLI 项目集成配置

## 1. 在 Android 项目中使用

### 方法一: 直接使用

```bash
# 在项目根目录运行
cd /path/to/your/android/project

# 使用CLI工具
android-cli gradle build --variant debug
android-cli gradle test
android-cli gradle install
```

### 方法二: 创建项目别名

在项目根目录创建 `.android-cli` 文件:

```bash
# .android-cli
ANDROID_CLI_HOME=/path/to/android-studio-cli/agent-harness
```

然后在 `.bashrc` 或 `.zshrc` 中添加:

```bash
# Android Studio CLI 项目集成
if [ -f .android-cli ]; then
    source .android-cli
    alias android-cli="python $ANDROID_CLI_HOME/cli_anything.android_studio"
fi
```

## 2. Git Hooks 集成

### pre-commit hook

创建 `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Git pre-commit hook for Android Studio CLI

echo "运行代码检查..."

# 运行lint检查
android-cli gradle lint --variant debug

if [ $? -ne 0 ]; then
    echo "Lint检查失败，请修复后再提交"
    exit 1
fi

echo "代码检查通过"
```

### pre-push hook

创建 `.git/hooks/pre-push`:

```bash
#!/bin/bash
# Git pre-push hook for Android Studio CLI

echo "运行测试..."

# 运行单元测试
android-cli gradle test --variant debug --type unit

if [ $? -ne 0 ]; then
    echo "测试失败，请修复后再推送"
    exit 1
fi

echo "测试通过"
```

## 3. CI/CD 集成

### GitHub Actions

创建 `.github/workflows/android.yml`:

```yaml
name: Android CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 11
      uses: actions/setup-java@v3
      with:
        java-version: '11'
        distribution: 'temurin'
    
    - name: Install Android Studio CLI
      run: |
        git clone https://github.com/HKUDS/CLI-Anything.git
        cd CLI-Anything/android-studio-cli
        pip install -e .
    
    - name: Build with Gradle
      run: android-cli gradle build --variant debug
    
    - name: Run Tests
      run: android-cli gradle test --variant debug --type unit
    
    - name: Run Lint
      run: android-cli gradle lint --variant debug
```

### GitLab CI

创建 `.gitlab-ci.yml`:

```yaml
stages:
  - build
  - test
  - lint

variables:
  ANDROID_HOME: "/opt/android-sdk"

build:
  stage: build
  script:
    - android-cli gradle build --variant debug
  artifacts:
    paths:
      - app/build/outputs/

test:
  stage: test
  script:
    - android-cli gradle test --variant debug --type unit

lint:
  stage: lint
  script:
    - android-cli gradle lint --variant debug
```

## 4. IDE 集成

### Android Studio External Tools

1. 打开 Android Studio
2. 进入 File → Settings → Tools → External Tools
3. 点击 + 添加新工具

**添加 ADB Devices:**
- Name: ADB Devices
- Program: android-cli
- Arguments: adb devices
- Working directory: $ProjectFileDir$

**添加 Build Project:**
- Name: Build Project (CLI)
- Program: android-cli
- Arguments: gradle build --variant debug
- Working directory: $ProjectFileDir$

**添加 Run Tests:**
- Name: Run Tests (CLI)
- Program: android-cli
- Arguments: gradle test --variant debug --type unit
- Working directory: $ProjectFileDir$

### VS Code Tasks

创建 `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Android: Build",
      "type": "shell",
      "command": "android-cli gradle build --variant debug",
      "group": "build",
      "problemMatcher": []
    },
    {
      "label": "Android: Test",
      "type": "shell",
      "command": "android-cli gradle test --variant debug --type unit",
      "group": "test",
      "problemMatcher": []
    },
    {
      "label": "Android: Lint",
      "type": "shell",
      "command": "android-cli gradle lint --variant debug",
      "group": "test",
      "problemMatcher": []
    },
    {
      "label": "Android: Clean",
      "type": "shell",
      "command": "android-cli gradle clean",
      "group": "build",
      "problemMatcher": []
    },
    {
      "label": "Android: Install",
      "type": "shell",
      "command": "android-cli gradle install --variant debug",
      "group": "build",
      "problemMatcher": []
    }
  ]
}
```

## 5. Makefile 集成

在项目根目录创建 `Makefile`:

```makefile
# Android Studio CLI Makefile

.PHONY: build test lint clean install devices avds

# 构建项目
build:
	android-cli gradle build --variant debug

# 运行测试
test:
	android-cli gradle test --variant debug --type unit

# 代码检查
lint:
	android-cli gradle lint --variant debug

# 清理项目
clean:
	android-cli gradle clean

# 安装到设备
install:
	android-cli gradle install --variant debug

# 列出设备
devices:
	android-cli adb devices

# 列出AVD
avds:
	android-cli emulator list-avds

# 启动模拟器
start:
	android-cli emulator start Pixel_6_API_33

# 停止模拟器
stop:
	android-cli emulator stop

# 查看日志
logcat:
	android-cli adb logcat

# 完整构建流程
all: clean build test lint install

# 帮助
help:
	@echo "可用命令:"
	@echo "  make build     - 构建项目"
	@echo "  make test      - 运行测试"
	@echo "  make lint      - 代码检查"
	@echo "  make clean     - 清理项目"
	@echo "  make install   - 安装到设备"
	@echo "  make devices   - 列出设备"
	@echo "  make avds      - 列出AVD"
	@echo "  make start     - 启动模拟器"
	@echo "  make stop      - 停止模拟器"
	@echo "  make logcat    - 查看日志"
	@echo "  make all       - 完整构建流程"
```

## 6. 常用开发流程

### 日常开发流程

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

### 调试流程

```bash
# 1. 列出连接的设备
android-cli adb devices

# 2. 安装调试版本
android-cli gradle install --variant debug

# 3. 查看实时日志
android-cli adb logcat

# 4. 截图
android-cli emulator screenshot Pixel_6_API_33 debug.png
```