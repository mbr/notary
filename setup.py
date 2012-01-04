#!/usr/bin/env python
# coding=utf8

import os
import sys

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='notary',
      version='0.0.1',
      description='Find out who\'s making breakfast this morning.',
      long_description=read('README.rst'),
      install_requires=['flask'],
      keywords='notary',
      author='Marc Brinkmann',
      author_email='git@marcbrinkmann.de',
      url='http://github.com/mbr/notary',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      package_data={'': ['templates/*.html']},
      classifiers=[
      ]
     )
