"""ADB (Android Debug Bridge) module for Android Studio CLI."""

import os
import subprocess
import json
from typing import Optional, List, Dict, Any


class ADB:
    """Wrapper for Android Debug Bridge commands."""
    
    def __init__(self, adb_path: Optional[str] = None):
        """Initialize ADB with optional custom path.
        
        Args:
            adb_path: Custom path to adb executable. If None, uses Android SDK default.
        """
        if adb_path:
            self.adb_path = adb_path
        else:
            # Try to find adb in Android SDK
            sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
            if not sdk_root:
                # Default Windows path
                sdk_root = os.path.expanduser("~/AppData/Local/Android/Sdk")
            
            self.adb_path = os.path.join(sdk_root, "platform-tools", "adb.exe")
            if not os.path.exists(self.adb_path):
                # Try alternative path
                self.adb_path = os.path.join(sdk_root, "platform-tools", "adb")
    
    def _run_command(self, args: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run an ADB command.
        
        Args:
            args: Command arguments
            check: Whether to raise exception on non-zero exit
            
        Returns:
            CompletedProcess instance
        """
        cmd = [self.adb_path] + args
        return subprocess.run(cmd, capture_output=True, text=True, check=check)
    
    def devices(self) -> List[Dict[str, str]]:
        """List connected devices.
        
        Returns:
            List of device dictionaries with 'serial' and 'state' keys
        """
        result = self._run_command(["devices"])
        devices = []
        for line in result.stdout.strip().split("\n")[1:]:  # Skip header
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    devices.append({
                        "serial": parts[0],
                        "state": parts[1]
                    })
        return devices
    
    def shell(self, command: str, device: Optional[str] = None) -> str:
        """Run a shell command on the device.
        
        Args:
            command: Shell command to run
            device: Device serial number (optional)
            
        Returns:
            Command output
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.extend(["shell", command])
        
        result = self._run_command(args)
        return result.stdout
    
    def install(self, apk_path: str, device: Optional[str] = None, 
                replace: bool = True, test: bool = False) -> str:
        """Install an APK to the device.
        
        Args:
            apk_path: Path to APK file
            device: Device serial number (optional)
            replace: Replace existing app
            test: Install test package
            
        Returns:
            Installation result
        """
        args = []
        if device:
            args.extend(["-s", device])
        
        install_args = []
        if replace:
            install_args.append("-r")
        if test:
            install_args.append("-t")
        
        args.extend(["install"] + install_args + [apk_path])
        result = self._run_command(args)
        return result.stdout
    
    def uninstall(self, package: str, device: Optional[str] = None, 
                  keep_data: bool = False) -> str:
        """Uninstall an app from the device.
        
        Args:
            package: Package name
            device: Device serial number (optional)
            keep_data: Keep app data
            
        Returns:
            Uninstallation result
        """
        args = []
        if device:
            args.extend(["-s", device])
        
        uninstall_args = []
        if keep_data:
            uninstall_args.append("-k")
        
        args.extend(["uninstall"] + uninstall_args + [package])
        result = self._run_command(args)
        return result.stdout
    
    def push(self, local_path: str, remote_path: str, 
             device: Optional[str] = None) -> str:
        """Push a file to the device.
        
        Args:
            local_path: Local file path
            remote_path: Remote file path
            device: Device serial number (optional)
            
        Returns:
            Push result
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.extend(["push", local_path, remote_path])
        
        result = self._run_command(args)
        return result.stdout
    
    def pull(self, remote_path: str, local_path: str, 
             device: Optional[str] = None) -> str:
        """Pull a file from the device.
        
        Args:
            remote_path: Remote file path
            local_path: Local file path
            device: Device serial number (optional)
            
        Returns:
            Pull result
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.extend(["pull", remote_path, local_path])
        
        result = self._run_command(args)
        return result.stdout
    
    def logcat(self, filter: Optional[str] = None, device: Optional[str] = None,
               lines: Optional[int] = None) -> str:
        """Get device logs.
        
        Args:
            filter: Log filter expression
            device: Device serial number (optional)
            lines: Number of lines to retrieve
            
        Returns:
            Log output
        """
        args = []
        if device:
            args.extend(["-s", device])
        
        logcat_args = []
        if lines:
            logcat_args.extend(["-d", "-t", str(lines)])
        if filter:
            logcat_args.append(filter)
        
        args.extend(["logcat"] + logcat_args)
        result = self._run_command(args)
        return result.stdout
    
    def forward(self, local_port: int, remote_port: int, 
                device: Optional[str] = None) -> str:
        """Forward a port from device to localhost.
        
        Args:
            local_port: Local port number
            remote_port: Remote port number
            device: Device serial number (optional)
            
        Returns:
            Forward result
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.extend(["forward", f"tcp:{local_port}", f"tcp:{remote_port}"])
        
        result = self._run_command(args)
        return result.stdout
    
    def reverse(self, remote_port: int, local_port: int, 
                device: Optional[str] = None) -> str:
        """Reverse forward a port from localhost to device.
        
        Args:
            remote_port: Remote port number
            local_port: Local port number
            device: Device serial number (optional)
            
        Returns:
            Reverse result
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.extend(["reverse", f"tcp:{remote_port}", f"tcp:{local_port}"])
        
        result = self._run_command(args)
        return result.stdout
    
    def start_server(self) -> str:
        """Start the ADB server.
        
        Returns:
            Start result
        """
        result = self._run_command(["start-server"])
        return result.stdout
    
    def kill_server(self) -> str:
        """Kill the ADB server.
        
        Returns:
            Kill result
        """
        result = self._run_command(["kill-server"])
        return result.stdout
    
    def get_state(self, device: Optional[str] = None) -> str:
        """Get device state.
        
        Args:
            device: Device serial number (optional)
            
        Returns:
            Device state
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.append("get-state")
        
        result = self._run_command(args)
        return result.stdout.strip()
    
    def get_serialno(self, device: Optional[str] = None) -> str:
        """Get device serial number.
        
        Args:
            device: Device serial number (optional)
            
        Returns:
            Serial number
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.append("get-serialno")
        
        result = self._run_command(args)
        return result.stdout.strip()
    
    def get_devpath(self, device: Optional[str] = None) -> str:
        """Get device path.
        
        Args:
            device: Device serial number (optional)
            
        Returns:
            Device path
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.append("get-devpath")
        
        result = self._run_command(args)
        return result.stdout.strip()
    
    def wait_for_device(self, device: Optional[str] = None, 
                        timeout: Optional[int] = None) -> str:
        """Wait for device to connect.
        
        Args:
            device: Device serial number (optional)
            timeout: Timeout in seconds (optional)
            
        Returns:
            Wait result
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.append("wait-for-device")
        
        if timeout:
            result = self._run_command(args, check=False)
        else:
            result = self._run_command(args)
        
        return result.stdout
    
    def bug_report(self, device: Optional[str] = None, 
                   output_path: Optional[str] = None) -> str:
        """Generate bug report.
        
        Args:
            device: Device serial number (optional)
            output_path: Output file path (optional)
            
        Returns:
            Bug report path or content
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.append("bugreport")
        
        if output_path:
            args.append(output_path)
            result = self._run_command(args)
            return f"Bug report saved to: {output_path}"
        else:
            result = self._run_command(args)
            return result.stdout
    
    def backup(self, device: Optional[str] = None, 
               apk: bool = False, shared: bool = False,
               output_path: str = "backup.ab") -> str:
        """Backup device data.
        
        Args:
            device: Device serial number (optional)
            apk: Include APKs
            shared: Include shared storage
            output_path: Output file path
            
        Returns:
            Backup result
        """
        args = []
        if device:
            args.extend(["-s", device])
        
        backup_args = []
        if apk:
            backup_args.append("-apk")
        if shared:
            backup_args.append("-shared")
        
        args.extend(["backup"] + backup_args + [output_path])
        result = self._run_command(args)
        return result.stdout
    
    def restore(self, backup_path: str, device: Optional[str] = None) -> str:
        """Restore device data from backup.
        
        Args:
            backup_path: Backup file path
            device: Device serial number (optional)
            
        Returns:
            Restore result
        """
        args = []
        if device:
            args.extend(["-s", device])
        args.extend(["restore", backup_path])
        
        result = self._run_command(args)
        return result.stdout