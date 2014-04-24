#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, print_function
from itertools import chain, imap, repeat
from setuptools import setup, find_packages
from os import walk
from os.path import join


def include_directories(in_dirs):
    paths = list()
    for directory in in_dirs:
        paths.extend(list(chain.from_iterable(imap(join, repeat(root[len('pyweed') + 1:]), files) for root, _, files in walk(join('pyweed', directory)))))
    return paths

package_data = include_directories([])

required_packages = [
    "httplib2",
]

setup(name='pyweed',
      version='0.0.2',
      description="Python module to communicate with Weed-FS",
      author="Łukasz Bołdys",
      author_email="mail@utek.pl",
      packages=find_packages(),
      package_data={
          'pyweed': package_data
      },
      test_suite="pyweed.tests",
      install_requires=required_packages)
