# ==================================================================================================
# Copyright 2011 Twitter, Inc.
# --------------------------------------------------------------------------------------------------
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this work except in compliance with the License.
# You may obtain a copy of the License in the LICENSE file, or at:
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==================================================================================================

python_library(
  name = 'base-test',
  sources = ['base_build_root_test.py'],
  dependencies = [
    'src/python/twitter/common/dirutil',
    'src/python/twitter/pants/base:address',
    'src/python/twitter/pants/base:build_root',
    'src/python/twitter/pants/base:target',
    'src/python/twitter/pants/targets:common',
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
    'src/python/twitter/common/contextutil',
    'src/python/twitter/common/dirutil',
    'src/python/twitter/common/lang',
    'src/python/twitter/pants:thrift_util',
  ]
)

python_test_suite(
  name = 'all',
  dependencies = [
    ':test_maven_layout',
    ':test_thrift_util',
    'tests/python/twitter/pants/base',
    'tests/python/twitter/pants/cache',
    'tests/python/twitter/pants/commands',
    'tests/python/twitter/pants/engine',
    'tests/python/twitter/pants/fs',
    'tests/python/twitter/pants/java',
    'tests/python/twitter/pants/net',
    'tests/python/twitter/pants/process',
    'tests/python/twitter/pants/python',
    'tests/python/twitter/pants/reporting',
    'tests/python/twitter/pants/scm',
    'tests/python/twitter/pants/targets',
    'tests/python/twitter/pants/tasks',
  ]
)
