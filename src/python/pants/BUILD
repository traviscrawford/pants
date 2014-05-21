# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

dependencies(
  name = 'pants',
  dependencies = [
    pants('src/python/pants/bin:pants'),
  ],
).with_description('An alias for the pants binary target.')

python_library(
  name = 'pants-packaged',

  # TODO(wickman) This version should be automatically pulled in from pants.version
  provides=setup_py(
    name='pantsbuild.pants',
    version='0.0.17',
    description="Twitter's pants build tool.",
    url='https://github.com/pantsbuild/pants',
    license='Apache License, Version 2.0',
    zip_safe=True,
    namespace_packages=['pants'],
    classifiers=[
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
    ]
  ).with_binaries(
    # TODO(John Sirois): Switch back when target cycles have been sorted out.
    # pants=pants('src/python/pants/bin:pants'),
    pants=pants(':_pants_transitional_publishable_binary_'),
  )
)

import urllib

from pants.tasks.confluence_publish import ConfluencePublish


def confluence_url_builder(page, config):
  title = config['title']
  return title, 'https://confluence.twitter.biz/display/%s/%s' % ( 
    config['space'],
    urllib.quote_plus(title)
  )
confluence = wiki(name='confluence',
                        url_builder=confluence_url_builder)

class TwitterConfluence(ConfluencePublish):
  def wiki(self):
    return confluence
  def api(self):
    return 'confluence2'

goal(
  name='confluence',
  action=TwitterConfluence,
  dependencies=['markdown']
).install().with_description('Publish one or more confluence pages.')


page(name='readme',
  source='README.md',
  provides=[
    wiki_artifact(
      wiki=pants(':confluence'),
      space='~travis',
      title='test_page',
    ),
  ],
)


# XXX move into base or thrift
python_library(
  name = 'binary_util',
  sources = ['binary_util.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.contextutil'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
    pants('3rdparty/python/twitter/commons:twitter.common.log'),
    pants('src/python/pants/base:config'),
    pants('src/python/pants/base:exceptions'),
  ],
)

python_library(
  name = 'thrift_util',
  sources = ['thrift_util.py'],
  dependencies = [
    pants(':binary_util'),
  ],
)
