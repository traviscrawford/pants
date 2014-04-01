# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import collections
import os
import sys

from twitter.common.collections import OrderedSet, maybe_list
from twitter.common.lang import Compatibility

from pants.base.address import Address
from pants.base.build_manual import manual
from pants.base.hash_utils import hash_all
from pants.base.source_root import SourceRoot


class TargetDefinitionException(Exception):
  """Thrown on errors in target definitions."""

  def __init__(self, target, msg):
    super(Exception, self).__init__('Error with %s: %s' % (target.address, msg))


class AbstractTarget(object):
  @property
  def has_resources(self):
    """Returns True if the target has an associated set of Resources."""
    return hasattr(self, 'resources') and self.resources

  @property
  def is_exported(self):
    """Returns True if the target provides an artifact exportable from the repo."""
    # TODO(John Sirois): fixup predicate dipping down into details here.
    return self.has_label('exportable') and self.provides

  @property
  def is_jar(self):
    """Returns True if the target is a jar."""
    return False

  @property
  def is_java_agent(self):
    """Returns `True` if the target is a java agent."""
    return self.has_label('java_agent')

  @property
  def is_jvm_app(self):
    """Returns True if the target produces a java application with bundled auxiliary files."""
    return False

  @property
  def is_thrift(self):
    """Returns True if the target has thrift IDL sources."""
    return False

  @property
  def is_jvm(self):
    """Returns True if the target produces jvm bytecode."""
    return self.has_label('jvm')

  @property
  def is_codegen(self):
    """Returns True if the target is a codegen target."""
    return self.has_label('codegen')

  @property
  def is_synthetic(self):
    """Returns True if the target is a synthetic target injected by the runtime."""
    return self.has_label('synthetic')

  @property
  def is_jar_library(self):
    """Returns True if the target is an external jar library."""
    return self.has_label('jars')

  @property
  def is_java(self):
    """Returns True if the target has or generates java sources."""
    return self.has_label('java')

  @property
  def is_apt(self):
    """Returns True if the target exports an annotation processor."""
    return self.has_label('apt')

  @property
  def is_python(self):
    """Returns True if the target has python sources."""
    return self.has_label('python')

  @property
  def is_scala(self):
    """Returns True if the target has scala sources."""
    return self.has_label('scala')

  @property
  def is_scalac_plugin(self):
    """Returns True if the target builds a scalac plugin."""
    return self.has_label('scalac_plugin')

  @property
  def is_test(self):
    """Returns True if the target is comprised of tests."""
    return self.has_label('tests')


@manual.builddict()
class Target(AbstractTarget):
  """The baseclass for all pants targets.

  Handles registration of a target amongst all parsed targets as well as location of the target
  parse context.
  """

  def has_sources(self, extension=''):
    return self.payload.has_sources(extension)

  @property
  def target_base(self):
    return SourceRoot.find(self)
  # def has_resources(self):
  #   return self.payload.has_resources()

  def inject_dependency(self, dependency_address):
    self._build_graph.inject_dependency(dependent=self.address, dependency=dependency_address)

  def sources_relative_to_buildroot(self):
    if self.has_sources():
      return self.payload.sources_relative_to_buildroot()
    else:
      return []

  @classmethod
  def identify(cls, targets):
    """Generates an id for a set of targets."""
    return cls.combine_ids(target.id for target in targets)

  @classmethod
  def maybe_readable_identify(cls, targets):
    """Generates an id for a set of targets.

    If the set is a single target, just use that target's id."""
    return cls.maybe_readable_combine_ids([target.id for target in targets])

  @staticmethod
  def combine_ids(ids):
    """Generates a combined id for a set of ids."""
    return hash_all(sorted(ids))  # We sort so that the id isn't sensitive to order.

  @classmethod
  def maybe_readable_combine_ids(cls, ids):
    """Generates combined id for a set of ids, but if the set is a single id, just use that."""
    ids = list(ids)  # We can't len a generator.
    return ids[0] if len(ids) == 1 else cls.combine_ids(ids)

  def __init__(self, name, address, payload, build_graph, exclusives=None):
    """
    :param string name: The target name.
    :param Address address: The Address that maps to this Target in the BuildGraph
    :param BuildGraph build_graph: The BuildGraph that this Target lives within
    """
    self.name = name
    self.address = address
    self.payload = payload
    self._build_graph = build_graph
    self.description = None
    self.labels = set()
    self.declared_exclusives = collections.defaultdict(set)
    if exclusives is not None:
      for k in exclusives:
        self.declared_exclusives[k].add(exclusives[k])
    self.exclusives = None

  @property
  def cloned_from(self):
    """Returns the target this target was derived from.

    If this target was not derived from another, returns itself.
    """
    return self._build_graph.get_clonal_ancestor(self.address)

  @property
  def traversable_specs(self):
    return []

  @property
  def dependencies(self):
    return [self._build_graph.get_target(dep_address)
            for dep_address in self._build_graph.dependencies_of(self.address)]

  @property
  def dependents(self):
    return [self._build_graph.get_target(dep_address)
            for dep_address in self._build_graph.dependents_of(self.address)]

  @property
  def is_synthetic(self):
    return self.address.is_synthetic

  def get_all_exclusives(self):
    """ Get a map of all exclusives declarations in the transitive dependency graph.

    For a detailed description of the purpose and use of exclusives tags,
    see the documentation of the CheckExclusives task.

    """
    if self.exclusives is None:
      self._propagate_exclusives()
    return self.exclusives

  def _propagate_exclusives(self):
    if self.exclusives is None:
      self.exclusives = collections.defaultdict(set)
      self.add_to_exclusives(self.declared_exclusives)
      # This may perform more work than necessary.
      # We want to just traverse the immediate dependencies of this target,
      # but for a general target, we can't do that. _propagate_exclusives is overridden
      # in subclasses when possible to avoid the extra work.
      self.walk(lambda t: self._propagate_exclusives_work(t))

  def _propagate_exclusives_work(self, target):
    # Note: this will cause a stack overflow if there is a cycle in
    # the dependency graph, so exclusives checking should occur after
    # cycle detection.
    if hasattr(target, "declared_exclusives"):
      self.add_to_exclusives(target.declared_exclusives)
    return None

  def add_to_exclusives(self, exclusives):
    if exclusives is not None:
      for key in exclusives:
        self.exclusives[key] |= exclusives[key]

  @property
  def id(self):
    """A unique identifier for the Target.

    The generated id is safe for use as a path name on unix systems.
    """
    return self.address.path_safe_spec

  @property
  def identifier(self):
    """A unique identifier for the Target.

    The generated id is safe for use as a path name on unix systems.
    """
    return self.id

  def walk(self, work, predicate=None):
    """Walk of this target's dependency graph visiting each node exactly once.

    If a predicate is supplied it will be used to test each target before handing the target to
    work and descending. Work can return targets in which case these will be added to the walk
    candidate set if not already walked.

    :param work: Callable that takes a :py:class:`pants.base.target.Target`
      as its single argument.
    :param predicate: Callable that takes a :py:class:`pants.base.target.Target`
      as its single argument and returns True if the target should passed to ``work``.
    """
    if not callable(work):
      raise ValueError('work must be callable but was %s' % work)
    if predicate and not callable(predicate):
      raise ValueError('predicate must be callable but was %s' % predicate)
    self._build_graph.walk_transitive_dependency_graph([self.address], work, predicate)

  @manual.builddict()
  def with_description(self, description):
    """Set a human-readable description of this target."""
    self.description = description
    return self

  def add_labels(self, *label):
    self.labels.update(label)

  def remove_label(self, label):
    self.labels.remove(label)

  def has_label(self, label):
    return label in self.labels

  def __eq__(self, other):
    return isinstance(other, Target) and self.address == other.address

  def __hash__(self):
    return hash(self.address)

  def __ne__(self, other):
    return not self.__eq__(other)

  def __repr__(self):
    return "%s(%s)" % (type(self).__name__, self.address)
