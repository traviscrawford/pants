# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  name = 'distribution',
  sources = globs('distribution/*.py'),
  resources = globs('distribution/*.class'),
  dependencies = [
    'src/python/pants/BUILD.commons:twitter.common.contextutil',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/BUILD.commons:twitter.common.log',
    'src/python/pants/base:revision',
  ]
)

python_library(
  name = 'executor',
  sources = ['executor.py'],
  dependencies = [
    ':distribution',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.contextutil',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/BUILD.commons:twitter.common.log',
  ]
)

python_library(
  name = 'jar',
  sources = globs('jar/*.py'),
  dependencies = [
    'src/python/pants/BUILD.commons:twitter.common.contextutil',
    'src/python/pants/BUILD.commons:twitter.common.lang',
  ]
)

python_library(
  name = 'nailgun_client',
  sources = ['nailgun_client.py'],
)

python_library(
  name = 'nailgun_executor',
  sources = ['nailgun_executor.py'],
  dependencies = [
    '3rdparty/python:psutil',
    ':nailgun_client',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/BUILD.commons:twitter.common.log',
    'src/python/pants/base:build_environment',
  ],
)

python_library(
  name = 'util',
  sources = ['util.py'],
  dependencies = [
    ':executor',
    ':nailgun_executor',
    'src/python/pants/base:workunit',
  ],
)
