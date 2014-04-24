#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages


required_packages = [
    "httplib2",
]

setup(name='pyweed',
      version='0.1.1',
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
