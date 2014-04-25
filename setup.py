#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages

__version__ = "0"

with open('pyweed/version.py') as f:
    exec(f.read())

required_packages = [
    "httplib2",
    "six"
]

setup(name='pyweed',
      version=__version__,
      description="Python module to communicate with Weed-FS",
      author="Łukasz Bołdys",
      author_email="mail@utek.pl",
      license="MIT",
      long_description=open('README.rst').read(),
      url="https://github.com/utek/pyweed",
      packages=find_packages(),
      include_package_data=True,
      test_suite="pyweed.tests",
      install_requires=required_packages)
