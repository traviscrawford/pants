# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  name = 'reporting',
  sources = globs('*.py'),
  resources = rglobs('assets/*') + globs('templates/*.mustache'),
  dependencies = [
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/BUILD.commons:twitter.common.threading',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:build_file',
    'src/python/pants/base:mustache',
    'src/python/pants/base:workunit',
    'src/python/pants/goal:run_tracker',  # XXX
    '3rdparty/python:ansicolors',
    '3rdparty/python:pystache',
  ]
)
