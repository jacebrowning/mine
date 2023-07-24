# Overview

This program lets you synchronize application data using Dropbox.

It automatically starts and stops programs that would otherwise fight over data in a shared folder and ensures only one instance is running. Many applications work fine when their data is stored in Dropbox, but some programs overwrite databases:

- iTunes
- iPhoto
- etc.

while others periodically write snapshot data:

- Eclipse
- Xcode
- etc.

and some just don't make sense to keep running on all your computers:

- Slack
- HipChat
- etc.

[![Build Status](https://img.shields.io/github/actions/workflow/status/jacebrowning/mine/main.yml?branch=main&label=build)](https://github.com/jacebrowning/mine/actions)
[![Coverage Status](https://img.shields.io/codecov/c/gh/jacebrowning/mine)](https://codecov.io/gh/jacebrowning/mine)
[![PyPI Version](https://img.shields.io/pypi/v/mine.svg?label=version)](https://pypi.org/project/mine)
[![PyPI Downloads](https://img.shields.io/pypi/dm/mine.svg?color=orange)](https://pypistats.org/packages/mine)

## Setup

### Requirements

- Python 3.10+

### Installation

Install `mine` with [pipx](https://pipxproject.github.io/pipx/installation/) (or pip):

```sh
$ pipx install mine
```

or directly from the source code:

```sh
$ git clone https://github.com/jacebrowning/mine.git
$ cd mine
$ python setup.py install
```

### Configuration

Create a `mine.yml` in your Dropbox:

```yaml
config:
  computers:
    - name: My iMac
      hostname: My-iMac.local
      address: 00:11:22:33:44:55
    - name: My MacBook Air
      hostname: My-MacBook-Air.local
      address: AA:BB:CC:DD:EE:FF
  applications:
    - name: iTunes
      properties:
        auto_queue: false
        single_instance: true
      versions:
        mac: iTunes.app
        windows: iTunes.exe
        linux: null
    - name: Slack
      properties:
        auto_queue: true
        single_instance: false
      versions:
        mac: Slack.app
        windows: null
        linux: null
```

Include the applications you would like `mine` to manage. Computers are added automatically when `mine` is run.

The `versions` dictionary identifies the name of the executable on each platform. The `properties.auto_queue` setting indicates `mine` should attempt to launch the application automatically when switching computers. The `properties.single_instance` setting indicates the application must be closed on other computers before another instance can start.

## Usage

To synchronize the current computer's state:

```sh
$ mine
```

To close applications on remote computers and start them locally:

```sh
$ mine switch
```

To close applications running locally:

```sh
$ mine close
```

To close applications locally and start them on another computer:

```sh
$ mine switch <name>
```

To delete conflicted files in your Dropbox:

```sh
$ mine clean
```
