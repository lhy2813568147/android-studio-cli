"""Setup script for Android Studio CLI."""

from setuptools import setup, find_packages

setup(
    name="cli-anything-android-studio",
    version="1.0.0",
    description="CLI-Anything harness for Android Studio",
    author="CLI-Anything",
    author_email="cli-anything@example.com",
    url="https://github.com/HKUDS/CLI-Anything",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": [
            "cli-anything-android-studio=cli_anything.android_studio.android_studio_cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)