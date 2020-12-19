#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A tool for writing in the International Phonetic Alphabet

IPAPad is a Qt-GUI based plain text editor with special key mappings and
clickable chart components that helps you write phonetic transcriptions in
the International Phonetic Alphabet (IPA).
"""

import sys
import os
import ctypes
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from .main_window import MainWindow
from . import shared


def main():
    """Execute the program's main logic with a graphical (Qt) interface."""
    base_path = os.path.dirname(__file__)
    if os.name == "nt":
        appid = f"florian.{ shared.__title__ }.{ shared.__version__ }" # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
    app = QApplication(sys.argv)
    mw = MainWindow(base_path=base_path)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
