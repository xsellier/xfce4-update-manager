#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='xfce4-update-manager',
      version='1.0.0',
      description='Update manager for xfce',
      author='Xavier Sellier',
      install_requires=[
        'notify2',
        'python-apt'
      ],
      long_description=open('README.md').read(),
      )
