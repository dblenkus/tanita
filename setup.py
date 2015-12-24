#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Domen Blenkuš
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

version = __import__('tanita').VERSION

setup(
    name='tanita',
    version=version,
    url='https://github.com/dblenkus/tanita',
    author='Domen Blenkuš',
    author_email='domen@blenkus.com',
    description='Process data from Tanita BC-601 Body Composition Monitor.',
    long_description=open('README.rst', 'r').read(),
    license='Apache License (2.0)',
    packages=['tanita'],
    install_requires=[
        'matplotlib>=1.5.0',
        'reportlab>=3.0.0',
    ],
    extras_require={
        'test': ['check-manifest', 'pylint', 'readme'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'tanita = tanita.tanita:main',
        ]
    },
)
