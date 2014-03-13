python_library(
  name = 'goal',
  sources = ['__init__.py'],
  dependencies = [
    ':error',
    ':context',
    ':group',
    ':phase',
    ':run_tracker',
    'src/python/twitter/pants/base:build_manual',
    'src/python/twitter/pants/tasks:task',
  ],
)

python_library(
  name = 'aggregated_timings',
  sources = ['aggregated_timings.py'],
  dependencies = [
    'src/python/twitter/common/dirutil',
  ]
)

# why is this in goal?
python_library(
  name = 'artifact_cache_stats',
  sources = ['artifact_cache_stats.py'],
  dependencies = [
    'src/python/twitter/common/dirutil',
  ]
)

python_library(
  name = 'context',
  sources = ['context.py'],
  dependencies = [
    ':products',
    'src/python/twitter/common/collections',
    'src/python/twitter/common/dirutil',
    'src/python/twitter/common/process',
    'src/python/twitter/pants/base:build_environment',
    'src/python/twitter/pants/base:parse_context',
    'src/python/twitter/pants/base:target',
    'src/python/twitter/pants/base:workunit',
    'src/python/twitter/pants/java:distribution',  # XXX(fixme)
    'src/python/twitter/pants/reporting',
    'src/python/twitter/pants/targets:all',  # XXX(fixme)
  ],
)

python_library(
  name = 'error',
  sources = ['error.py'],
)

python_library(
  name = 'group',
  sources = ['group.py'],
)

python_library(
  name = 'initialize_reporting',  # XXX shouldn't this be in reporting?!
  sources = ['initialize_reporting.py'],
  dependencies = [
    'src/python/twitter/common/dirutil',
    'src/python/twitter/common/lang',
    'src/python/twitter/pants/reporting',
  ],
)

python_library(
  name = 'phase',
  sources = ['phase.py'],
  dependencies = [
    ':error',
    'src/python/twitter/pants/base:build_manual',
  ],
)

python_library(
  name = 'products',
  sources = ['products.py'],
  dependencies = [
    'src/python/twitter/common/collections',
  ],
)

python_library(
  name = 'run_tracker',
  sources = ['run_tracker.py'],
  dependencies = [
    ':aggregated_timings',
    ':artifact_cache_stats',
    'src/python/twitter/pants/base:run_info',
    'src/python/twitter/pants/base:worker_pool',
    'src/python/twitter/pants/base:workunit',
    'src/python/twitter/pants/reporting',
    'src/python/twitter/pants/base:config',
  ],
)

