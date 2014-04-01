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

from functools import partial

from twitter.common.collections import maybe_list, OrderedSet

from twitter.pants.base.build_manual import manual
from twitter.pants.base.payload import JarLibraryPayload
from twitter.pants.base.target import Target

from .jar_dependency import JarDependency


@manual.builddict(tags=["anylang"])
class JarLibrary(Target):
  """A set of dependencies that may be depended upon,
  as if depending upon the set of dependencies directly.
  """

  def __init__(self, jars=None, overrides=None, *args, **kwargs):
    """
    :param string name: The name of this target, which combined with this
      build file defines the target :class:`twitter.pants.base.address.Address`.
    :param jars: List of :class:`twitter.pants.base.target.Target` instances
      this target depends on.
    :param overrides: List of strings, each of which will be recursively resolved to
      any targets that provide artifacts. Those artifacts will override corresponding
      direct/transitive dependencies in the dependencies list.
    :param exclusives: An optional map of exclusives tags. See CheckExclusives for details.
    """
    payload = JarLibraryPayload(jars, overrides)
    super(JarLibrary, self).__init__(payload=payload, *args, **kwargs)
    self.add_labels('jars')

  @property
  def jar_dependencies(self):
    return self.payload.jars

  def _resolve_overrides(self):
    """
    Resolves override jars, and then excludes and re-includes each of them
    to create and return a new dependency set.
    """
    if not self.override_targets:
      return self._pre_override_dependencies

    result = OrderedSet()

    # resolve overrides and fetch all of their "artifact-providing" dependencies
    excludes = set()
    for override_target in self.override_targets:
      # add pre_override deps of the target as exclusions
      for resolved in override_target.resolve():
        excludes.update(self._excludes(resolved))
      # prepend the target as a new target
      result.add(override_target)

    # add excludes for each artifact
    for direct_dep in self._pre_override_dependencies:
      # add relevant excludes to jar dependencies
      for jar_dep in self._jar_dependencies(direct_dep):
        for exclude in excludes:
          jar_dep.exclude(exclude.org, exclude.name)
      result.add(direct_dep)

    return result
