"""
x-gif-maker: Create animated GIFs/MP4s for social media posts.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = ""

# Read requirements
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="x-gif-maker",
    version="2.0.0",
    author="CCAgentOrg",
    author_email="contact@nanobot.srik.me",
    description="Create animated GIFs and MP4s for social media posts with 11+ animation styles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CCAgentOrg/nanobot-skills",
    project_urls={
        "Bug Reports": "https://github.com/CCAgentOrg/nanobot-skills/issues",
        "Source": "https://github.com/CCAgentOrg/nanobot-skills",
        "Documentation": "https://nanobot.srik.me",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="gif mp4 animation social-media twitter instagram",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "x-gif-maker=scripts.create_gif:main",
        ],
    },
)
