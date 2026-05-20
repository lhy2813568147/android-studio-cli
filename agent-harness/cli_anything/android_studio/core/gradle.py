"""Gradle module for Android Studio CLI."""

import os
import subprocess
import json
from typing import Optional, List, Dict, Any


class Gradle:
    """Wrapper for Gradle build commands."""
    
    def __init__(self, gradle_path: Optional[str] = None, project_dir: Optional[str] = None):
        """Initialize Gradle with optional custom path.
        
        Args:
            gradle_path: Custom path to gradle executable. If None, uses gradlew or gradle.
            project_dir: Project directory (optional)
        """
        self.project_dir = project_dir or os.getcwd()
        
        if gradle_path:
            self.gradle_path = gradle_path
        else:
            # Try gradlew first, then gradle
            gradlew = os.path.join(self.project_dir, "gradlew.bat")
            if os.path.exists(gradlew):
                self.gradle_path = gradlew
            else:
                gradlew = os.path.join(self.project_dir, "gradlew")
                if os.path.exists(gradlew):
                    self.gradle_path = gradlew
                else:
                    # Try system gradle
                    self.gradle_path = "gradle"
    
    def _run_command(self, args: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run a Gradle command.
        
        Args:
            args: Command arguments
            check: Whether to raise exception on non-zero exit
            
        Returns:
            CompletedProcess instance
        """
        cmd = [self.gradle_path] + args
        return subprocess.run(cmd, capture_output=True, text=True, check=check, 
                            cwd=self.project_dir)
    
    def build(self, variant: Optional[str] = None, clean: bool = False) -> str:
        """Build the project.
        
        Args:
            variant: Build variant (e.g., 'debug', 'release')
            clean: Clean before building
            
        Returns:
            Build output
        """
        args = []
        if clean:
            args.append("clean")
        
        if variant:
            args.append(f"assemble{variant.capitalize()}")
        else:
            args.append("assembleDebug")
        
        result = self._run_command(args)
        return result.stdout
    
    def test(self, variant: Optional[str] = None, 
             test_type: str = "unit") -> str:
        """Run tests.
        
        Args:
            variant: Build variant (optional)
            test_type: Test type ('unit', 'android', 'lint')
            
        Returns:
            Test output
        """
        args = []
        
        if test_type == "unit":
            if variant:
                args.append(f"test{variant.capitalize()}UnitTest")
            else:
                args.append("testDebugUnitTest")
        elif test_type == "android":
            if variant:
                args.append(f"connected{variant.capitalize()}AndroidTest")
            else:
                args.append("connectedDebugAndroidTest")
        elif test_type == "lint":
            if variant:
                args.append(f"lint{variant.capitalize()}")
            else:
                args.append("lintDebug")
        
        result = self._run_command(args)
        return result.stdout
    
    def clean(self) -> str:
        """Clean the project.
        
        Returns:
            Clean output
        """
        result = self._run_command(["clean"])
        return result.stdout
    
    def tasks(self, all_tasks: bool = False) -> str:
        """List available tasks.
        
        Args:
            all_tasks: Show all tasks
            
        Returns:
            Task list
        """
        args = ["tasks"]
        if all_tasks:
            args.append("--all")
        
        result = self._run_command(args)
        return result.stdout
    
    def dependencies(self, configuration: Optional[str] = None) -> str:
        """Show project dependencies.
        
        Args:
            configuration: Configuration name (optional)
            
        Returns:
            Dependencies output
        """
        args = ["dependencies"]
        if configuration:
            args.extend(["--configuration", configuration])
        
        result = self._run_command(args)
        return result.stdout
    
    def properties(self) -> str:
        """Show project properties.
        
        Returns:
            Properties output
        """
        result = self._run_command(["properties"])
        return result.stdout
    
    def generate_wrapper(self, version: Optional[str] = None) -> str:
        """Generate Gradle wrapper.
        
        Args:
            version: Gradle version (optional)
            
        Returns:
            Generation output
        """
        args = ["wrapper"]
        if version:
            args.extend(["--gradle-version", version])
        
        result = self._run_command(args)
        return result.stdout
    
    def signing_report(self, variant: Optional[str] = None) -> str:
        """Generate signing report.
        
        Args:
            variant: Build variant (optional)
            
        Returns:
            Signing report
        """
        args = []
        if variant:
            args.append(f"signingReport{variant.capitalize()}")
        else:
            args.append("signingReport")
        
        result = self._run_command(args)
        return result.stdout
    
    def assemble(self, variant: Optional[str] = None) -> str:
        """Assemble the project.
        
        Args:
            variant: Build variant (optional)
            
        Returns:
            Assemble output
        """
        args = []
        if variant:
            args.append(f"assemble{variant.capitalize()}")
        else:
            args.append("assembleDebug")
        
        result = self._run_command(args)
        return result.stdout
    
    def bundle(self, variant: Optional[str] = None) -> str:
        """Create app bundle.
        
        Args:
            variant: Build variant (optional)
            
        Returns:
            Bundle output
        """
        args = []
        if variant:
            args.append(f"bundle{variant.capitalize()}")
        else:
            args.append("bundleDebug")
        
        result = self._run_command(args)
        return result.stdout
    
    def install(self, variant: Optional[str] = None, device: Optional[str] = None) -> str:
        """Install the app on device.
        
        Args:
            variant: Build variant (optional)
            device: Device serial number (optional)
            
        Returns:
            Install output
        """
        args = []
        if variant:
            args.append(f"install{variant.capitalize()}")
        else:
            args.append("installDebug")
        
        if device:
            args.extend(["-Pandroid.injected.build.api=28", 
                        f"-Pandroid.injected.invoked.from.ide=true",
                        f"-Pandroid.injected.adb.device={device}"])
        
        result = self._run_command(args)
        return result.stdout
    
    def uninstall(self, variant: Optional[str] = None) -> str:
        """Uninstall the app from device.
        
        Args:
            variant: Build variant (optional)
            
        Returns:
            Uninstall output
        """
        args = []
        if variant:
            args.append(f"uninstall{variant.capitalize()}")
        else:
            args.append("uninstallDebug")
        
        result = self._run_command(args)
        return result.stdout
    
    def lint(self, variant: Optional[str] = None) -> str:
        """Run lint checks.
        
        Args:
            variant: Build variant (optional)
            
        Returns:
            Lint output
        """
        args = []
        if variant:
            args.append(f"lint{variant.capitalize()}")
        else:
            args.append("lintDebug")
        
        result = self._run_command(args)
        return result.stdout
    
    def check(self, variant: Optional[str] = None) -> str:
        """Run all checks.
        
        Args:
            variant: Build variant (optional)
            
        Returns:
            Check output
        """
        args = []
        if variant:
            args.append(f"check{variant.capitalize()}")
        else:
            args.append("check")
        
        result = self._run_command(args)
        return result.stdout
    
    def javadoc(self, variant: Optional[str] = None) -> str:
        """Generate Javadoc.
        
        Args:
            variant: Build variant (optional)
            
        Returns:
            Javadoc output
        """
        args = []
        if variant:
            args.append(f"generate{variant.capitalize()}Javadoc")
        else:
            args.append("generateDebugJavadoc")
        
        result = self._run_command(args)
        return result.stdout
    
    def proguard(self, variant: Optional[str] = None) -> str:
        """Run ProGuard/R8.
        
        Args:
            variant: Build variant (optional)
            
        Returns:
            ProGuard output
        """
        args = []
        if variant:
            args.append(f"minify{variant.capitalize()}WithProguard")
        else:
            args.append("minifyDebugWithProguard")
        
        result = self._run_command(args)
        return result.stdout