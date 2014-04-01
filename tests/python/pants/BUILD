# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  name = 'base-test',
  sources = ['base_build_root_test.py'],
  dependencies = [
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:address',
    'src/python/pants/base:build_root',
    'src/python/pants/base:target',
    'src/python/pants/targets:common',
  ]
)

python_tests(
  name = 'test_maven_layout',
  sources = ['test_maven_layout.py'],
  dependencies = [
    ':base-test',
  ]
)

python_tests(
  name = 'test_thrift_util',
  sources = ['test_thrift_util.py'],
  dependencies = [
    ':base-test',
    'src/python/pants/BUILD.commons:twitter.common.contextutil',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants:thrift_util',
  ]
)

python_test_suite(
  name = 'all',
  dependencies = [
    ':test_maven_layout',
    ':test_thrift_util',
    'tests/python/pants/base',
    'tests/python/pants/cache',
    'tests/python/pants/commands',
    'tests/python/pants/engine',
    'tests/python/pants/fs',
    'tests/python/pants/java',
    'tests/python/pants/net',
    'tests/python/pants/process',
    'tests/python/pants/python',
    'tests/python/pants/reporting',
    'tests/python/pants/scm',
    'tests/python/pants/targets',
    'tests/python/pants/tasks',
  ]
)
