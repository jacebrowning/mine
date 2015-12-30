# mine

>...for applications that haven't learned to share.

[![Build Status](http://img.shields.io/travis/jacebrowning/mine/master.svg)](https://travis-ci.org/jacebrowning/mine)
[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/mine/master.svg)](https://coveralls.io/r/jacebrowning/mine)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/mine.svg)](https://scrutinizer-ci.com/g/jacebrowning/mine/?branch=master)
[![PyPI Version](http://img.shields.io/pypi/v/mine.svg)](https://pypi.python.org/pypi/mine)
[![PyPI Downloads](http://img.shields.io/pypi/dm/mine.svg)](https://pypi.python.org/pypi/mine)

This is a program that lets you synchronize application data using Dropbox.

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

# Getting Started

## Requirements

* Python 3.3+

## Installation

`mine` can be installed with pip:

```
$ pip install mine
```

or directly from the source code:

```
$ git clone https://github.com/jacebrowning/mine.git
$ cd mine
$ python setup.py install
```

## Setup

Create a `mine.yml` in your Dropbox:

```
config:
  applications:
  - name: iTunes
    properties:
      auto_queue: false
      single_instance: true
    versions:
      linux: null
      mac: iTunes.app
      windows: iTunes.exe
  - name: Slack
    properties:
      auto_queue: true
      single_instance: false
    versions:
      linux: null
      mac: Slack.app
      windows: null
  computers:
  - address: 00:11:22:33:44:55
    hostname: My-iMac.local
    name: My iMac
  - address: AA:BB:CC:DD:EE:FF
    hostname: My-MacBook-Air.local
    name: My MacBook Air
```

Include the applications you would like `mine` to manage. Computers are added automatically when `mine` is run.

The `versions` dictionary identifies the name of the executable on each platform. The `properties.auto_queue` setting indicates `mine` should attempt to launch the application automatically when switching computers. The `properties.single_instance` setting indicates the application must be closed on other computers before another instance can start.

For remote application management, `mine` needs to be started automatically on each of your computers. Cron is good for this:

1. Find the full path to `mine` with `$ which mine`
2. Add a `crontab` schedule with `$ crontab -e`: `@reboot /path/to/mine --daemon --verbose >> /tmp/mine.log 2>&1 &`

# Basic Usage

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
