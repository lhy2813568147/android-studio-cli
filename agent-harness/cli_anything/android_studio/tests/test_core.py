"""Tests for Android Studio CLI."""

import os
import sys
import json
import pytest
from unittest.mock import patch, MagicMock

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli_anything.android_studio.core.adb import ADB
from cli_anything.android_studio.core.gradle import Gradle
from cli_anything.android_studio.core.emulator import Emulator


class TestADB:
    """Tests for ADB class."""
    
    def test_init_default(self):
        """Test ADB initialization with default path."""
        adb = ADB()
        assert adb.adb_path is not None
    
    def test_init_custom_path(self):
        """Test ADB initialization with custom path."""
        adb = ADB("/custom/path/to/adb")
        assert adb.adb_path == "/custom/path/to/adb"
    
    @patch("subprocess.run")
    def test_devices(self, mock_run):
        """Test devices command."""
        mock_run.return_value = MagicMock(
            stdout="List of devices attached\nemulator-5554\tdevice\n",
            returncode=0
        )
        
        adb = ADB()
        devices = adb.devices()
        
        assert len(devices) == 1
        assert devices[0]["serial"] == "emulator-5554"
        assert devices[0]["state"] == "device"
    
    @patch("subprocess.run")
    def test_shell(self, mock_run):
        """Test shell command."""
        mock_run.return_value = MagicMock(
            stdout="Hello from device",
            returncode=0
        )
        
        adb = ADB()
        result = adb.shell("echo Hello from device")
        
        assert result == "Hello from device"
    
    @patch("subprocess.run")
    def test_install(self, mock_run):
        """Test install command."""
        mock_run.return_value = MagicMock(
            stdout="Success",
            returncode=0
        )
        
        adb = ADB()
        result = adb.install("app.apk")
        
        assert result == "Success"
    
    @patch("subprocess.run")
    def test_uninstall(self, mock_run):
        """Test uninstall command."""
        mock_run.return_value = MagicMock(
            stdout="Success",
            returncode=0
        )
        
        adb = ADB()
        result = adb.uninstall("com.example.app")
        
        assert result == "Success"


class TestGradle:
    """Tests for Gradle class."""
    
    def test_init_default(self):
        """Test Gradle initialization with default path."""
        gradle = Gradle()
        assert gradle.gradle_path is not None
    
    def test_init_custom_path(self):
        """Test Gradle initialization with custom path."""
        gradle = Gradle("/custom/path/to/gradle")
        assert gradle.gradle_path == "/custom/path/to/gradle"
    
    @patch("subprocess.run")
    def test_build(self, mock_run):
        """Test build command."""
        mock_run.return_value = MagicMock(
            stdout="BUILD SUCCESSFUL",
            returncode=0
        )
        
        gradle = Gradle()
        result = gradle.build()
        
        assert "BUILD SUCCESSFUL" in result
    
    @patch("subprocess.run")
    def test_clean(self, mock_run):
        """Test clean command."""
        mock_run.return_value = MagicMock(
            stdout="BUILD SUCCESSFUL",
            returncode=0
        )
        
        gradle = Gradle()
        result = gradle.clean()
        
        assert "BUILD SUCCESSFUL" in result
    
    @patch("subprocess.run")
    def test_test(self, mock_run):
        """Test test command."""
        mock_run.return_value = MagicMock(
            stdout="TEST PASSED",
            returncode=0
        )
        
        gradle = Gradle()
        result = gradle.test()
        
        assert "TEST PASSED" in result


class TestEmulator:
    """Tests for Emulator class."""
    
    def test_init_default(self):
        """Test Emulator initialization with default path."""
        emulator = Emulator()
        assert emulator.emulator_path is not None
    
    def test_init_custom_path(self):
        """Test Emulator initialization with custom path."""
        emulator = Emulator("/custom/path/to/emulator")
        assert emulator.emulator_path == "/custom/path/to/emulator"
    
    @patch("subprocess.run")
    def test_list_avds(self, mock_run):
        """Test list_avds command."""
        mock_run.return_value = MagicMock(
            stdout="Pixel_6_API_33\nPixel_4_API_30\n",
            returncode=0
        )
        
        emulator = Emulator()
        avds = emulator.list_avds()
        
        assert len(avds) == 2
        assert "Pixel_6_API_33" in avds
        assert "Pixel_4_API_30" in avds


if __name__ == "__main__":
    pytest.main([__file__])