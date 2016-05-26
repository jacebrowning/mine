#!/usr/bin/env python

"""Setup script for mine."""

import setuptools

from mine import __project__, __version__, CLI, DESCRIPTION

try:
    README = open("README.rst").read()
    CHANGELOG = open("CHANGELOG.rst").read()
except IOError:
    LONG_DESCRIPTION = "Coming soon..."
else:
    LONG_DESCRIPTION = README + '\n' + CHANGELOG

setuptools.setup(
    name=__project__,
    version=__version__,

    description=DESCRIPTION,
    url='https://github.com/jacebrowning/mine',
    author='Jace Browning',
    author_email='jacebrowning@gmail.com',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': [CLI + ' = mine.cli:main']},

    long_description=LONG_DESCRIPTION,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ],

    install_requires=open("requirements.txt").readlines(),
)
