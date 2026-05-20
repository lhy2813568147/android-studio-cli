# Android Studio CLI 便捷启动脚本
# 使用方法: .\android-cli.ps1 [命令]

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    $Arguments
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CliDir = $ScriptDir

# 设置Android SDK环境变量
if (-not $env:ANDROID_HOME) {
    $env:ANDROID_HOME = "$env:USERPROFILE\AppData\Local\Android\Sdk"
}
$env:PATH = "$env:ANDROID_HOME\platform-tools;$env:ANDROID_HOME\emulator;$env:ANDROID_HOME\cmdline-tools\latest\bin;$env:PATH"

# 运行CLI
Set-Location $CliDir
python -m cli_anything.android_studio @Arguments