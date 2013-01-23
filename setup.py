#!/usr/bin/env python
from setuptools import setup

long_description = open('README.rst').read()

setup(name='opencouncil',
      version='0.0.1',
      author="Jeffrey Johnson",
      author_email="jjohnson@opensandiego.org",
      license="MIT",
      url="http://council.opensandiego.org",
      description='Open Council SD',
      long_description=long_description,
      platforms=['any'],
)
