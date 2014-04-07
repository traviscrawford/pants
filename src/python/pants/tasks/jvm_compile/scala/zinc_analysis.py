# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import itertools
import json
import os
from collections import defaultdict

from pants.base.build_environment import get_buildroot
from pants.tasks.jvm_compile.analysis import Analysis
from pants.tasks.jvm_compile.anonymizer import Anonymizer


class ZincAnalysisElement(object):
  """Encapsulates one part of the analysis.

  Subclasses specify which section headers comprise this part. Note that data in these objects is
  just text, possibly split on lines or '->'.
  """
  headers = ()  # Override in subclasses.

  @classmethod
  def from_json_obj(cls, obj):
    return cls([obj[header] for header in cls.headers])

  def __init__(self, args):
    # Subclasses can alias the elements of self.args in their own __init__, for convenience.
    self.args = args

  def write(self, outfile, inline_vals=True, rebasings=None):
    self._write_multiple_sections(outfile, self.headers, self.args, inline_vals, rebasings)

  def _write_multiple_sections(self, outfile, headers, reps, inline_vals=True, rebasings=None):
    """Write multiple sections."""
    for header, rep in zip(headers, reps):
      self._write_section(outfile, header, rep, inline_vals, rebasings)

  def _write_section(self, outfile, header, rep, inline_vals=True, rebasings=None):
    """Write a single section.

    Items are sorted, for ease of testing.
    """
    def rebase(txt):
      for rebase_from, rebase_to in rebasings:
        if rebase_to is None:
          if rebase_from in txt:
            return None
        else:
          txt = txt.replace(rebase_from, rebase_to)
      return txt

    rebasings = rebasings or []
    items = []
    for k, vals in rep.iteritems():
      for v in vals:
        item = rebase('%s -> %s%s' % (k, '' if inline_vals else '\n', v))
        if item:
          items.append(item)
    items.sort()
    outfile.write(header + ':\n')
    outfile.write('%d items\n' % len(items))
    for item in items:
      outfile.write(item)
      outfile.write('\n')

  def anonymize_keys(self, anonymizer, arg):
    old_keys = list(arg.keys())
    for k in old_keys:
      vals = arg[k]
      del arg[k]
      arg[anonymizer.convert(k)] = vals

  def anonymize_values(self, anonymizer, arg):
    for k, vals in arg.iteritems():
      arg[k] = [anonymizer.convert(v) for v in vals]

  def anonymize_base64_values(self, anonymizer, arg):
    def random_base64_string(s):
      if s == 'AAAAAAAAAAA=':  # Leave empty objects untouched.
        return s
      else:
        return Anonymizer.random_base64_string()

    for k, vals in arg.iteritems():
      arg[k] = [random_base64_string(v) for v in vals]


class ZincAnalysis(Analysis):
  """Parsed representation of a zinc analysis.

  Note also that all files in keys/values are full-path, just as they appear in the analysis file.
  If you want paths relative to the build root or the classes dir or whatever, you must compute
  those yourself.
  """

  # Implementation of class method required by Analysis.

  FORMAT_VERSION_LINE = 'format version: 4\n'

  @staticmethod
  def merge_dicts(dicts):
    """Merges multiple dicts into one.

    Assumes keys don't overlap.
    """
    ret = defaultdict(list)
    for d in dicts:
      ret.update(d)
    return ret

  @classmethod
  def merge(cls, analyses):
    # Note: correctly handles "internalizing" external deps that must be internal post-merge.

    # Merge relations.
    src_prod = ZincAnalysis.merge_dicts([a.relations.src_prod for a in analyses])
    binary_dep = ZincAnalysis.merge_dicts([a.relations.binary_dep for a in analyses])
    classes = ZincAnalysis.merge_dicts([a.relations.classes for a in analyses])
    used = ZincAnalysis.merge_dicts([a.relations.used for a in analyses])

    class_to_source = dict((v, k) for k, vs in classes.iteritems() for v in vs)

    def merge_dependencies(internals, externals):
      internal = ZincAnalysis.merge_dicts(internals)
      naive_external = ZincAnalysis.merge_dicts(externals)
      external = defaultdict(list)
      for k, vs in naive_external.iteritems():
        for v in vs:
          vfile = class_to_source.get(v)
          if vfile and vfile in src_prod:
            internal[k].append(vfile)  # Internalized.
          else:
            external[k].append(v)  # Remains external.
      return internal, external

    internal, external = merge_dependencies(
      [a.relations.internal_src_dep for a in analyses],
      [a.relations.external_dep for a in analyses])

    internal_pi, external_pi = merge_dependencies(
      [a.relations.internal_src_dep_pi for a in analyses],
      [a.relations.external_dep_pi for a in analyses])

    member_ref_internal, member_ref_external = merge_dependencies(
      [a.relations.member_ref_internal_dep for a in analyses],
      [a.relations.member_ref_external_dep for a in analyses])

    inheritance_internal, inheritance_external = merge_dependencies(
      [a.relations.inheritance_internal_dep for a in analyses],
      [a.relations.inheritance_external_dep for a in analyses])

    relations = Relations((src_prod, binary_dep,
                           internal, external,
                           internal_pi, external_pi,
                           member_ref_internal, member_ref_external,
                           inheritance_internal, inheritance_external,
                           classes, used))

    # Merge stamps.
    products = ZincAnalysis.merge_dicts([a.stamps.products for a in analyses])
    sources = ZincAnalysis.merge_dicts([a.stamps.sources for a in analyses])
    binaries = ZincAnalysis.merge_dicts([a.stamps.binaries for a in analyses])
    classnames = ZincAnalysis.merge_dicts([a.stamps.classnames for a in analyses])
    stamps = Stamps((products, sources, binaries, classnames))

    # Merge APIs.
    internal_apis = ZincAnalysis.merge_dicts([a.apis.internal for a in analyses])
    naive_external_apis = ZincAnalysis.merge_dicts([a.apis.external for a in analyses])
    external_apis = defaultdict(list)
    for k, vs in naive_external_apis.iteritems():
      kfile = class_to_source.get(k)
      if kfile and kfile in src_prod:
        internal_apis[kfile] = vs  # Internalized.
      else:
        external_apis[k] = vs  # Remains external.
    apis = APIs((internal_apis, external_apis))

    # Merge source infos.
    source_infos = SourceInfos((ZincAnalysis.merge_dicts([a.source_infos.source_infos for a in analyses]), ))

    # Merge compilations.
    compilation_vals = sorted(set([x[0] for a in analyses for x in a.compilations.compilations.itervalues()]))
    compilations_dict = defaultdict(list)
    for i, v in enumerate(compilation_vals):
      compilations_dict['%03d' % i] = [v]
    compilations = Compilations((compilations_dict, ))

    compile_setup = analyses[0].compile_setup if len(analyses) > 0 else CompileSetup((defaultdict(list), ))
    return ZincAnalysis(relations, stamps, apis, source_infos, compilations, compile_setup)

  def __init__(self, relations, stamps, apis, source_infos, compilations, compile_setup):
    (self.relations, self.stamps, self.apis, self.source_infos, self.compilations, self.compile_setup) = \
      (relations, stamps, apis, source_infos, compilations, compile_setup)

  # Impelementation of methods required by Analysis.

  def split(self, splits, catchall=False):
    # Note: correctly handles "externalizing" internal deps that must be external post-split.
    buildroot = get_buildroot()
    splits = [set([s if os.path.isabs(s) else os.path.join(buildroot, s) for s in x]) for x in splits]
    if catchall:
      # Even empty sources with no products have stamps.
      remainder_sources = set(self.stamps.sources.keys()).difference(*splits)
      splits.append(remainder_sources)  # The catch-all

    # Split relations.
    src_prod_splits = self._split_dict(self.relations.src_prod, splits)
    binary_dep_splits = self._split_dict(self.relations.binary_dep, splits)
    classes_splits = self._split_dict(self.relations.classes, splits)

    # For historical reasons, external deps are specified as src->class while internal deps are
    # specified as src->src. So we pick a representative class for each src.
    representatives = dict((k, min(vs)) for k, vs in self.relations.classes.iteritems())

    def split_dependencies(all_internal, all_external):
      naive_internals = self._split_dict(all_internal, splits)
      naive_externals = self._split_dict(all_external, splits)

      internals = []
      externals = []
      for naive_internal, external, split in zip(naive_internals, naive_externals, splits):
        internal = defaultdict(list)
        for k, vs in naive_internal.iteritems():
          for v in vs:
            if v in split:
              internal[k].append(v)  # Remains internal.
            else:
              external[k].append(representatives[v])  # Externalized.
        internals.append(internal)
        externals.append(external)
      return internals, externals

    internal_splits, external_splits = \
      split_dependencies(self.relations.internal_src_dep, self.relations.external_dep)
    internal_pi_splits, external_pi_splits = \
      split_dependencies(self.relations.internal_src_dep_pi, self.relations.external_dep_pi)

    member_ref_internal_splits, member_ref_external_splits = \
      split_dependencies(self.relations.member_ref_internal_dep, self.relations.member_ref_external_dep)
    inheritance_internal_splits, inheritance_external_splits = \
      split_dependencies(self.relations.inheritance_internal_dep, self.relations.inheritance_external_dep)
    used_splits = self._split_dict(self.relations.used, splits)

    relations_splits = []
    for args in zip(src_prod_splits, binary_dep_splits,
                    internal_splits, external_splits,
                    internal_pi_splits, external_pi_splits,
                    member_ref_internal_splits, member_ref_external_splits,
                    inheritance_internal_splits, inheritance_external_splits,
                    classes_splits, used_splits):
      relations_splits.append(Relations(args))

    # Split stamps.
    stamps_splits = []
    for src_prod, binary_dep, split in zip(src_prod_splits, binary_dep_splits, splits):
      products_set = set(itertools.chain(*src_prod.values()))
      binaries_set = set(itertools.chain(*binary_dep.values()))
      products = dict((k, v) for k, v in self.stamps.products.iteritems() if k in products_set)
      sources = dict((k, v) for k, v in self.stamps.sources.iteritems() if k in split)
      binaries = dict((k, v) for k, v in self.stamps.binaries.iteritems() if k in binaries_set)
      classnames = dict((k, v) for k, v in self.stamps.classnames.iteritems() if k in binaries_set)
      stamps_splits.append(Stamps((products, sources, binaries, classnames)))

    # Split apis.

    # The splits, but expressed via class representatives of the sources (see above).
    representative_splits = [filter(None, [representatives.get(s) for s in srcs]) for srcs in splits]
    representative_to_internal_api = {}
    for src, rep in representatives.items():
      representative_to_internal_api[rep] = self.apis.internal.get(src)

    # Note that the keys in self.apis.external are classes, not sources.
    internal_api_splits = self._split_dict(self.apis.internal, splits)
    external_api_splits = self._split_dict(self.apis.external, representative_splits)

    # All externalized deps require a copy of the relevant api.
    for external, external_api in zip(external_splits, external_api_splits):
      for vs in external.values():
        for v in vs:
          if v in representative_to_internal_api:
            external_api[v] = representative_to_internal_api[v]

    apis_splits = []
    for args in zip(internal_api_splits, external_api_splits):
      apis_splits.append(APIs(args))

    # Split source infos.
    source_info_splits = \
      [SourceInfos((x, )) for x in self._split_dict(self.source_infos.source_infos, splits)]

    analyses = []
    for relations, stamps, apis, source_infos in zip(relations_splits, stamps_splits, apis_splits, source_info_splits):
      analyses.append(ZincAnalysis(relations, stamps, apis, source_infos, self.compilations, self.compile_setup))

    return analyses

  def write(self, outfile, rebasings=None):
    outfile.write(ZincAnalysis.FORMAT_VERSION_LINE)
    self.relations.write(outfile, rebasings=rebasings)
    self.stamps.write(outfile, rebasings=rebasings)
    self.apis.write(outfile, inline_vals=False, rebasings=rebasings)
    self.source_infos.write(outfile, inline_vals=False, rebasings=rebasings)
    self.compilations.write(outfile, inline_vals=True, rebasings=rebasings)
    self.compile_setup.write(outfile, inline_vals=True, rebasings=rebasings)

  # Extra methods on this class only.

  # Anonymize the contents of this analysis. Useful for creating test data.
  # Note that the resulting file is not a valid analysis, as the base64-encoded serialized objects
  # will be replaced with random base64 strings. So these are useful for testing analysis parsing,
  # splitting and merging, but not for actually reading into Zinc.
  def anonymize(self, anonymizer):
    for element in [self.relations, self.stamps, self.apis, self.source_infos,
                    self.compilations, self.compile_setup]:
      element.anonymize(anonymizer)

  # Write this analysis to JSON.
  def write_json_to_path(self, outfile_path):
    with open(outfile_path, 'w') as outfile:
      self.write_json(outfile)

  def write_json(self, outfile):
    obj = dict(zip(('relations', 'stamps', 'apis', 'source_infos', 'compilations', 'compile_setup'),
                     (self.relations, self.stamps, self.apis, self.source_infos, self.compilations, self.compile_setup)))
    json.dump(obj, outfile, cls=ZincAnalysisJSONEncoder, sort_keys=True, indent=2)

  def _split_dict(self, d, splits):
    """Split a dict by its keys.

    splits: A list of lists of keys.
    Returns one dict per split.
    """
    ret = []
    for split in splits:
      dict_split = defaultdict(list)
      for f in split:
        if f in d:
          dict_split[f] = d[f]
      ret.append(dict_split)
    return ret


class Relations(ZincAnalysisElement):
  headers = ('products', 'binary dependencies',
             # TODO: The following 4 headers will go away after SBT completes the
             # transition to the new headers (the 4 after that).
             'direct source dependencies', 'direct external dependencies',
             'public inherited source dependencies', 'public inherited external dependencies',
             'member reference internal dependencies', 'member reference external dependencies',
             'inheritance internal dependencies', 'inheritance external dependencies',
             'class names', 'used names')

  def __init__(self, args):
    super(Relations, self).__init__(args)
    (self.src_prod, self.binary_dep,
     self.internal_src_dep, self.external_dep,
     self.internal_src_dep_pi, self.external_dep_pi,
     self.member_ref_internal_dep, self.member_ref_external_dep,
     self.inheritance_internal_dep, self.inheritance_external_dep,
     self.classes, self.used) = self.args

  def anonymize(self, anonymizer):
    for a in self.args:
      self.anonymize_values(anonymizer, a)
      self.anonymize_keys(anonymizer, a)


class Stamps(ZincAnalysisElement):
  headers = ('product stamps', 'source stamps', 'binary stamps', 'class names')

  def __init__(self, args):
    super(Stamps, self).__init__(args)
    (self.products, self.sources, self.binaries, self.classnames) = self.args

  def anonymize(self, anonymizer):
    for a in self.args:
      self.anonymize_keys(anonymizer, a)
    self.anonymize_values(anonymizer, self.classnames)


class APIs(ZincAnalysisElement):
  headers = ('internal apis', 'external apis')

  def __init__(self, args):
    super(APIs, self).__init__(args)
    (self.internal, self.external) = self.args

  def anonymize(self, anonymizer):
    for a in self.args:
      self.anonymize_base64_values(anonymizer, a)
      self.anonymize_keys(anonymizer, a)


class SourceInfos(ZincAnalysisElement):
  headers = ("source infos", )

  def __init__(self, args):
    super(SourceInfos, self).__init__(args)
    (self.source_infos, ) = self.args

  def anonymize(self, anonymizer):
    for a in self.args:
      self.anonymize_base64_values(anonymizer, a)
      self.anonymize_keys(anonymizer, a)


class Compilations(ZincAnalysisElement):
  headers = ('compilations', )

  def __init__(self, args):
    super(Compilations, self).__init__(args)
    (self.compilations, ) = self.args

  def anonymize(self, anonymizer):
    pass


class CompileSetup(ZincAnalysisElement):
  headers = ('output mode', 'output directories','compile options','javac options',
             'compiler version', 'compile order')

  def __init__(self, args):
    super(CompileSetup, self).__init__(args)
    (self.output_mode, self.output_dirs, self.compile_options, self.javac_options,
     self.compiler_version, self.compile_order) = self.args

  def anonymize(self, anonymizer):
    self.anonymize_values(anonymizer, self.output_dirs)
    for k, vs in list(self.compile_options.items()):  # Make a copy, so we can del as we go.
      # Remove mentions of custom plugins.
      for v in vs:
        if v.startswith('-Xplugin') or v.startswith('-P'):
          del self.compile_options[k]


class ZincAnalysisJSONEncoder(json.JSONEncoder):
  """A custom encoder for writing analysis elements as JSON.

  Not currently used, but might be useful in the future, e.g., for creating javascript-y
  analysis browsing tools.
  """
  def default(self, obj):
    if isinstance(obj, ZincAnalysisElement):
      ret = {}
      for h, a in zip(type(obj).headers, obj.args):
        ret[h] = a
      return ret
    else:
      super(ZincAnalysisJSONEncoder, self).default(obj)
