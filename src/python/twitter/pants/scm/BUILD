python_library(
  name = 'all',
  dependencies = [
    ':git',
  ]
)

python_library(
  name = 'scm',
  sources = ['__init__.py'],
  dependencies = [
    'src/python/twitter/common/lang',
  ],
)

python_library(
  name = 'git',
  sources = ['git.py'],
  dependencies = [
    ':scm',
    'src/python/twitter/common/log',
  ],
)
