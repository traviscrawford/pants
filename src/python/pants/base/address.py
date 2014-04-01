# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os

from twitter.common.lang import Compatibility

from pants.base.build_file import BuildFile


def parse_spec(spec, relative_to=''):
  if not isinstance(spec, basestring):
    print "Spec %s is not a string!" % spec
  spec_parts = spec.rsplit(':', 1)
  if len(spec_parts) == 1:
    spec_path = spec_parts[0]
    assert spec_path, (
      'Attempted to parse a bad spec string {spec}: empty spec string'
      .format(spec=spec)
    )
    target_name = os.path.basename(spec_path)
    return spec_path, target_name

  spec_path, target_name = spec_parts
  if not spec_path:
    spec_path = relative_to
  return spec_path, target_name


class Address(object):
  """A target address.

  An address is a unique name representing a
  :class:`pants.base.target.Target`. Its composed of the
  path from the root of the repo to the Target plus the target name.

  While not their only use, a noteworthy use of addresses is specifying
  target dependencies. For example:

  ::

    some_target(name='mytarget',
      dependencies=['path/to/buildfile:targetname']
    )

  Where ``path/to/buildfile:targetname`` is the dependent target address.
  """

  # @classmethod
  # def parse(cls, root_dir, spec, is_relative=True):
  #   """Parses the given spec into an Address.

  #   An address spec can be one of:
  #   1.) the (relative) path of a BUILD file
  #   2.) the (relative) path of a directory containing a BUILD file child
  #   3.) either of 1 or 2 with a ':[target name]' suffix
  #   4.) a bare ':[target name]' indicating the BUILD file to use is the one in the current directory

  #   If the spec does not have a target name suffix the target name is taken to be the same name
  #   as the BUILD file's parent directory.  In this way the containing directory name
  #   becomes the 'default' target name for a BUILD file.

  #   If there is no BUILD file at the path pointed to, or if there is but the specified target name
  #   is not defined in the BUILD file, an IOError is raised.
  #   """

  #   if spec.startswith(':'):
  #     spec = '.' + spec
  #   parts = spec.split(':', 1)
  #   path = parts[0]
  #   if is_relative:
  #     path = os.path.relpath(os.path.abspath(path), root_dir)
  #   buildfile = BuildFile(root_dir, path)

  #   name = os.path.basename(os.path.dirname(buildfile.relpath)) if len(parts) == 1 else parts[1]
  #   return Address(buildfile, name)

  def __init__(self, spec_path, target_name):
    """
    :param string spec_path: The path from the root of the repo to this Target.
    :param string target_name: The name of a target this Address refers to.
    """
    norm_path = os.path.normpath(spec_path)
    self.spec_path = norm_path if norm_path != '.' else ''
    self.target_name = target_name

  @property
  def spec(self):
    return '{spec_path}:{target_name}'.format(spec_path=self.spec_path,
                                              target_name=self.target_name)
  @property
  def path_safe_spec(self):
    return ('{safe_spec_path}.{target_name}'
            .format(safe_spec_path=self.spec_path.replace(os.sep, '.'),
                    target_name=self.target_name))

  @property
  def relative_spec(self):
    return ':{target_name}'.format(target_name=self.target_name)

  @property
  def is_synthetic(self):
    return False

  def reference(self, referencing_path=None):
    """How to reference this address in a BUILD file."""
    if referencing_path and self.spec_path == referencing_path:
      return self.relative_spec
    elif os.path.basename(self.spec_path) != self.target_name:
      self.spec
    else:
      return self.spec_path

  def __eq__(self, other):
    return (other and
            self.spec_path == other.spec_path and
            self.target_name == other.target_name)

  def __hash__(self):
    return hash((self.spec_path, self.target_name))

  def __ne__(self, other):
    return not self.__eq__(other)

  def __repr__(self):
    return self.spec


class BuildFileAddress(Address):
  def __init__(self, build_file, target_name=None):
    self.build_file = build_file
    spec_path = os.path.dirname(build_file.relpath)
    default_target_name = os.path.basename(spec_path)
    super(BuildFileAddress, self).__init__(spec_path=spec_path,
                                           target_name=target_name or default_target_name)

  def __repr__(self):
    return ("BuildFileAddress({build_file}, {target_name})"
            .format(build_file=self.build_file,
                    target_name=self.target_name))


class SyntheticAddress(Address):
  def __init__(self, spec, relative_to=''):
    spec_path, target_name = parse_spec(spec, relative_to=relative_to)
    super(SyntheticAddress, self).__init__(spec_path=spec_path, target_name=target_name)

  def __repr__(self):
    return "SyntheticAddress({spec})".format(spec=self.spec)

  @property
  def is_synthetic(self):
    return True
