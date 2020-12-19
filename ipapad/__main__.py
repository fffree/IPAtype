#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import Qt
from widgets import MainWindow

def main():
    app = Qt.QApplication(sys.argv)

    mw = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()