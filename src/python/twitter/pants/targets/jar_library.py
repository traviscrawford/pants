# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from functools import partial

from twitter.common.collections import OrderedSet, maybe_list

from pants.base.build_manual import manual
from pants.base.payload import JarLibraryPayload
from pants.base.target import Target
from pants.targets.jar_dependency import JarDependency


@manual.builddict(tags=["anylang"])
class JarLibrary(Target):
  """A set of dependencies that may be depended upon,
  as if depending upon the set of dependencies directly.
  """

  def __init__(self, jars=None, overrides=None, *args, **kwargs):
    """
    :param string name: The name of this target, which combined with this
      build file defines the target :class:`pants.base.address.Address`.
    :param jars: List of :class:`pants.base.target.Target` instances
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
