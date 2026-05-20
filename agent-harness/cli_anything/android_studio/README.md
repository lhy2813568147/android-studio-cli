# Android Studio CLI

A CLI-Anything harness for Android Studio that provides command-line access to Android development tools including ADB, Gradle, and Android Emulator.

## Features

- **ADB Commands**: Device management, file transfer, log viewing
- **Gradle Commands**: Build, test, lint, assemble, bundle
- **Emulator Commands**: AVD management, emulator control, screenshots
- **Interactive REPL**: Interactive command-line interface
- **JSON Output**: Machine-readable output for AI agents

## Installation

```bash
# Install from PyPI
pip install cli-anything-android-studio

# Or install from source
git clone https://github.com/HKUDS/CLI-Anything.git
cd CLI-Anything/android-studio-cli
pip install -e .
```

## Quick Start

```bash
# List connected devices
cli-anything-android-studio adb devices

# Build the project
cli-anything-android-studio gradle build --variant debug

# List available AVDs
cli-anything-android-studio emulator list-avds
```

## Commands

### ADB Commands

- `devices` - List connected devices
- `shell <command>` - Run shell command on device
- `install <apk>` - Install APK to device
- `uninstall <package>` - Uninstall app from device
- `push <local> <remote>` - Push file to device
- `pull <remote> <local>` - Pull file from device
- `logcat` - Get device logs

### Gradle Commands

- `build` - Build the project
- `test` - Run tests
- `clean` - Clean the project
- `tasks` - List available tasks
- `dependencies` - Show project dependencies
- `assemble` - Assemble the project
- `bundle` - Create app bundle
- `install` - Install app on device
- `lint` - Run lint checks

### Emulator Commands

- `list-avds` - List available AVDs
- `start <avd>` - Start an emulator
- `stop [avd]` - Stop emulator(s)
- `list-devices` - List available device definitions
- `list-images` - List available system images
- `create-avd <name> <image>` - Create a new AVD
- `delete-avd <name>` - Delete an AVD
- `screenshot <avd> <path>` - Take a screenshot

## JSON Output

All commands support JSON output for agent consumption:

```bash
cli-anything-android-studio --json adb devices
```

## Requirements

- Python 3.10+
- Android SDK installed
- ADB (Android Debug Bridge)
- Gradle (optional, uses gradlew if available)
- Android Emulator (optional)

## License

Apache License 2.0