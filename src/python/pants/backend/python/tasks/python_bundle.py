# coding=utf-8
# Copyright 2018 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import os

from pants.backend.python.targets.python_app import PythonApp
from pants.base.build_environment import get_buildroot
from pants.build_graph.bundle_mixin import BundleMixin
from pants.fs import archive
from pants.task.task import Task
from pants.util.dirutil import safe_mkdir


class PythonBundle(BundleMixin, Task):
  """Create an archive bundle of PythonApp targets."""

  _DEPLOYABLE_ARCHIVES = 'deployable_archives'
  _PEX_ARCHIVES = 'pex_archives'

  @classmethod
  def product_types(cls):
    return [cls._DEPLOYABLE_ARCHIVES]

  @classmethod
  def prepare(cls, options, round_manager):
    super(PythonBundle, cls).prepare(options, round_manager)
    round_manager.require_data(cls._PEX_ARCHIVES)

  @staticmethod
  def _get_archive_path(vt):
    ext = archive.archive_extensions.get(vt.target.payload.archive, vt.target.payload.archive)
    filename = '{}.{}'.format(vt.target.id, ext)
    return os.path.join(vt.results_dir, filename) if vt.target.payload.archive else ''

  @property
  def create_target_dirs(self):
    return True

  def __init__(self, *args, **kwargs):
    super(PythonBundle, self).__init__(*args, **kwargs)
    self._outdir = self.get_options().pants_distdir

  def execute(self):
    targets_to_bundle = self.context.targets(PythonApp.is_python_app)

    with self.invalidated(targets_to_bundle, invalidate_dependents=True) as invalidation_check:
      bundle_archive_product = self.context.products.get(self._DEPLOYABLE_ARCHIVES)

      for vt in invalidation_check.all_vts:
        bundle_dir = self.get_bundle_dir(vt.results_dir, vt.target.name)
        archiver = archive.archiver(vt.target.payload.archive) if vt.target.payload.archive else None
        archive_path = self._get_archive_path(vt)

        if not vt.valid:  # Only recreate the bundle/archive if it's changed
          self._bundle(vt.target, bundle_dir)
          if vt.target.payload.archive:
            archive_path = archiver.create(bundle_dir, self._outdir, vt.target.id)

        if archiver:
          bundle_archive_product.add(
            vt.target, os.path.dirname(archive_path)).append(os.path.basename(archive_path))
          self.context.log.info(
            'created {}'.format(os.path.relpath(archive_path, get_buildroot())))

        if vt.target in self.context.target_roots:  # Always publish bundle/archive in dist
          self.publish_results(self.get_options().pants_distdir,
                               False,
                               vt,
                               bundle_dir,
                               archive_path,
                               vt.target.id,
                               vt.target.payload.archive)

  def _bundle(self, target, bundle_dir):
    self.context.log.debug('creating {}'.format(os.path.relpath(bundle_dir, get_buildroot())))
    safe_mkdir(bundle_dir, clean=True)
    binary_path = self._get_binary_path(target)
    os.symlink(binary_path, os.path.join(bundle_dir, os.path.basename(binary_path)))
    self.symlink_bundles(target, bundle_dir)

  def _get_binary_path(self, target):
    pex_archives = self.context.products.get(self._PEX_ARCHIVES)
    for basedir, filenames in pex_archives.get(target.binary).items():
      for filename in filenames:
        return os.path.join(basedir, filename)
