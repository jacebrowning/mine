mine
======
TBD

[![Build Status](http://img.shields.io/travis/jacebrowning/mine/master.svg)](https://travis-ci.org/jacebrowning/mine)
[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/mine/master.svg)](https://coveralls.io/r/jacebrowning/mine)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/mine.svg)](https://scrutinizer-ci.com/g/jacebrowning/mine/?branch=master)
[![PyPI Version](http://img.shields.io/pypi/v/mine.svg)](https://pypi.python.org/pypi/mine)
[![PyPI Downloads](http://img.shields.io/pypi/dm/mine.svg)](https://pypi.python.org/pypi/mine)


Getting Started
===============

Requirements
------------

* Python 3.3+

Installation
------------

Mine can be installed with pip:

```
$ pip install mine
```

or directly from the source code:

```
$ git clone https://github.com/jacebrowning/mine.git
$ cd mine
$ python setup.py install
```

Basic Usage
===========

After installation, abstract base classes can be imported from the package:

```
$ python
>>> import mine
mine.__version__
```

For Contributors
================

Requirements
------------

* Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* virtualenv: https://pypi.python.org/pypi/virtualenv#installation
* Pandoc: http://johnmacfarlane.net/pandoc/installing.html
* Graphviz: http://www.graphviz.org/Download.php

Installation
------------

Create a virtualenv:

```
$ make env
```

Run the tests:

```
$ make test
$ make tests  # includes integration tests
```

Build the documentation:

```
$ make doc
```

Run static analysis:

```
$ make pep8
$ make pep257
$ make pylint
$ make check  # includes all checks
```

Prepare a release:

```
$ make dist  # dry run
$ make upload
```
