# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from pants.base.address import SyntheticAddress
from pants.base.payload import JvmTargetPayload
from pants.base.target import Target
from pants.targets.exclude import Exclude
from pants.targets.jar_library import JarLibrary
from pants.targets.jarable import Jarable
from pants.targets.resources import Resources


class JvmTarget(Target, Jarable):
  """A base class for all java module targets that provides path and dependency translation."""

  def __init__(self,
               address=None,
               sources=None,
               provides=None,
               excludes=None,
               resources=None,
               configurations=None,
               **kwargs):
    """
    :param string name: The name of this target, which combined with this
      build file defines the target :class:`pants.base.address.Address`.
    :param sources: A list of filenames representing the source code
      this library is compiled from.
    :type sources: list of strings
    :param dependencies: List of :class:`pants.base.target.Target` instances
      this target depends on.
    :type dependencies: list of targets
    :param excludes: One or more :class:`pants.targets.exclude.Exclude` instances
      to filter this target's transitive dependencies against.
    :param configurations: One or more ivy configurations to resolve for this target.
      This parameter is not intended for general use.
    :type configurations: tuple of strings
    """

    payload = JvmTargetPayload(sources=sources,
                               sources_rel_path=address.spec_path,
                               provides=provides,
                               excludes=excludes,
                               configurations=configurations)
    super(JvmTarget, self).__init__(address=address, payload=payload, **kwargs)

    self._resource_specs = resources or []
    self.add_labels('jvm')

  @property
  def jar_dependencies(self):
    jar_deps = set()
    def collect_jar_deps(target):
      if isinstance(target, JarLibrary):
        for jar in target.payload.jars:
          jar_deps.add(jar)

    self.walk(work=collect_jar_deps)
    return jar_deps

  @property
  def has_resources(self):
    return len(self.resources) > 0

  @property
  def traversable_specs(self):
    return self._resource_specs

  @property
  def resources(self):
    return [self._build_graph.get_target(SyntheticAddress(spec)) for spec in self._resource_specs]
