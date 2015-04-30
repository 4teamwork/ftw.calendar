from setuptools import setup, find_packages
import os

version = '2.1.0'

tests_require = ['ftw.testing [splinter]',
                 'ftw.builder',
                 'plone.app.testing',
                 'ftw.testbrowser',
                 ]


setup(name='ftw.calendar',
      version=version,
      description="Calendar view based on fullcalendar",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        "Programming Language :: Python",
        ],
      keywords='',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.calendar',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      install_requires=[
          'setuptools',
          'simplejson',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
