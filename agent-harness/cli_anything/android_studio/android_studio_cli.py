#!/usr/bin/env python3
"""Android Studio CLI — A command-line interface for Android development.

This CLI provides comprehensive Android development capabilities using
ADB, Gradle, and Android Emulator as the backend engines.

Usage:
    # One-shot commands
    python3 -m cli_anything.android_studio adb devices
    python3 -m cli_anything.android_studio gradle build --variant debug
    python3 -m cli_anything.android_studio emulator list-avds

    # Interactive REPL
    python3 -m cli_anything.android_studio repl
"""

import sys
import os
import json
import click
from typing import Optional

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli_anything.android_studio.core.adb import ADB
from cli_anything.android_studio.core.gradle import Gradle
from cli_anything.android_studio.core.emulator import Emulator

# Global state
_json_output = False
_repl_mode = False


def output(data, message: str = ""):
    """Output data in JSON or human-readable format."""
    if _json_output:
        click.echo(json.dumps(data, indent=2, default=str))
    else:
        if message:
            click.echo(message)
        if isinstance(data, dict):
            _print_dict(data)
        elif isinstance(data, list):
            _print_list(data)
        else:
            click.echo(str(data))


def _print_dict(d: dict, indent: int = 0):
    """Print dictionary in human-readable format."""
    prefix = "  " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            click.echo(f"{prefix}{k}:")
            _print_dict(v, indent + 1)
        elif isinstance(v, list):
            click.echo(f"{prefix}{k}:")
            _print_list(v, indent + 1)
        else:
            click.echo(f"{prefix}{k}: {v}")


def _print_list(items: list, indent: int = 0):
    """Print list in human-readable format."""
    prefix = "  " * indent
    for i, item in enumerate(items):
        if isinstance(item, dict):
            click.echo(f"{prefix}[{i}]")
            _print_dict(item, indent + 1)
        else:
            click.echo(f"{prefix}- {item}")


def handle_error(func):
    """Decorator to handle errors gracefully."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            if _json_output:
                click.echo(json.dumps({"error": str(e), "type": "file_not_found"}))
            else:
                click.echo(f"Error: {e}", err=True)
            if not _repl_mode:
                sys.exit(1)
        except (ValueError, IndexError, RuntimeError) as e:
            if _json_output:
                click.echo(json.dumps({"error": str(e), "type": type(e).__name__}))
            else:
                click.echo(f"Error: {e}", err=True)
            if not _repl_mode:
                sys.exit(1)
        except subprocess.CalledProcessError as e:
            if _json_output:
                click.echo(json.dumps({
                    "error": e.stderr or str(e),
                    "type": "subprocess_error",
                    "returncode": e.returncode
                }))
            else:
                click.echo(f"Error: {e.stderr or e}", err=True)
            if not _repl_mode:
                sys.exit(1)
    return wrapper


@click.group(invoke_without_command=True)
@click.option("--json", "json_output", is_flag=True, help="Output in JSON format")
@click.option("--sdk-root", help="Android SDK root path")
@click.pass_context
def cli(ctx, json_output: bool, sdk_root: Optional[str]):
    """Android Studio CLI — A command-line interface for Android development."""
    global _json_output
    _json_output = json_output
    
    ctx.ensure_object(dict)
    ctx.obj["sdk_root"] = sdk_root
    
    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


@cli.command()
@click.option("--project-dir", help="Project directory")
@click.pass_context
def repl(ctx, project_dir: Optional[str]):
    """Start interactive REPL mode."""
    global _repl_mode
    _repl_mode = True
    
    click.echo("Android Studio CLI REPL")
    click.echo("Type 'help' for available commands, 'exit' to quit")
    click.echo()
    
    adb = ADB()
    gradle = Gradle(project_dir=project_dir or os.getcwd())
    emulator = Emulator()
    
    while True:
        try:
            line = input("android-studio> ").strip()
            if not line:
                continue
            
            if line in ("exit", "quit", "q"):
                break
            
            if line == "help":
                click.echo("""
Available commands:
  adb <command>       - ADB commands
  gradle <command>    - Gradle commands  
  emulator <command>  - Emulator commands
  help                - Show this help
  exit                - Exit REPL
""")
                continue
            
            parts = line.split()
            command = parts[0]
            args = parts[1:]
            
            if command == "adb":
                _handle_adb_command(adb, args)
            elif command == "gradle":
                _handle_gradle_command(gradle, args)
            elif command == "emulator":
                _handle_emulator_command(emulator, args)
            else:
                click.echo(f"Unknown command: {command}")
        
        except KeyboardInterrupt:
            click.echo()
            continue
        except EOFError:
            break
    
    click.echo("Goodbye!")


def _handle_adb_command(adb: ADB, args: list):
    """Handle ADB commands in REPL."""
    if not args:
        click.echo("Usage: adb <command> [args...]")
        return
    
    command = args[0]
    command_args = args[1:]
    
    if command == "devices":
        devices = adb.devices()
        output(devices, "Connected devices:")
    elif command == "shell":
        if not command_args:
            click.echo("Usage: adb shell <command>")
            return
        result = adb.shell(" ".join(command_args))
        click.echo(result)
    elif command == "install":
        if not command_args:
            click.echo("Usage: adb install <apk_path>")
            return
        result = adb.install(command_args[0])
        click.echo(result)
    elif command == "uninstall":
        if not command_args:
            click.echo("Usage: adb uninstall <package>")
            return
        result = adb.uninstall(command_args[0])
        click.echo(result)
    elif command == "push":
        if len(command_args) < 2:
            click.echo("Usage: adb push <local_path> <remote_path>")
            return
        result = adb.push(command_args[0], command_args[1])
        click.echo(result)
    elif command == "pull":
        if len(command_args) < 2:
            click.echo("Usage: adb pull <remote_path> <local_path>")
            return
        result = adb.pull(command_args[0], command_args[1])
        click.echo(result)
    elif command == "logcat":
        result = adb.logcat(" ".join(command_args) if command_args else None)
        click.echo(result)
    else:
        click.echo(f"Unknown ADB command: {command}")


def _handle_gradle_command(gradle: Gradle, args: list):
    """Handle Gradle commands in REPL."""
    if not args:
        click.echo("Usage: gradle <command> [args...]")
        return
    
    command = args[0]
    command_args = args[1:]
    
    if command == "build":
        variant = command_args[0] if command_args else None
        result = gradle.build(variant)
        click.echo(result)
    elif command == "test":
        variant = command_args[0] if command_args else None
        result = gradle.test(variant)
        click.echo(result)
    elif command == "clean":
        result = gradle.clean()
        click.echo(result)
    elif command == "tasks":
        result = gradle.tasks()
        click.echo(result)
    elif command == "dependencies":
        result = gradle.dependencies()
        click.echo(result)
    elif command == "assemble":
        variant = command_args[0] if command_args else None
        result = gradle.assemble(variant)
        click.echo(result)
    elif command == "bundle":
        variant = command_args[0] if command_args else None
        result = gradle.bundle(variant)
        click.echo(result)
    elif command == "install":
        variant = command_args[0] if command_args else None
        result = gradle.install(variant)
        click.echo(result)
    elif command == "lint":
        variant = command_args[0] if command_args else None
        result = gradle.lint(variant)
        click.echo(result)
    else:
        click.echo(f"Unknown Gradle command: {command}")


def _handle_emulator_command(emulator: Emulator, args: list):
    """Handle Emulator commands in REPL."""
    if not args:
        click.echo("Usage: emulator <command> [args...]")
        return
    
    command = args[0]
    command_args = args[1:]
    
    if command == "list-avds":
        avds = emulator.list_avds()
        output(avds, "Available AVDs:")
    elif command == "start":
        if not command_args:
            click.echo("Usage: emulator start <avd_name>")
            return
        click.echo(f"Starting emulator: {command_args[0]}")
        emulator.start(command_args[0])
    elif command == "stop":
        avd_name = command_args[0] if command_args else None
        result = emulator.stop(avd_name)
        click.echo(result)
    elif command == "list-devices":
        devices = emulator.list_devices()
        output(devices, "Available devices:")
    elif command == "list-images":
        images = emulator.list_system_images()
        output(images, "Available system images:")
    else:
        click.echo(f"Unknown Emulator command: {command}")


# ADB commands
@cli.group()
def adb():
    """ADB (Android Debug Bridge) commands."""
    pass


@adb.command("devices")
def adb_devices():
    """List connected devices."""
    adb = ADB()
    devices = adb.devices()
    output(devices, "Connected devices:")


@adb.command("shell")
@click.argument("command", nargs=-1, required=True)
def adb_shell(command):
    """Run shell command on device."""
    adb = ADB()
    result = adb.shell(" ".join(command))
    click.echo(result)


@adb.command("install")
@click.argument("apk_path")
@click.option("--device", "-s", help="Device serial number")
def adb_install(apk_path, device):
    """Install APK to device."""
    adb = ADB()
    result = adb.install(apk_path, device)
    click.echo(result)


@adb.command("uninstall")
@click.argument("package")
@click.option("--device", "-s", help="Device serial number")
@click.option("--keep-data", "-k", is_flag=True, help="Keep app data")
def adb_uninstall(package, device, keep_data):
    """Uninstall app from device."""
    adb = ADB()
    result = adb.uninstall(package, device, keep_data)
    click.echo(result)


@adb.command("push")
@click.argument("local_path")
@click.argument("remote_path")
@click.option("--device", "-s", help="Device serial number")
def adb_push(local_path, remote_path, device):
    """Push file to device."""
    adb = ADB()
    result = adb.push(local_path, remote_path, device)
    click.echo(result)


@adb.command("pull")
@click.argument("remote_path")
@click.argument("local_path")
@click.option("--device", "-s", help="Device serial number")
def adb_pull(remote_path, local_path, device):
    """Pull file from device."""
    adb = ADB()
    result = adb.pull(remote_path, local_path, device)
    click.echo(result)


@adb.command("logcat")
@click.option("--filter", "-f", help="Log filter expression")
@click.option("--device", "-s", help="Device serial number")
@click.option("--lines", "-n", type=int, help="Number of lines to retrieve")
def adb_logcat(filter, device, lines):
    """Get device logs."""
    adb = ADB()
    result = adb.logcat(filter, device, lines)
    click.echo(result)


# Gradle commands
@cli.group()
def gradle():
    """Gradle build commands."""
    pass


@gradle.command("build")
@click.option("--variant", "-v", help="Build variant (debug, release)")
@click.option("--clean", "-c", is_flag=True, help="Clean before building")
@click.option("--project-dir", "-p", help="Project directory")
def gradle_build(variant, clean, project_dir):
    """Build the project."""
    gradle = Gradle(project_dir=project_dir)
    result = gradle.build(variant, clean)
    click.echo(result)


@gradle.command("test")
@click.option("--variant", "-v", help="Build variant")
@click.option("--type", "-t", "test_type", default="unit", 
              type=click.Choice(["unit", "android", "lint"]),
              help="Test type")
@click.option("--project-dir", "-p", help="Project directory")
def gradle_test(variant, test_type, project_dir):
    """Run tests."""
    gradle = Gradle(project_dir=project_dir)
    result = gradle.test(variant, test_type)
    click.echo(result)


@gradle.command("clean")
@click.option("--project-dir", "-p", help="Project directory")
def gradle_clean(project_dir):
    """Clean the project."""
    gradle = Gradle(project_dir=project_dir)
    result = gradle.clean()
    click.echo(result)


@gradle.command("tasks")
@click.option("--all", "-a", is_flag=True, help="Show all tasks")
@click.option("--project-dir", "-p", help="Project directory")
def gradle_tasks(all, project_dir):
    """List available tasks."""
    gradle = Gradle(project_dir=project_dir)
    result = gradle.tasks(all)
    click.echo(result)


@gradle.command("dependencies")
@click.option("--configuration", "-c", help="Configuration name")
@click.option("--project-dir", "-p", help="Project directory")
def gradle_dependencies(configuration, project_dir):
    """Show project dependencies."""
    gradle = Gradle(project_dir=project_dir)
    result = gradle.dependencies(configuration)
    click.echo(result)


@gradle.command("assemble")
@click.option("--variant", "-v", help="Build variant")
@click.option("--project-dir", "-p", help="Project directory")
def gradle_assemble(variant, project_dir):
    """Assemble the project."""
    gradle = Gradle(project_dir=project_dir)
    result = gradle.assemble(variant)
    click.echo(result)


@gradle.command("bundle")
@click.option("--variant", "-v", help="Build variant")
@click.option("--project-dir", "-p", help="Project directory")
def gradle_bundle(variant, project_dir):
    """Create app bundle."""
    gradle = Gradle(project_dir=project_dir)
    result = gradle.bundle(variant)
    click.echo(result)


@gradle.command("install")
@click.option("--variant", "-v", help="Build variant")
@click.option("--device", "-s", help="Device serial number")
@click.option("--project-dir", "-p", help="Project directory")
def gradle_install(variant, device, project_dir):
    """Install app on device."""
    gradle = Gradle(project_dir=project_dir)
    result = gradle.install(variant, device)
    click.echo(result)


@gradle.command("lint")
@click.option("--variant", "-v", help="Build variant")
@click.option("--project-dir", "-p", help="Project directory")
def gradle_lint(variant, project_dir):
    """Run lint checks."""
    gradle = Gradle(project_dir=project_dir)
    result = gradle.lint(variant)
    click.echo(result)


# Emulator commands
@cli.group()
def emulator():
    """Android Emulator commands."""
    pass


@emulator.command("list-avds")
def emulator_list_avds():
    """List available AVDs."""
    emulator = Emulator()
    avds = emulator.list_avds()
    output(avds, "Available AVDs:")


@emulator.command("start")
@click.argument("avd_name")
def emulator_start(avd_name):
    """Start an emulator."""
    emulator = Emulator()
    click.echo(f"Starting emulator: {avd_name}")
    emulator.start(avd_name)


@emulator.command("stop")
@click.argument("avd_name", required=False)
def emulator_stop(avd_name):
    """Stop emulator(s)."""
    emulator = Emulator()
    result = emulator.stop(avd_name)
    click.echo(result)


@emulator.command("list-devices")
def emulator_list_devices():
    """List available device definitions."""
    emulator = Emulator()
    devices = emulator.list_devices()
    output(devices, "Available devices:")


@emulator.command("list-images")
def emulator_list_images():
    """List available system images."""
    emulator = Emulator()
    images = emulator.list_system_images()
    output(images, "Available system images:")


@emulator.command("create-avd")
@click.argument("name")
@click.argument("system_image")
@click.option("--device", "-d", help="Device definition")
@click.option("--force", "-f", is_flag=True, help="Force overwrite")
def emulator_create_avd(name, system_image, device, force):
    """Create a new AVD."""
    emulator = Emulator()
    result = emulator.create_avd(name, system_image, device, force)
    click.echo(result)


@emulator.command("delete-avd")
@click.argument("name")
def emulator_delete_avd(name):
    """Delete an AVD."""
    emulator = Emulator()
    result = emulator.delete_avd(name)
    click.echo(result)


@emulator.command("screenshot")
@click.argument("avd_name")
@click.argument("output_path")
def emulator_screenshot(avd_name, output_path):
    """Take a screenshot."""
    emulator = Emulator()
    result = emulator.screenshot(avd_name, output_path)
    click.echo(result)


if __name__ == "__main__":
    cli()