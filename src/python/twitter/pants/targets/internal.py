# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import collections
import copy
from functools import partial

from twitter.common.collections import OrderedSet, maybe_list

from pants.base.target import Target, TargetDefinitionException
from pants.targets.anonymous import AnonymousDeps
from pants.targets.external_dependency import ExternalDependency
from pants.targets.jar_dependency import JarDependency


class InternalTarget(Target):
  """A baseclass for targets that support an optional dependency set."""

  class CycleException(Exception):
    """Thrown when a circular dependency is detected."""
    def __init__(self, cycle):
      Exception.__init__(self, 'Cycle detected:\n\t%s' % (
          ' ->\n\t'.join(str(target.address) for target in cycle)
      ))

  @classmethod
  def sort_targets(cls, internal_targets):
    """Returns the targets that internal_targets depend on sorted from most dependent to least."""
    roots = OrderedSet()
    inverted_deps = collections.defaultdict(OrderedSet)  # target -> dependent targets
    visited = set()
    path = OrderedSet()

    def invert(target):
      if target in path:
        path_list = list(path)
        cycle_head = path_list.index(target)
        cycle = path_list[cycle_head:] + [target]
        raise cls.CycleException(cycle)
      path.add(target)
      if target not in visited:
        visited.add(target)
        if getattr(target, 'internal_dependencies', None):
          for internal_dependency in target.internal_dependencies:
            if hasattr(internal_dependency, 'internal_dependencies'):
              inverted_deps[internal_dependency].add(target)
              invert(internal_dependency)
        else:
          roots.add(target)
      path.remove(target)

    for internal_target in internal_targets:
      invert(internal_target)

    ordered = []
    visited.clear()

    def topological_sort(target):
      if target not in visited:
        visited.add(target)
        if target in inverted_deps:
          for dep in inverted_deps[target]:
            topological_sort(dep)
        ordered.append(target)

    for root in roots:
      topological_sort(root)

    return ordered

  def sort(self):
    """Returns a list of targets this target depends on sorted from most dependent to least."""
    return self.sort_targets([self])

  def coalesce(self, discriminator):
    """Returns a list of targets this target depends on sorted from most dependent to least and
    grouped where possible by target type as categorized by the given discriminator.
    """
    return self.coalesce_targets([self], discriminator)

  def __init__(self, name, dependencies, exclusives=None):
    """
    :param string name: The name of this module target, addressable via pants via the
      portion of the spec following the colon.
    :param dependencies: List of :class:`pants.base.target.Target` instances
      this target depends on.
    :type dependencies: list of targets
    """
    Target.__init__(self, name, exclusives=exclusives)
    self._injected_deps = []
    self._processed_dependencies = resolve(dependencies)

    self.add_labels('internal')
    self.dependency_addresses = OrderedSet()

    self._dependencies = OrderedSet()
    self._internal_dependencies = OrderedSet()
    self._jar_dependencies = OrderedSet()

    if dependencies:
      maybe_list(self._processed_dependencies,
                 expected_type=(ExternalDependency, AnonymousDeps, Target),
                 raise_type=partial(TargetDefinitionException, self))

  def add_injected_dependency(self, spec):
    self._injected_deps.append(spec)

  def inject_dependencies(self):
    self.update_dependencies(resolve(self._injected_deps))

  @property
  def dependencies(self):
    self._maybe_apply_deps()
    return self._dependencies

  @property
  def internal_dependencies(self):
    self._maybe_apply_deps()
    return self._internal_dependencies

  @property
  def jar_dependencies(self):
    self._maybe_apply_deps()
    return self._jar_dependencies

  def _maybe_apply_deps(self):
    if self._processed_dependencies is not None:
      self.update_dependencies(self._processed_dependencies)
      self._processed_dependencies = None
    if self._injected_deps:
      self.update_dependencies(resolve(self._injected_deps))
      self._injected_deps = []

  def update_dependencies(self, dependencies):
    if dependencies:
      for dependency in dependencies:
        for resolved_dependency in dependency.resolve():
          self._dependencies.add(resolved_dependency)
          if isinstance(resolved_dependency, InternalTarget):
            self._internal_dependencies.add(resolved_dependency)
      self._jar_dependencies = OrderedSet(filter(lambda tgt: isinstance(tgt, JarDependency),
                                                 self._dependencies - self._internal_dependencies))

  def valid_dependency(self, dep):
    """Subclasses can over-ride to reject invalid dependencies."""
    return True

  def _propagate_exclusives(self):
    # Note: this overrides Target._propagate_exclusives without
    # calling the supermethod. Targets in pants do not necessarily
    # have a dependencies field, or ever have their dependencies
    # available at all pre-resolve. Subtypes of InternalTarget, however,
    # do have well-defined dependency lists in their dependencies field,
    # so we can do a better job propagating their exclusives quickly.
    if self.exclusives is not None:
      return
    self.exclusives = copy.deepcopy(self.declared_exclusives)
    for t in self.dependencies:
      if isinstance(t, Target):
        t._propagate_exclusives()
        self.add_to_exclusives(t.exclusives)
      elif hasattr(t, "declared_exclusives"):
        self.add_to_exclusives(t.declared_exclusives)
