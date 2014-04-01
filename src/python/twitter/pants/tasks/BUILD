# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  name = 'common',
  sources = ['__init__.py'],
  dependencies = [
    ':task',
    ':task_error',
  ]
)

python_library(
  name = 'antlr_gen',
  sources = ['antlr_gen.py'],
  dependencies = [
    ':code_gen',
    ':common',
    ':nailgun_task',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/targets:java',
    'src/python/pants/targets:java',
  ],
)

python_library(
  name = 'args_resource_mapper',
  sources = ['args_resource_mapper.py'],
  dependencies = [
    ':common',
    'src/python/pants/java:jar',
    'src/python/pants/targets:java',
    'src/python/pants/targets:scala',
  ],
)

python_library(
  name = 'benchmark_run',
  sources = ['benchmark_run.py'],
  dependencies = [
    ':common',
    ':jvm_task',
    'src/python/pants/java:util',
  ],
)

python_library(
  name = 'binary_create',
  sources = ['binary_create.py'],
  dependencies = [
    ':common',
    ':jvm_binary_task',
    'src/python/pants/BUILD.commons:twitter.common.contextutil',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:build_environment',
    'src/python/pants/fs',
    'src/python/pants/java:jar',
  ],
)

python_library(
  name = 'bootstrap_jvm_tools',
  sources = ['bootstrap_jvm_tools.py'],
  dependencies = [
    ':common',
    'src/python/pants/base:workunit',
  ],
)

python_library(
  name = 'build_lint',
  sources = ['build_lint.py'],
  dependencies = [
    ':common',
  ],
)

python_library(
  name = 'builddictionary',
  sources = ['builddictionary.py'],
  resources = globs('templates/builddictionary/*.mustache'),
  dependencies = [
    ':common',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:build_file_helpers',
    'src/python/pants/base:generator',
    'src/python/pants/goal:phase',
    '3rdparty/python:setuptools',
  ],
)

python_library(
  name = 'bundle_create',
  sources = ['bundle_create.py'],
  dependencies = [
    ':common',
    ':jvm_binary_task',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.contextutil',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:build_environment',
    'src/python/pants/fs',
    'src/python/pants/java:jar',
    'src/python/pants/targets:jvm',
  ],
)

python_library(
  name = 'cache_manager',
  sources = ['cache_manager.py'],
  dependencies = [
    ':common',
    'src/python/pants/base:build_invalidator',
    'src/python/pants/base:target',
    'src/python/pants/targets:common',
    'src/python/pants/targets:jvm',
  ],
)

python_library(
  name = 'check_exclusives',
  sources = ['check_exclusives.py'],
  dependencies = [
    ':common',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/base:target',
    'src/python/pants/targets:common',
  ],
)

python_library(
  name = 'check_published_deps',
  sources = ['check_published_deps.py'],
  dependencies = [
    ':common',
    ':console_task',
    ':jar_publish',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:build_file',
    'src/python/pants/base:target',
    'src/python/pants/targets:jvm',
  ],
)

python_library(
  name = 'checkstyle',
  sources = ['checkstyle.py'],
  dependencies = [
    ':common',
    ':nailgun_task',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/process',
  ],
)

python_library(
  name = 'code_gen',
  sources = ['code_gen.py'],
  dependencies = [
    ':common',
    'src/python/pants/base:build_environment',
  ],
)

python_library(
  name = 'confluence_publish',
  sources = ['confluence_publish.py'],
  dependencies = [
    ':common',
    'src/python/pants/BUILD.commons:twitter.common.confluence',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/targets:common',
    'src/python/pants:binary_util',
  ],
)

python_library(
  name = 'console_task',
  sources = ['console_task.py'],
  dependencies = [
    ':common',
  ],
)

python_library(
  name = 'dependees',
  sources = ['dependees.py'],
  dependencies = [
    ':common',
    ':console_task',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:build_file',
    'src/python/pants/base:build_file_context',
    'src/python/pants/base:target',
    'src/python/pants/targets:common',
  ],
)

python_library(
  name = 'dependencies',
  sources = ['dependencies.py'],
  dependencies = [
    ':common',
    ':console_task',
    'src/python/pants/targets:jvm',
    'src/python/pants/targets:python',
  ],
)

python_library(
  name = 'depmap',
  sources = ['depmap.py'],
  dependencies = [
    ':common',
    ':console_task',
    'src/python/pants/targets:jvm',
  ],
)

python_library(
  name = 'detect_duplicates',
  sources = ['detect_duplicates.py'],
  dependencies = [
    ':common',
    ':jvm_binary_task',
    'src/python/pants/java:jar',
  ],
)

python_library(
  name = 'eclipse_gen',
  sources = ['eclipse_gen.py'],
  resources = globs('templates/eclipse/*.mustache'),
  dependencies = [
    ':common',
    ':ide_gen',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:generator',
  ],
)

python_library(
  name = 'filedeps',
  sources = ['filedeps.py'],
  dependencies = [
    ':common',
    ':console_task',
    'src/python/pants/targets:jvm',
    'src/python/pants/targets:common',
  ],
)

python_library(
  name = 'filemap',
  sources = ['filemap.py'],
  dependencies = [
    ':common',
    ':console_task',
    'src/python/pants/base:build_file',
    'src/python/pants/base:target',
  ],
)

python_library(
  name = 'filter',
  sources = ['filter.py'],
  dependencies = [
    ':common',
    ':console_task',
    'src/python/pants/base:address',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:build_file_aliases',
    'src/python/pants/base:target',
  ],
)

python_library(
  name = 'ide_gen',
  sources = ['ide_gen.py'],
  dependencies = [
    ':checkstyle',
    ':common',
    ':jvm_binary_task',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:target',
    'src/python/pants/goal:phase', # XXX?
    'src/python/pants/targets:jvm',
    'src/python/pants:binary_util',
  ],
)

python_library(
  name = 'idea_gen',
  sources = ['idea_gen.py'],
  resources = globs('templates/idea/*.mustache'),
  dependencies = [
    ':common',
    ':ide_gen',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:generator',
    'src/python/pants/targets:common',
    'src/python/pants/targets:java',
    'src/python/pants/targets:scala',
  ],
)

python_library(
  name = 'ivy_resolve',
  sources = ['ivy_resolve.py'],
  resources = globs('templates/ivy_resolve/*.mustache'),
  dependencies = [
    ':common',
    ':cache_manager',
    ':ivy_utils',  # inline?
    ':nailgun_task',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants:binary_util',
    'src/python/pants/ivy',
  ],
)

python_library(
  name = 'ivy_utils',
  sources = ['ivy_utils.py'],
  dependencies = [
    ':common',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:generator',
    'src/python/pants/base:revision',
    'src/python/pants/base:target',
    'src/python/pants/ivy',
    'src/python/pants/java:util',
  ],
)

python_library(
  name = 'jar_create',
  sources = ['jar_create.py'],
  dependencies = [
    ':common',
    ':javadoc_gen',
    ':scaladoc_gen',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:build_environment',
    'src/python/pants/fs',
    'src/python/pants/java:jar',
    'src/python/pants/targets:jvm',
  ],
)

python_library(
  name = 'jar_publish',
  sources = ['jar_publish.py'],
  resources = globs('templates/jar_publish/*.mustache'),
  dependencies = [
    ':common',
    ':scm_publish',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.config',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/BUILD.commons:twitter.common.log',
    'src/python/pants/base:address',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:generator',
    'src/python/pants/base:target',
    'src/python/pants/ivy',
    'src/python/pants/targets:common',
  ],
)

python_library(
  name = 'javadoc_gen',
  sources = ['javadoc_gen.py'],
  dependencies = [
    ':jvmdoc_gen',
  ],
)

python_library(
  name = 'junit_run',
  sources = ['junit_run.py'],
  dependencies = [
    ':common',
    ':jvm_task',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants:binary_util',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:workunit',
    'src/python/pants/java:util',
    'src/python/pants/targets:java',
  ],
)

python_library(
  name = 'jvm_binary_task',
  sources = ['jvm_binary_task.py'],
  dependencies = [
    ':common',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/targets:jvm',
  ],
)

python_library(
  name = 'jvm_run',
  sources = ['jvm_run.py'],
  dependencies = [
    ':common',
    ':jvm_task',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:workunit',
    'src/python/pants/java:executor',
    'src/python/pants/java:util',
    'src/python/pants/targets:jvm',
  ],
)

python_library(
  name = 'jvm_task',
  sources = ['jvm_task.py'],
  dependencies = [
    ':common',
    'src/python/pants/base:build_environment',
  ],
)

python_library(
  name = 'jvm_tool_bootstrapper',
  sources = ['jvm_tool_bootstrapper.py'],
  dependencies = [
    ':common',
  ],
)

python_library(
  name = 'jvmdoc_gen',
  sources = ['jvmdoc_gen.py'],
  dependencies = [
    ':common',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants:binary_util',
  ],
)

python_library(
  name = 'list_goals',
  sources = ['list_goals.py'],
  dependencies = [
    ':console_task',
    'src/python/pants/goal',
  ],
)

python_library(
  name = 'listtargets',
  sources = ['listtargets.py'],
  dependencies = [
    ':common',
    ':console_task',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:build_file',
    'src/python/pants/base:target',
  ],
)

python_library(
  name = 'markdown_to_html',
  sources = ['markdown_to_html.py'],
  dependencies = [
    '3rdparty/python:elementtree',
    '3rdparty/python:markdown',
    '3rdparty/python:pygments',
    ':common',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:address',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:target',
    'src/python/pants/targets:common',
    'src/python/pants:binary_util',
  ],
)

python_library(
  name = 'minimal_cover',
  sources = ['minimal_cover.py'],
  dependencies = [
    ':console_task',
  ],
)

python_library(
  name = 'nailgun_task',
  sources = ['nailgun_task.py'],
  dependencies = [
    ':common',
    'src/python/pants/java:executor',
    'src/python/pants/java:nailgun_executor',
    'src/python/pants/java:distribution',
    'src/python/pants/java:util',
  ],
)

python_library(
  name = 'pathdeps',
  sources = ['pathdeps.py'],
  dependencies = [
    ':console_task',
  ],
)

python_library(
  name = 'paths',
  sources = ['paths.py'],
  dependencies = [
    ':common',
    ':console_task',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:address',
    'src/python/pants/base:target',
  ],
)

python_library(
  name = 'prepare_resources',
  sources = ['prepare_resources.py'],
  dependencies = [
    ':common',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/goal:products',
  ],
)

python_library(
  name = 'protobuf_gen',
  sources = ['protobuf_gen.py'],
  dependencies = [
    ':common',
    ':code_gen',
    'src/python/pants/BUILD.commons:twitter.common.log',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants:binary_util',
    'src/python/pants/targets:java',
    'src/python/pants/targets:python',
  ],
)

python_library(
  name = 'provides',
  sources = ['provides.py'],
  dependencies = [
    ':common',
    ':ivy_utils',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.contextutil',
    'src/python/pants/targets:jvm',
  ],
)

python_library(
  name = 'roots',
  sources = ['roots.py'],
  dependencies = [
    ':console_task',
    'src/python/pants/targets:common',
  ],
)

python_library(
  name = 'scala_repl',
  sources = ['scala_repl.py'],
  dependencies = [
    ':common',
    ':jvm_task',
    'src/python/pants/base:workunit',
    'src/python/pants/java:util',
  ],
)

python_library(
  name = 'scaladoc_gen',
  sources = ['scaladoc_gen.py'],
  dependencies = [
    ':jvmdoc_gen',
  ],
)

python_library(
  name = 'scalastyle',
  sources = ['scalastyle.py'],
  dependencies = [
    ':common',
    ':nailgun_task',
    'src/python/pants/base:config',
    'src/python/pants/base:target',
    'src/python/pants/process',
  ],
)

python_library(
  name = 'scm_publish',
  sources = ['scm_publish.py'],
  dependencies = [
    ':common',
  ],
)

python_library(
  name = 'scrooge_gen',
  sources = ['scrooge_gen.py'],
  dependencies = [
    ':common',
    ':nailgun_task',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:build_environment',
    'src/python/pants/targets:common',
    'src/python/pants/targets:java',
    'src/python/pants/targets:scala',
    'src/python/pants:thrift_util',
  ],
)

python_library(
  name = 'sorttargets',
  sources = ['sorttargets.py'],
  dependencies = [
    ':common',
    ':console_task',
    'src/python/pants/BUILD.commons:twitter.common.util',
    'src/python/pants/base:target',
  ],
)

python_library(
  name = 'specs_run',
  sources = ['specs_run.py'],
  dependencies = [
    ':common',
    ':jvm_task',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/base:workunit',
    'src/python/pants:binary_util',
    'src/python/pants/java:util',
  ],
)

python_library(
  name = 'targets_help',
  sources = ['targets_help.py'],
  dependencies = [
    ':common',
    ':console_task',
    'src/python/pants/base:target',
    'src/python/pants/targets:common',
  ],
)

python_library(
  name = 'task',
  sources = ['task.py'],
  dependencies = [
    ':cache_manager',
    ':common',
    ':ivy_utils',
    ':jvm_tool_bootstrapper',
    ':task_error',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/base:config',
    'src/python/pants/base:build_invalidator',
    'src/python/pants/base:hash_utils',
    'src/python/pants/base:worker_pool',
    'src/python/pants/base:workunit',
    'src/python/pants/cache',
    'src/python/pants/ivy',
    'src/python/pants/java:executor',
    'src/python/pants/reporting',
  ],
)

python_library(
  name = 'task_error',
  sources = ['task_error.py'],
  dependencies = [
    'src/python/pants/base:build_manual',
  ],
)


"""
XXX this code does not exist on master
python_library(
  name = 'thrift_gemerator',
  sources = ['thrift_gemerator.py'],
  dependencies = [
    ':common',
    ':scm_publish',
    'src/python/pants/BUILD.commons:twitter.common.config',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/targets:ruby_thrift_library',
    'src/python/pants/base:build_environment',
  ],
)
"""

python_library(
  name = 'thrift_gen',
  sources = ['thrift_gen.py'],
  dependencies = [
    ':common',
    ':code_gen',
    'src/python/pants/BUILD.commons:twitter.common.log',
    'src/python/pants/BUILD.commons:twitter.common.collections',
    'src/python/pants/BUILD.commons:twitter.common.dirutil',
    'src/python/pants/base:build_environment',
    'src/python/pants/targets:common',
    'src/python/pants/targets:java',
    'src/python/pants/targets:python',
    'src/python/pants:thrift_util',
  ],
)

python_library(
  name = 'what_changed',
  sources = ['what_changed.py'],
  dependencies = [
    ':common',
    ':console_task',
    ':task_error',
    'src/python/pants/BUILD.commons:twitter.common.lang',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:build_file',
    'src/python/pants/base:target',
    'src/python/pants/scm',
  ],
)
