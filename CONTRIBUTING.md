# For Contributors

## Setup

### Requirements

* Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* Pandoc: http://johnmacfarlane.net/pandoc/installing.html
* Graphviz: http://www.graphviz.org/Download.php

### Installation

Install project dependencies into a virtual environment:

```sh
$ make install
```

## Development Tasks

### Testing

Manually run the tests:

```sh
$ make test
$ make tests  # includes integration tests
```

or keep them running on change:

```sh
$ make watch
```

> In order to have OS X notifications, `brew install terminal-notifier`.

### Documentation

Build the documentation:

```sh
$ make doc
```

### Static Analysis

Run linters and static analyzers:

```sh
$ make pep8
$ make pep257
$ make pylint
$ make check  # includes all checks
```

## Continuous Integration

The CI server will report overall build status:

```sh
$ make ci
```

## Release Tasks

Release to PyPI:

```sh
$ make upload-test  # dry run upload to a test server
$ make upload
```
