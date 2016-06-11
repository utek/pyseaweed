#!/usr/bin/env python
# coding=utf-8
import os

from setuptools import find_packages, setup

__version__ = "0"

with open('pyseaweed/version.py') as f:
    exec(f.read())

LICENSE = open(
    os.path.join(os.path.dirname(__file__), 'LICENSE')).read().strip()

DESCRIPTION = open(
    os.path.join(os.path.dirname(__file__), 'README.rst')).read().strip()

required_packages = [
    "requests",
    "six"
]

setup(name='pyseaweed',
      version=__version__,
      description="Module to simplify usage of WeedFS in python.",
      author="Łukasz Bołdys",
      author_email="mail@utek.pl",
      license=LICENSE,
      long_description=open('README.rst').read(),
      url="https://github.com/utek/pyseaweed",
      packages=find_packages(),
      include_package_data=True,
      test_suite="pyseaweed",
      install_requires=required_packages,
      classifiers=[
          "Intended Audience :: Developers",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ])
