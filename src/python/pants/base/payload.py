# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os
from hashlib import sha1

from twitter.common.collections import OrderedSet
from twitter.common.lang import AbstractClass

from pants.base.build_environment import get_buildroot


def hash_sources(hasher, root_path, rel_path, sources):
  hasher.update(rel_path)
  for source in sorted(sources):
    with open(os.path.join(root_path, rel_path, source), 'r') as f:
      hasher.update(source)
      hasher.update(f.read())


def hash_bundle(bundle):
  hasher = sha1()
  hasher.update(bundle.relative_to)
  hasher.update(bundle.rel_path)
  for abs_path in sorted(bundle.filemap.keys()):
    buildroot_relative_path = os.path.relpath(abs_path, get_buildroot())
    hasher.update(buildroot_relative_path)
    hasher.update(bundle.filemap[abs_path])
    with open(abs_path, 'r') as f:
      hasher.update(f.read())
  return hasher.hexdigest()


class Payload(AbstractClass):
  def invalidation_hash(self, hasher):
    pass
    # raise NotImplementedError

  def has_sources(self, extension):
    raise NotImplementedError

  def has_resources(self, extension):
    raise NotImplementedError


class SourcesMixin(object):
  def has_sources(self, extension=''):
    return any(source.endswith(extension) for source in self.sources)

  def sources_relative_to_buildroot(self):
    return [os.path.join(self.sources_rel_path, source) for source in self.sources]


class BundlePayload(Payload):
  def __init__(self, bundles):
    self.bundles = bundles

  def has_sources(self, extension):
    return False

  def has_resources(self):
    return False

  def invalidation_hash(self, hasher):
    bundle_hashes = [hash_bundle(bundle) for bundle in self.bundles]
    for bundle_hash in sorted(bundle_hashes):
      hasher.update(bundle_hash)


class JvmTargetPayload(Payload, SourcesMixin):
  def __init__(self,
               sources_rel_path=None,
               sources=None,
               provides=None,
               excludes=None,
               configurations=None):
    self.sources_rel_path = sources_rel_path
    self.sources = OrderedSet(sources)
    self.provides = provides or frozenset()
    self.excludes = OrderedSet(excludes)
    self.configurations = OrderedSet(configurations)

  def __hash__(self):
    return hash((self.sources, self.provides, self.excludes, self.configurations))

  def has_resources(self):
    return False

  def invalidation_hash(self, hasher):
    sources_hash = hash_sources(hasher, get_buildroot(), self.sources_rel_path, self.sources)
    if self.provides:
      hasher.update(str(hash(self.provides)))
    for exclude in self.excludes:
      hasher.update(str(hash(exclude)))
    for config in self.configurations:
      hasher.update(config)


class PythonPayload(Payload, SourcesMixin):
  def __init__(self,
               sources_rel_path=None,
               sources=None,
               resources=None,
               requirements=None,
               provides=None,
               compatibility=None):
    self.sources_rel_path = sources_rel_path
    self.sources = sources
    self.resources = resources
    self.requirements = requirements
    self.provides = provides
    self.compatibility = compatibility


class ResourcesPayload(Payload):
  def __init__(self, resources):
    self.resources = resources


class JarLibraryPayload(Payload):
  def __init__(self, jars, overrides):
    self.jars = OrderedSet(jars)
    self.overrides = OrderedSet(overrides)

  def has_sources(self, extension):
    return False

  def has_resources(self):
    return False

  def invalidation_hash(self, hasher):
    hasher.update(str(hash(self.jars)))
    hasher.update(str(hash(self.overrides)))
