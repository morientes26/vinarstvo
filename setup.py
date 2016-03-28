# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages
import os
import sys


_version = '0.0.1'
#_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

_short_description = "Winelist is inventory management for wines and other product in bar"


#_transform_dir = 'pylint_django/transforms/transforms'
#_package_data = {
#    'pylint_django': [
#        os.path.join('transforms/transforms', name) for name in os.listdir(_transform_dir)
#    ]
#}

_classifiers = (
    'Development Status :: 1 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: Unix',
    'Topic :: Software Development :: Quality Assurance',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
)


#_install_requires = [
#    'pylint-plugin-utils>=0.2.1'
#]


# if sys.version_info < (2, 7):
#     # pylint 1.4 dropped support for Python 2.6
#     _install_requires += [
#         'pylint>=1.0,<1.4',
#         'astroid>=1.0,<1.3.0',
#         'logilab-common>=0.60.0,<0.63',
#     ]
# else:
#     _install_requires += [
#         'pylint>=1.0',
#     ]

setup(
    name='winelist',
    url='https://github.com/morientes26/winecart.git',
    author='morienstudio',
    author_email='michalkalman@gmail.com',
    description=_short_description,
    version=_version,
    #packages=_packages,
    #package_data=_package_data,
    #install_requires=_install_requires,
    license='GPLv2',
    classifiers=_classifiers,
    keywords='winelist'
)
