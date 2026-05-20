---
name: cli-anything-android-studio
description: "CLI-Anything harness for Android Studio — ADB, Gradle, and Emulator commands."
version: 1.0.0
author: CLI-Anything
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [android, studio, cli, adb, gradle, emulator, development]
    homepage: https://github.com/HKUDS/CLI-Anything
---

# Android Studio CLI

A CLI-Anything harness for Android Studio that provides command-line access to Android development tools including ADB, Gradle, and Android Emulator.

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

### One-shot Commands

```bash
# List connected devices
cli-anything-android-studio adb devices

# Build the project
cli-anything-android-studio gradle build --variant debug

# List available AVDs
cli-anything-android-studio emulator list-avds
```

### Interactive REPL

```bash
# Start interactive mode
cli-anything-android-studio repl

# Then use commands:
android-studio> adb devices
android-studio> gradle build debug
android-studio> emulator list-avds
```

## Commands

### ADB Commands

```bash
# List connected devices
cli-anything-android-studio adb devices

# Run shell command
cli-anything-android-studio adb shell "ls /sdcard"

# Install APK
cli-anything-android-studio adb install app.apk

# Uninstall app
cli-anything-android-studio adb uninstall com.example.app

# Push file to device
cli-anything-android-studio adb push local.txt /sdcard/remote.txt

# Pull file from device
cli-anything-android-studio adb pull /sdcard/remote.txt local.txt

# Get device logs
cli-anything-android-studio adb logcat --lines 100
```

### Gradle Commands

```bash
# Build project
cli-anything-android-studio gradle build --variant debug

# Run tests
cli-anything-android-studio gradle test --variant debug --type unit

# Clean project
cli-anything-android-studio gradle clean

# List tasks
cli-anything-android-studio gradle tasks

# Show dependencies
cli-anything-android-studio gradle dependencies

# Assemble APK
cli-anything-android-studio gradle assemble --variant debug

# Create app bundle
cli-anything-android-studio gradle bundle --variant release

# Install on device
cli-anything-android-studio gradle install --variant debug

# Run lint checks
cli-anything-android-studio gradle lint --variant debug
```

### Emulator Commands

```bash
# List available AVDs
cli-anything-android-studio emulator list-avds

# Start emulator
cli-anything-android-studio emulator start Pixel_6_API_33

# Stop emulator
cli-anything-android-studio emulator stop Pixel_6_API_33

# List available devices
cli-anything-android-studio emulator list-devices

# List available system images
cli-anything-android-studio emulator list-images

# Create new AVD
cli-anything-android-studio emulator create-avd "Pixel_6_API_33" "system-images;android-33;google_apis;x86_64"

# Delete AVD
cli-anything-android-studio emulator delete-avd "Pixel_6_API_33"

# Take screenshot
cli-anything-android-studio emulator screenshot Pixel_6_API_33 screenshot.png
```

## JSON Output

All commands support JSON output for agent consumption:

```bash
# Get devices in JSON format
cli-anything-android-studio --json adb devices

# Get build result in JSON format
cli-anything-android-studio --json gradle build --variant debug
```

## Environment Variables

- `ANDROID_HOME` or `ANDROID_SDK_ROOT`: Path to Android SDK
- Default SDK path: `~/AppData/Local/Android/Sdk` (Windows)

## Requirements

- Python 3.10+
- Android SDK installed
- ADB (Android Debug Bridge)
- Gradle (optional, uses gradlew if available)
- Android Emulator (optional)

## Examples

### Build and Install App

```bash
# Build debug APK
cli-anything-android-studio gradle build --variant debug

# Install on connected device
cli-anything-android-studio gradle install --variant debug

# Or install APK directly
cli-anything-android-studio adb install app/build/outputs/apk/debug/app-debug.apk
```

### Run Tests

```bash
# Run unit tests
cli-anything-android-studio gradle test --variant debug --type unit

# Run Android instrumented tests
cli-anything-android-studio gradle test --variant debug --type android

# Run lint checks
cli-anything-android-studio gradle lint --variant debug
```

### Manage Emulators

```bash
# List available AVDs
cli-anything-android-studio emulator list-avds

# Start emulator
cli-anything-android-studio emulator start Pixel_6_API_33

# Wait for device
cli-anything-android-studio adb wait-for-device

# Install and run app
cli-anything-android-studio gradle install --variant debug
```

### Device Management

```bash
# List connected devices
cli-anything-android-studio adb devices

# Get device properties
cli-anything-android-studio adb shell "getprop ro.product.model"

# Take screenshot
cli-anything-android-studio adb shell "screencap -p /sdcard/screenshot.png"
cli-anything-android-studio adb pull /sdcard/screenshot.png .
```

## Troubleshooting

### ADB not found

If ADB is not found, set the `ANDROID_HOME` environment variable:

```bash
export ANDROID_HOME=/path/to/android/sdk
```

### Gradle not found

If Gradle is not found, ensure `gradlew` is in your project directory or install Gradle:

```bash
# Use gradlew (recommended)
./gradlew build

# Or install Gradle
brew install gradle  # macOS
sdk install gradle   # SDKMAN
```

### Emulator not starting

If the emulator fails to start:

1. Check if the AVD exists: `cli-anything-android-studio emulator list-avds`
2. Verify system images are installed: `cli-anything-android-studio emulator list-images`
3. Check hardware acceleration (Intel HAXM or AMD Hypervisor)

## License

Apache License 2.0