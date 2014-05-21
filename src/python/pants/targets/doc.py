# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from pants.base.payload import ResourcesPayload
from pants.base.target import Target


class WikiArtifact(object):
  def __init__(self, wiki, **kwargs):
    self.wiki = wiki
    self.config = kwargs


class Wiki(Target):
  """Target that identifies a wiki where pages can be published."""

  def __init__(self, name, url_builder, exclusives=None):
    """
    :param string name: The name of this target, which combined with this
      build file defines the target :class:`pants.base.address.Address`.
    :param url_builder: Function that accepts a page target and an optional wiki config dict.
    :returns: A tuple of (alias, fully qualified url).
    """
    Target.__init__(self, name, exclusives=exclusives)
    self.url_builder = url_builder


class Page(Target):
  """Describes a single documentation page.

  Example: ::

     page(name='mypage',
       source='mypage.md',
       provides=[
         wiki_artifact(wiki='address/of/my/wiki',
                      space='my_space',
                      title='my_page',
                      parent='my_parent'),
       ],
     )
  """

  def __init__(self, source, resources=None, provides=None, **kwargs):
    """
    :param string name: The name of this target, which combined with this
      build file defines the target :class:`pants.base.address.Address`.
    :param source: Source of the page in markdown format.
    :param dependencies: List of :class:`pants.base.target.Target` instances
      this target depends on.
    :type dependencies: list of targets
    :param resources: An optional list of Resources objects.
    """
    super(Page, self).__init__(
      payload=ResourcesPayload(sources_rel_path=kwargs.get('address').spec_path,
                               sources=[source]),
      **kwargs)
    self.resources = self._resolve_paths(resources) if resources else []
    self.provides = provides

  @property
  def source(self):
    return list(self.payload.sources)[0]
