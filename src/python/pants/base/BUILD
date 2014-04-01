# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  name = 'abbreviate_target_ids',
  sources = ['abbreviate_target_ids.py'],
)

python_library(
  name = 'address',
  sources = ['address.py'],
  dependencies = [
    'src/python/pants/BUILD.commons:twitter.common.lang',
    ':build_file',
  ]
)

python_library(
  name = 'build_environment',
  sources = ['build_environment.py'],
  dependencies = [
    'src/python/pants/BUILD.commons:twitter.common.log',
    'src/python/pants/version',
    'src/python/pants/scm:all',
    ':build_root',
  ]
)

python_library(
  name = 'build_file',
  sources = ['build_file.py'],
  dependencies = [
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.python',
  ]
)

python_library(
  name = 'build_file_aliases',
  sources = ['build_file_aliases.py'],
  dependencies = [
    'src/python/pants/targets:all',  # XXX(fixme)
  ]
)

python_library(
  name = 'build_file_context',  # XXX(fixme)
  sources = ['build_file_context.py'],
  dependencies = [
    ':build_environment',
    ':build_file_aliases',
    ':build_file_helpers',
    ':config',
    'src/python/pants/goal',
    'src/python/pants/targets:common',
    'src/python/pants/tasks:common',
  ]
)

python_library(
  name = 'build_file_helpers',  # XXX(fixme)
  sources = ['build_file_helpers.py'],
  dependencies = [
    'src/python/pants/targets:all',  # XXX(fixme)
  ]
)

python_library(
  name = 'build_invalidator',
  sources = ['build_invalidator.py'],
  dependencies = [
    ':hash_utils',
    ':target',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/fs',
  ]
)

python_library(
  name = 'build_manual',
  sources = ['build_manual.py'],
)

python_library(
  name = 'build_root',
  sources = ['build_root.py'],
  dependencies = [
    'src/python/pants/BUILD.commons:twitter.common.lang',
  ],
)

python_library(
  name = 'config',
  sources = ['config.py'],
  dependencies = [
    ':build_environment',
  ]
)

python_library(
  name = 'double_dag',
  sources = ['double_dag.py'],
  dependencies = [
    ':abbreviate_target_ids',
  ]
)

python_library(
  name = 'generator',
  sources = ['generator.py'],
  dependencies = [
    ':mustache',
    'src/python/pants/BUILD.commons:twitter.common.lang',
  ]
)

python_library(
  name = 'hash_utils',
  sources = ['hash_utils.py'],
)

python_library(
  name = 'mustache',
  sources = ['mustache.py'],
  dependencies = [
    '3rdparty/python:pystache',
  ]
)

python_library(
  name = 'parse_context',
  sources = ['parse_context.py'],
  dependencies = [
    ':build_environment',
    ':build_file',
    ':build_file_context',
    ':config',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/BUILD.commons:twitter.common.lang',
  ]
)

python_library(
  name = 'rcfile',
  sources = ['rcfile.py'],
  dependencies = [
    ':config',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/BUILD.commons:twitter.common.log',
  ]
)

python_library(
  name = 'revision',
  sources = ['revision.py'],
)

python_library(
  name = 'run_info',
  sources = ['run_info.py'],
  dependencies = [
    ':build_environment',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
  ],
)

python_library(
  name = 'target',
  sources = ['target.py'],
  dependencies = [
    ':address',
    ':build_manual',
    ':hash_utils',
    ':parse_context',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.lang',
  ],
)

python_library(
  name = 'timer',
  sources = ['timer.py'],
  dependencies = [
    'src/python/pants/BUILD.commons:twitter.common.lang',
  ],
)

python_library(
  name = 'worker_pool',
  sources = ['worker_pool.py'],
  dependencies = [
    'src/python/pants/reporting', # XXX(fixme)
  ],
)

python_library(
  name = 'workunit',
  sources = ['workunit.py'],
  dependencies = [
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/BUILD.commons:twitter.common.rwbuf', # XXX(fixme)
  ],
)
