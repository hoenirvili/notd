#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='notd',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['notd'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        notd=notd:cli
    ''',
)
