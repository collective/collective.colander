from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.colander',
      version=version,
      description="A tool to convert a Zope schema to a colander schema",
      long_description=open("README.txt").read() + "\n" +
                       open("TODO.txt").read() + "\n" + 
                       open("HISTORY.txt").read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='colander, zope, schema',
      author='Patrick Gerken',
      author_email='do3ccqrv@googlemail.com',
      url='do3.cc',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'colander',
          'zope.schema'
          # -*- Extra requirements: -*-
      ],
      tests_require=['deform'],
      test_suite = "collective.colander.tests",
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
