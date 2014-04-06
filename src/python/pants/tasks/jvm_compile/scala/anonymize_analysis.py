# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import sys

from pants.tasks.jvm_compile.anonymizer import Anonymizer
from pants.tasks.jvm_compile.scala.zinc_analysis_parser import ZincAnalysisParser


def main():
  word_file = sys.argv[1]
  analysis_file = sys.argv[2]
  classes_dir = sys.argv[3]

  with open(word_file, 'r') as infile:
    word_list = infile.read().split()
  anonymizer = Anonymizer({}, word_list)
  analysis = ZincAnalysisParser(classes_dir).parse_from_path(analysis_file)
  analysis.anonymize(anonymizer)
  analysis.write_to_path(analysis_file + '.anon')

if __name__ == '__main__':
  main()
