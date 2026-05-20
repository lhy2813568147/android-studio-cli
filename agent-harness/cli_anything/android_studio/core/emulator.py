"""Emulator module for Android Studio CLI."""

import os
import subprocess
import json
import time
from typing import Optional, List, Dict, Any


class Emulator:
    """Wrapper for Android Emulator commands."""
    
    def __init__(self, emulator_path: Optional[str] = None):
        """Initialize Emulator with optional custom path.
        
        Args:
            emulator_path: Custom path to emulator executable. If None, uses Android SDK default.
        """
        if emulator_path:
            self.emulator_path = emulator_path
        else:
            # Try to find emulator in Android SDK
            sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
            if not sdk_root:
                # Default Windows path
                sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
            
            self.emulator_path = os.path.join(sdk_root, "emulator", "emulator.exe")
            if not os.path.exists(self.emulator_path):
                # Try alternative path
                self.emulator_path = os.path.join(sdk_root, "emulator", "emulator")
    
    def _run_command(self, args: List[str], check: bool = True, 
                    timeout: Optional[int] = None) -> subprocess.CompletedProcess:
        """Run an emulator command.
        
        Args:
            args: Command arguments
            check: Whether to raise exception on non-zero exit
            timeout: Command timeout in seconds
            
        Returns:
            CompletedProcess instance
        """
        cmd = [self.emulator_path] + args
        return subprocess.run(cmd, capture_output=True, text=True, check=check, 
                            timeout=timeout)
    
    def list_avds(self) -> List[str]:
        """List available Android Virtual Devices (AVDs).
        
        Returns:
            List of AVD names
        """
        result = self._run_command(["-list-avds"])
        avds = [line.strip() for line in result.stdout.split("\n") if line.strip()]
        return avds
    
    def start(self, avd_name: str, options: Optional[Dict[str, Any]] = None) -> subprocess.Popen:
        """Start an emulator.
        
        Args:
            avd_name: AVD name
            options: Additional emulator options
            
        Returns:
            Popen instance for the emulator process
        """
        args = ["-avd", avd_name]
        
        if options:
            for key, value in options.items():
                if value is True:
                    args.append(f"-{key}")
                elif value is not False:
                    args.extend([f"-{key}", str(value)])
        
        cmd = [self.emulator_path] + args
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def stop(self, avd_name: Optional[str] = None) -> str:
        """Stop emulator(s).
        
        Args:
            avd_name: AVD name (optional). If None, stops all emulators.
            
        Returns:
            Stop result
        """
        # Use ADB to stop emulator
        sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        if not sdk_root:
            sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
        
        adb_path = os.path.join(sdk_root, "platform-tools", "adb.exe")
        if not os.path.exists(adb_path):
            adb_path = os.path.join(sdk_root, "platform-tools", "adb")
        
        if avd_name:
            # Find emulator serial for this AVD
            result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
            for line in result.stdout.split("\n"):
                if "emulator" in line and avd_name in line:
                    serial = line.split()[0]
                    subprocess.run([adb_path, "-s", serial, "emu", "kill"], 
                                 capture_output=True, text=True)
                    return f"Stopped emulator: {avd_name}"
            return f"Emulator not found: {avd_name}"
        else:
            # Stop all emulators
            subprocess.run([adb_path, "emu", "kill"], capture_output=True, text=True)
            return "Stopped all emulators"
    
    def create_avd(self, name: str, system_image: str, 
                   device: Optional[str] = None, 
                   force: bool = False) -> str:
        """Create a new AVD.
        
        Args:
            name: AVD name
            system_image: System image (e.g., 'system-images;android-30;google_apis;x86_64')
            device: Device definition (optional)
            force: Force overwrite if exists
            
        Returns:
            Creation result
        """
        # Use avdmanager
        sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        if not sdk_root:
            sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
        
        avdmanager_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin", "avdmanager.bat")
        if not os.path.exists(avdmanager_path):
            avdmanager_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin", "avdmanager")
        
        args = [avdmanager_path, "create", "avd", "-n", name, "-k", system_image]
        
        if device:
            args.extend(["-d", device])
        if force:
            args.append("--force")
        
        result = subprocess.run(args, capture_output=True, text=True, input="no\n")
        return result.stdout
    
    def delete_avd(self, name: str) -> str:
        """Delete an AVD.
        
        Args:
            name: AVD name
            
        Returns:
            Deletion result
        """
        # Use avdmanager
        sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        if not sdk_root:
            sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
        
        avdmanager_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin", "avdmanager.bat")
        if not os.path.exists(avdmanager_path):
            avdmanager_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin", "avdmanager")
        
        args = [avdmanager_path, "delete", "avd", "-n", name]
        result = subprocess.run(args, capture_output=True, text=True)
        return result.stdout
    
    def list_devices(self) -> List[Dict[str, str]]:
        """List available device definitions.
        
        Returns:
            List of device dictionaries
        """
        # Use avdmanager
        sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        if not sdk_root:
            sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
        
        avdmanager_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin", "avdmanager.bat")
        if not os.path.exists(avdmanager_path):
            avdmanager_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin", "avdmanager")
        
        args = [avdmanager_path, "list", "device"]
        result = subprocess.run(args, capture_output=True, text=True)
        
        devices = []
        current_device = {}
        
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line.startswith("id:"):
                if current_device:
                    devices.append(current_device)
                current_device = {"id": line.split(":")[1].strip()}
            elif line.startswith("Name:"):
                current_device["name"] = line.split(":")[1].strip()
            elif line.startswith("OEM:"):
                current_device["oem"] = line.split(":")[1].strip()
            elif line.startswith("Tag:"):
                current_device["tag"] = line.split(":")[1].strip()
        
        if current_device:
            devices.append(current_device)
        
        return devices
    
    def list_system_images(self) -> List[Dict[str, str]]:
        """List available system images.
        
        Returns:
            List of system image dictionaries
        """
        # Use sdkmanager
        sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        if not sdk_root:
            sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
        
        sdkmanager_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin", "sdkmanager.bat")
        if not os.path.exists(sdkmanager_path):
            sdkmanager_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin", "sdkmanager")
        
        args = [sdkmanager_path, "--list_installed"]
        result = subprocess.run(args, capture_output=True, text=True)
        
        images = []
        in_images = False
        
        for line in result.stdout.split("\n"):
            if "Installed packages:" in line:
                in_images = True
                continue
            if in_images and line.strip():
                if "Path" in line or "-------" in line:
                    continue
                parts = line.split("|")
                if len(parts) >= 2:
                    path = parts[0].strip()
                    version = parts[1].strip()
                    description = parts[2].strip() if len(parts) > 2 else ""
                    if path:
                        images.append({
                            "path": path,
                            "version": version,
                            "description": description
                        })
        
        return images
    
    def screenshot(self, avd_name: str, output_path: str) -> str:
        """Take a screenshot of the emulator.
        
        Args:
            avd_name: AVD name
            output_path: Output file path
            
        Returns:
            Screenshot result
        """
        # Use ADB
        sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        if not sdk_root:
            sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
        
        adb_path = os.path.join(sdk_root, "platform-tools", "adb.exe")
        if not os.path.exists(adb_path):
            adb_path = os.path.join(sdk_root, "platform-tools", "adb")
        
        # Find emulator serial for this AVD
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "emulator" in line and avd_name in line:
                serial = line.split()[0]
                subprocess.run([adb_path, "-s", serial, "shell", "screencap", "-p", "/sdcard/screenshot.png"],
                             capture_output=True, text=True)
                subprocess.run([adb_path, "-s", serial, "pull", "/sdcard/screenshot.png", output_path],
                             capture_output=True, text=True)
                return f"Screenshot saved to: {output_path}"
        
        return f"Emulator not found: {avd_name}"
    
    def record_video(self, avd_name: str, output_path: str, 
                     time_limit: Optional[int] = None) -> str:
        """Record video from the emulator.
        
        Args:
            avd_name: AVD name
            output_path: Output file path
            time_limit: Time limit in seconds (optional)
            
        Returns:
            Recording result
        """
        # Use ADB
        sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        if not sdk_root:
            sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
        
        adb_path = os.path.join(sdk_root, "platform-tools", "adb.exe")
        if not os.path.exists(adb_path):
            adb_path = os.path.join(sdk_root, "platform-tools", "adb")
        
        # Find emulator serial for this AVD
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "emulator" in line and avd_name in line:
                serial = line.split()[0]
                args = [adb_path, "-s", serial, "shell", "screenrecord"]
                if time_limit:
                    args.extend(["--time-limit", str(time_limit)])
                args.append("/sdcard/video.mp4")
                
                subprocess.run(args, capture_output=True, text=True)
                subprocess.run([adb_path, "-s", serial, "pull", "/sdcard/video.mp4", output_path],
                             capture_output=True, text=True)
                return f"Video saved to: {output_path}"
        
        return f"Emulator not found: {avd_name}"
    
    def install_apk(self, avd_name: str, apk_path: str) -> str:
        """Install an APK on the emulator.
        
        Args:
            avd_name: AVD name
            apk_path: Path to APK file
            
        Returns:
            Installation result
        """
        # Use ADB
        sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        if not sdk_root:
            sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
        
        adb_path = os.path.join(sdk_root, "platform-tools", "adb.exe")
        if not os.path.exists(adb_path):
            adb_path = os.path.join(sdk_root, "platform-tools", "adb")
        
        # Find emulator serial for this AVD
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "emulator" in line and avd_name in line:
                serial = line.split()[0]
                result = subprocess.run([adb_path, "-s", serial, "install", apk_path],
                                       capture_output=True, text=True)
                return result.stdout
        
        return f"Emulator not found: {avd_name}"
    
    def get_prop(self, avd_name: str, prop_name: str) -> str:
        """Get emulator property.
        
        Args:
            avd_name: AVD name
            prop_name: Property name
            
        Returns:
            Property value
        """
        # Use ADB
        sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        if not sdk_root:
            sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
        
        adb_path = os.path.join(sdk_root, "platform-tools", "adb.exe")
        if not os.path.exists(adb_path):
            adb_path = os.path.join(sdk_root, "platform-tools", "adb")
        
        # Find emulator serial for this AVD
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "emulator" in line and avd_name in line:
                serial = line.split()[0]
                result = subprocess.run([adb_path, "-s", serial, "shell", "getprop", prop_name],
                                       capture_output=True, text=True)
                return result.stdout.strip()
        
        return f"Emulator not found: {avd_name}"