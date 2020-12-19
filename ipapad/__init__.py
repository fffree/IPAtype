#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Resources:
# Tutorial: http://zetcode.com/gui/pyqt4/menusandtoolbars/
# Default Icon Names: http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html#names
"""
A tool for writing in the International Phonetic Alphabet.

IPAPad is a Qt-GUI based plain text editor with special key mappings and
clickable chart components that helps you write phonetic transcriptions in
the International Phonetic Alphabet (IPA).
"""

#
# Imports
#
from . import shared
#from . import __main__

#
# Module Properties
#
__all__ = ["shared", "widgets", "__main__"]
__author__ = shared.__author__
__contact__ = shared.__contact__
__copyright__ = shared.__copyright__
__license__ = shared.__license__
__date__ = shared.__date__
__version__ = shared.__version__
__title__ = shared.__title__

#
# Is someone trying to run IPAtype from this file?
#
if __name__ == '__main__':
    print("Please run __main__.py instead of __init__.py.")
