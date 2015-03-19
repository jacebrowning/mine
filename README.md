mine
====

[![Build Status](http://img.shields.io/travis/jacebrowning/mine/master.svg)](https://travis-ci.org/jacebrowning/mine)
[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/mine/master.svg)](https://coveralls.io/r/jacebrowning/mine)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/mine.svg)](https://scrutinizer-ci.com/g/jacebrowning/mine/?branch=master)
[![PyPI Version](http://img.shields.io/pypi/v/mine.svg)](https://pypi.python.org/pypi/mine)
[![PyPI Downloads](http://img.shields.io/pypi/dm/mine.svg)](https://pypi.python.org/pypi/mine)

`mine` lets you syncronize application data using Dropbox.

It automatically starts and stops programs that would otherwise fight over data in a shared folder and ensures only one instance is running.  Many applications work fine when their data is stored in Dropbox, but some programs overwrite databases:

* iTunes
* iPhoto
* etc.

while others periodically write snapshot data:

* Eclipse
* Xcode
* etc.

and some just don't make sense to keep running on all your computers:

* Slack
* HipChat
* etc.

Getting Started
===============

Requirements
------------

* Python 3.3+

Installation
------------

`mine` can be installed with pip:

```
$ pip3 install mine
```

or directly from the source code:

```
$ git clone https://github.com/jacebrowning/mine.git
$ cd mine
$ python3 setup.py install
```

Setup
-----

Create a `mine.yml` in your Dropbox:

```
config:
  applications:
  - name: Eclipse
    queued: false
    versions:
      linux: null
      mac: Eclipse.app
      windows: null
  - name: iTunes
    queued: true
    versions:
      linux: null
      mac: iTunes.app
      windows: null
  computers:
  - address: 00:11:22:33:44:55
    hostname: My-iMac.local
    name: My iMac
  - address: AA:BB:CC:DD:EE:FF
    hostname: My-MacBook-Air.local
    name: My MacBook Air
```

Include the applications you would like `mine` to manage. The `queued` setting indicates it must be closed before anoter instance can start. Computers are added automatically when `mine` is run.

For remote application management, `mine` needs to be called periodically on each of your computers. Cron is good for this:

1. find the full path to `mine` with `$ which mine`
2. add a crontab scedule: `*/5 *   *   *   *   /full/path/to/mine`

Basic Usage
===========

To synchronize the current computer's state:

```
$ mine
```

To close applications on remote computers and start them locally:

```
$ mine switch
```

To close applications locally an start them on another computer:

```
$ mine switch <name>
```

To delete conflicted files in your Dropbox:

```
$ mine clean
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
