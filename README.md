# Whooshstore

[![Build Status](https://travis-ci.org/knipknap/whooshstore.svg?branch=master)](https://travis-ci.org/knipknap/whooshstore)
[![Coverage Status](https://coveralls.io/repos/github/knipknap/whooshstore/badge.svg?branch=master)](https://coveralls.io/github/knipknap/whooshstore?branch=master)
[![Code Climate](https://lima.codeclimate.com/github/knipknap/whooshstore/badges/gpa.svg)](https://lima.codeclimate.com/github/knipknap/whooshstore)

## Summary

Whooshstore is a simple Python module for indexing and searching files
on your local hard drive. It supports incremental indexing, pagination,
and provides a Python API as well as a command line tool.

## Example CLI usage

```
ws-update -b --index my.idx datadir  # build the index
ws-update -b --append --index my.idx datadir  # incremental update
ws-update --help  # complete command line syntax

ws --index my.idx hello world     # query the index
ws --help  # complete command line syntax
```

## Python API

```python
from whooshstore import util, open_index, update_index, search

# Build the index.
ix = open_index('my.idx', False)
files = util.find_files('datadir', ('*.txt',))
update_index(files, ix = ix, incremental = False, batch = True)

# Query.
for result in search('hello world', ix = ix, limit = 20):
    print result
```
