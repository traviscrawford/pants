# ==================================================================================================
# Copyright 2013 Twitter, Inc.
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

import os
import pytest
from textwrap import dedent
import unittest

from contextlib import contextmanager

from twitter.common.contextutil import pushd, temporary_dir
from twitter.common.dirutil import touch

from twitter.pants.base.address import BuildFileAddress, SyntheticAddress
from twitter.pants.base.build_file import BuildFile
from twitter.pants.base.build_file_parser import BuildFileParser
from twitter.pants.base.build_environment import set_buildroot
from twitter.pants.base.target import Target
from twitter.pants.graph.build_graph import BuildGraph


class FakeTarget(Target):
  def __init__(self, *args, **kwargs):
    super(FakeTarget, self).__init__(*args, payload=None, **kwargs)


class BuildFileParserTest(unittest.TestCase):
  @contextmanager
  def workspace(self, *buildfiles):
    with temporary_dir() as root_dir:
      set_buildroot(root_dir)
      with pushd(root_dir):
        for buildfile in buildfiles:
          touch(os.path.join(root_dir, buildfile))
        yield os.path.realpath(root_dir)

  def test_noop_parse(self):
    with self.workspace('BUILD') as root_dir:
      parser = BuildFileParser(root_dir=root_dir,
                               exposed_objects={},
                               path_relative_utils={},
                               target_alias_map={})
      build_file = BuildFile(root_dir, '')
      parser.parse_build_file(build_file)
      registered_proxies = set(parser._target_proxy_by_address.values())
      self.assertEqual(len(registered_proxies), 0)

  def test_trivial_target(self):
    with self.workspace('BUILD') as root_dir:
      def fake_target(*args, **kwargs):
        assert False, "This fake target should never be called in this test!"

      parser = BuildFileParser(root_dir=root_dir,
                               exposed_objects={},
                               path_relative_utils={},
                               target_alias_map={'fake': fake_target})

      with open(os.path.join(root_dir, 'BUILD'), 'w') as build:
        build.write('''fake(name='foozle')''')

      build_file = BuildFile(root_dir, 'BUILD')
      parser.parse_build_file(build_file)
      registered_proxies = set(parser._target_proxy_by_address.values())

    self.assertEqual(len(registered_proxies), 1)
    proxy = registered_proxies.pop()
    self.assertEqual(proxy.name, 'foozle')
    self.assertEqual(proxy.address, BuildFileAddress(build_file, 'foozle'))
    self.assertEqual(proxy.target_type, fake_target)

  def test_exposed_object(self):
    with self.workspace('BUILD') as root_dir:
      parser = BuildFileParser(root_dir=root_dir,
                               exposed_objects={'fake_object': object()},
                               path_relative_utils={},
                               target_alias_map={})

      with open(os.path.join(root_dir, 'BUILD'), 'w') as build:
        build.write('''fake_object''')

      build_file = BuildFile(root_dir, 'BUILD')
      parser.parse_build_file(build_file)
      registered_proxies = set(parser._target_proxy_by_address.values())

    self.assertEqual(len(registered_proxies), 0)

  def test_path_relative_util(self):
    with self.workspace('a/b/c/BUILD') as root_dir:
      def path_relative_util(foozle, rel_path):
        self.assertEqual(rel_path, 'a/b/c')

      parser = BuildFileParser(root_dir=root_dir,
                               exposed_objects={},
                               path_relative_utils={'fake_util': path_relative_util},
                               target_alias_map={})

      with open(os.path.join(root_dir, 'a/b/c/BUILD'), 'w') as build:
        build.write('''fake_util("baz")''')

      build_file = BuildFile(root_dir, 'a/b/c/BUILD')
      parser.parse_build_file(build_file)
      registered_proxies = set(parser._target_proxy_by_address.values())

    self.assertEqual(len(registered_proxies), 0)

  def test_transitive_closure_spec(self):
    with self.workspace('./BUILD', 'a/BUILD', 'a/b/BUILD') as root_dir:
      with open(os.path.join(root_dir, './BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="foo",
               dependencies=[
                 'a',
               ])
        '''))

      with open(os.path.join(root_dir, 'a/BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="a",
               dependencies=[
                 'a/b:bat',
               ])
        '''))

      with open(os.path.join(root_dir, 'a/b/BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="bat")
        '''))

      parser = BuildFileParser(root_dir=root_dir,
                               exposed_objects={},
                               path_relative_utils={},
                               target_alias_map={'fake': FakeTarget})

      parser.populate_target_proxy_transitive_closure_for_spec(':foo')
      self.assertEqual(len(parser._target_proxy_by_address), 3)

  def test_sibling_build_files(self):
    with self.workspace('./BUILD', './BUILD.foo', './BUILD.bar') as root_dir:
      with open(os.path.join(root_dir, './BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="base",
               dependencies=[
                 ':foo',
               ])
        '''))

      with open(os.path.join(root_dir, './BUILD.foo'), 'w') as build:
        build.write(dedent('''
          fake(name="foo",
               dependencies=[
                 ':bat',
               ])
        '''))

      with open(os.path.join(root_dir, './BUILD.bar'), 'w') as build:
        build.write(dedent('''
          fake(name="bat")
        '''))

      parser = BuildFileParser(root_dir=root_dir,
                               exposed_objects={},
                               path_relative_utils={},
                               target_alias_map={'fake': FakeTarget})

      bar_build_file = BuildFile(root_dir, 'BUILD.bar')
      base_build_file = BuildFile(root_dir, 'BUILD')
      foo_build_file = BuildFile(root_dir, 'BUILD.foo')
      parser.parse_build_file_family(bar_build_file)
      addresses = parser._target_proxy_by_address.keys()
      self.assertEqual(set([bar_build_file, base_build_file, foo_build_file]),
                       set([address.build_file for address in addresses]))
      self.assertEqual(set([':base', ':foo', ':bat']),
                       set([address.spec for address in addresses]))

    # This workspace is malformed, you can't shadow a name in a sibling BUILD file
    with self.workspace('./BUILD', './BUILD.foo', './BUILD.bar') as root_dir:
      with open(os.path.join(root_dir, './BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="base",
               dependencies=[
                 ':foo',
               ])
        '''))

      with open(os.path.join(root_dir, './BUILD.foo'), 'w') as build:
        build.write(dedent('''
          fake(name="foo",
               dependencies=[
                 ':bat',
               ])
        '''))

      with open(os.path.join(root_dir, './BUILD.bar'), 'w') as build:
        build.write(dedent('''
          fake(name="base")
        '''))

      parser = BuildFileParser(root_dir=root_dir,
                               exposed_objects={},
                               path_relative_utils={},
                               target_alias_map={'fake': FakeTarget})
      self.assertRaises(AssertionError,
                        parser.populate_target_proxy_transitive_closure_for_spec,
                        ':base')

