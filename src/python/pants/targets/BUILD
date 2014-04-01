# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  name = 'all',
  dependencies = [
    ':common',
    ':jvm',
    ':java',
    ':python',
    ':scala',
  ],
)

python_library(
  name = 'common',
  sources = [
    'anonymous.py',
    'doc.py',
    'external_dependency.py',
    'pants_target.py',
    'repository.py',
    'resources.py',  # XXX dependency on InternalTarget which is an abstraction leak
    'sources.py',
    'util.py',
    'with_dependencies.py',
    'with_sources.py',
  ],
  dependencies = [
    # ':jvm', XXX internal.py is in :jvm, so common won't work without it.
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/base:address',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:build_manual',
    'src/python/pants/base:parse_context',
    'src/python/pants/base:target',
  ],
)

python_library(
  name = 'jvm',
  sources = [
    'artifact.py',
    'benchmark.py',
    'credentials.py',
    'exclude.py',
    'exportable_jvm_library.py',
    'internal.py',  # XXX fixme
    'jar_dependency.py',
    'jar_library.py',
    'jarable.py',
    'jvm_binary.py',
    'jvm_target.py',
  ],
  dependencies = [
    ':common',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/base:build_manual',
    'src/python/pants/base:parse_context',
    'src/python/pants/base:target',
  ],
)

python_library(
  name = 'java',
  sources = [
    'annotation_processor.py',
    'java_agent.py',
    'java_antlr_library.py',
    'java_library.py',
    'java_protobuf_library.py',
    'java_tests.py',
    'java_thrift_library.py',
  ],
  dependencies = [
    ':common',
    ':jvm',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/base:build_manual',
    'src/python/pants/base:target',
  ],
)

python_library(
  name = 'scala',
  sources = [
    'scala_library.py',
    'scala_tests.py',
    'scalac_plugin.py',
  ],
  dependencies = [
    ':common',
    ':jvm',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/base:build_manual',
    'src/python/pants/base:target',
  ],
)

python_library(
  name = 'python',
  sources = [
    'python_antlr_library.py',
    'python_artifact.py',
    'python_binary.py',
    'python_egg.py',
    'python_library.py',
    'python_requirement.py',
    'python_target.py',
    'python_tests.py',
    'python_thrift_library.py',
  ],
  dependencies = [
    '3rdparty/python:setuptools',
    ':common',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/BUILD.commons:twitter.common.python',
    'src/python/pants/BUILD.commons:twitter.common.quantity',
    'src/python/pants/base:build_manual',
    'src/python/pants/base:parse_context',
    'src/python/pants/base:target',
  ],
)
