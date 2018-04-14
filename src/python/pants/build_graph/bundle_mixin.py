# coding=utf-8
# Copyright 2018 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import os.path

from pants.base.build_environment import get_buildroot
from pants.base.exceptions import TargetDefinitionException
from pants.fs import archive
from pants.util.dirutil import absolute_symlink, safe_mkdir, safe_mkdir_for
from pants.util.fileutil import atomic_copy


class BundleMixin(object):
  @staticmethod
  def get_bundle_dir(results_dir, name):
    return os.path.join(results_dir, '{}-bundle'.format(name))

  def symlink_bundles(self, app, bundle_dir):
    """For each bundle in the given app, symlinks relevant matched paths.

    Validates that at least one path was matched by a bundle.
    """
    for bundle_counter, bundle in enumerate(app.bundles):
      count = 0
      for path, relpath in bundle.filemap.items():
        bundle_path = os.path.join(bundle_dir, relpath)
        count += 1
        if os.path.exists(bundle_path):
          continue

        if os.path.isfile(path):
          safe_mkdir(os.path.dirname(bundle_path))
          os.symlink(path, bundle_path)
        elif os.path.isdir(path):
          safe_mkdir(bundle_path)

      if count == 0:
        raise TargetDefinitionException(app.target,
                                        'Bundle index {} of "bundles" field '
                                        'does not match any files.'.format(bundle_counter))

  def publish_results(self, dist_dir, use_basename_prefix, vt, bundle_dir, archivepath, id, archive_ext):
    """Publish a copy of the bundle and archive from the results dir in dist."""
    # TODO (from mateor) move distdir management somewhere more general purpose.
    name = vt.target.basename if use_basename_prefix else id
    bundle_copy = os.path.join(dist_dir, '{}-bundle'.format(name))
    absolute_symlink(bundle_dir, bundle_copy)
    self.context.log.info(
      'created bundle copy {}'.format(os.path.relpath(bundle_copy, get_buildroot())))

    if archivepath:
      ext = archive.archive_extensions.get(archive_ext, archive_ext)
      archive_copy = os.path.join(dist_dir,'{}.{}'.format(name, ext))
      safe_mkdir_for(archive_copy)  # Ensure parent dir exists
      atomic_copy(archivepath, archive_copy)
      self.context.log.info(
        'created archive copy {}'.format(os.path.relpath(archive_copy, get_buildroot())))
