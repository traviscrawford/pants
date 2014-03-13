python_library(
  name = 'reporting',
  sources = globs('*.py'),
  resources = rglobs('assets/*') + globs('templates/*.mustache'),
  dependencies = [
    'src/python/twitter/common/dirutil',
    'src/python/twitter/common/threading',
    'src/python/twitter/pants/base:build_environment',
    'src/python/twitter/pants/base:build_file',
    'src/python/twitter/pants/base:mustache',
    'src/python/twitter/pants/base:workunit',
    'src/python/twitter/pants/goal:run_tracker',  # XXX
    '3rdparty/python:ansicolors',
    '3rdparty/python:pystache',
  ]
)
