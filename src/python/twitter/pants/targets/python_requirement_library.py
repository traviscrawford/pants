# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from pants.base.target import Target


class PythonRequirementLibrary(Target):
  def __init__(self, requirements=None, *args, **kwargs):
    super(PythonRequirementLibrary, self).__init__(*args, payload=requirements, **kwargs)
