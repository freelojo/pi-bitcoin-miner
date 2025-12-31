"""
Raspberry Pi Bitcoin Miner - Setup Configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pi-bitcoin-miner",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Distributed Bitcoin mining using Raspberry Pi 4 and Pico boards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pi-bitcoin-miner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Embedded Systems",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.14",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pi-bitcoin-miner=controller.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "controller": ["py.typed"],
    },
)
