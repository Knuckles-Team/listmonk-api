#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from listmonk_api.version import __version__, __author__, __credits__
from pathlib import Path
import re

readme = Path('README.md').read_text()
version = __version__
readme = re.sub(r"Version: [0-9]*\.[0-9]*\.[0-9][0-9]*", f"Version: {version}", readme)
print(f"README: {readme}")
with open("README.md", "w") as readme_file:
    readme_file.write(readme)
description = 'Python tool that allows you to take multiple full page screenshots of web pages without ads.'

setup(
    name='listmonk-api',
    version=f"{version}",
    description=description,
    long_description=f'{readme}',
    long_description_content_type='text/markdown',
    url='https://github.com/Knucklessg1/listmonk-api',
    author=__author__,
    author_email='knucklessg1@gmail.com',
    license='Unlicense',
    packages=['listmonk_api'],
    include_package_data=True,
    install_requires=['requests', 'urllib3'],
    py_modules=['listmonk_api'],
    package_data={'listmonk_api': ['listmonk_api']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: Public Domain',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ]
)