from twitter.pants.base.target import Target


class PythonRequirementLibrary(Target):
  def __init__(self, requirements=None, *args, **kwargs):
    super(PythonRequirementLibrary, self).__init__(*args, payload=requirements, **kwargs)
