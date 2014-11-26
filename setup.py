#!/usr/bin/env python

"""
Setup script for mine.
"""

import setuptools

from mine import __project__, __version__

import os
if os.path.exists('README.rst'):
    README = open('README.rst').read()
else:
    README = ""  # a placeholder, readme is generated on release
CHANGES = open('CHANGES.md').read()


setuptools.setup(
    name=__project__,
    version=__version__,

    description="TBD",
    url='https://github.com/jacebrowning/mine',
    author='Jace Browning',
    author_email='jacebrowning@gmail.com',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': []},

    long_description=(README + '\n' + CHANGES),
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
    ],

    # TODO: switch to requirements.txt after YORM is stable
    # install_requires=open('requirements.txt').readlines(),

    install_requires=[
        "YORM",
    ],
    dependency_links=[
        'https://github.com/jacebrowning/yorm/archive/develop.zip#egg=YORM'
    ]
)
