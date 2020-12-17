# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from setuptools import setup, find_packages

install_requires = [line.rstrip() for line in open("requirements.txt", "r")]

with open("README.md", "r") as f:
    long_description = f.read()


def find_version(file_path):
    with open(file_path, "r") as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
        if version_match:
            return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="pybulletX",
    version=find_version("pybulletX/__init__.py"),
    author="Po-Wei Chou",
    author_email="poweic@fb.com",
    description="A Pythonic wrapper for pybullet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fair-robotics/core",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
)
