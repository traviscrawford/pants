python_library(
  name = 'distribution',
  sources = globs('distribution/*.py'),
  resources = globs('distribution/*.class'),
  dependencies = [
    'src/python/twitter/common/contextutil',
    'src/python/twitter/common/lang',
    'src/python/twitter/common/log',
    'src/python/twitter/pants/base:revision',
  ]
)

python_library(
  name = 'executor',
  sources = ['executor.py'],
  dependencies = [
    ':distribution',
    'src/python/twitter/common/collections',
    'src/python/twitter/common/contextutil',
    'src/python/twitter/common/lang',
    'src/python/twitter/common/log',
  ]
)

python_library(
  name = 'jar',
  sources = globs('jar/*.py'),
  dependencies = [
    'src/python/twitter/common/contextutil',
    'src/python/twitter/common/lang',
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
    'src/python/twitter/common/collections',
    'src/python/twitter/common/dirutil',
    'src/python/twitter/common/lang',
    'src/python/twitter/common/log',
    'src/python/twitter/pants/base:build_environment',
  ],
)

python_library(
  name = 'util',
  sources = ['util.py'],
  dependencies = [
    ':executor',
    ':nailgun_executor',
    'src/python/twitter/pants/base:workunit',
  ],
)

