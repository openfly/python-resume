#!/usr/bin/env python

'''
    Execution:
        python setup.py build
        python setup.py install
    Purpose:
        This is the setup script for the app
'''

__author__ = 'Matt Joyce'
__email__ = 'matt@surly.bike'
__copyright__ = "Copyright 2017, Matt Joyce"

from setuptools import setup, find_packages
from pip.req import parse_requirements

INSTALL_REQS = parse_requirements('requirements.txt', session=False)
REQS = [str(ir.req) for ir in INSTALL_REQS]

setup(
    name='python-resume',
    version='0.1.2',
    description='Resume Generator',
    author='Matt Joyce',
    author_email='matt@surly.bike',
    url='http://surly.bike/',
    # install dependencies from requirements.txt
    install_requires=REQS,
    packages=find_packages(),
    # bin files / python standalone executable scripts
    scripts=['bin/resume.py'],
    include_package_data=True,
    zip_safe=False,
)
