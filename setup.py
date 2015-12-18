# -*- coding: utf-8 -*-
from setuptools import setup
from IPAtype import __author__, __contact__, __license__

def readme():
    with open("README.md") as fh:
        return fh.read()

setup(name='IPAtype',
      version=shared.__version__,
      description='A tool for writing in the International Phonetic Alphabet',
      long_description=readme(),
      url='http://florian.me.uk',
      author=__author__,
      author_email=__contact__,
      license=__license__,
      packages=['IPAtype'],
      scripts=['bin/IPAtype'],
      #install_requires=['enchant'], #Any non-standard dependencies
      zip_safe=True)
