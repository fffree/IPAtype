#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Imports
#

import sys
import traceback
import json
import os
from PyQt4 import Qt
import shared

#
# shared
#

__title__ = shared.__title__
__path__ = os.path.dirname(__file__) #Should be redundant but somehow doesn't always get defined?

class AboutDialog(Qt.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowIcon(Qt.QIcon(os.path.join(__path__, "resources", "icons", "status", "dialog-information.png")))
        self.setStyleSheet("QLabel { padding:15px; background:white }")
        self.setWindowTitle("About %s" % __title__)
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.setLayout(Qt.QVBoxLayout())

        self.tabWidget = Qt.QTabWidget()
        self.layout().addWidget(self.tabWidget)

        self.aboutTab = Qt.QLabel()
        self.aboutTab.setText((
            "<html>"
            " <body>"
            "  <center>"
            "   <p><img src=\"application-icon.png\" width=\"100\" height=\"100\" /></p>"
            "   <p><b><font size=\"20\">%s 2.0.0</font></b></p>"
            "   <p><big>A simple program to help you write transcriptions in the IPA.</big></p>"
            "   <p>(C) 2012-2015 Florian Breit</p>"
            "   <p><a href=\"http://florian.me.uk\">http://florian.me.uk</a></p>"
            "  </center>"
            " </body>"
            "</html>"
        ) % (__title__) )
        self.aboutTab.setText(
            (
                "<html>"
                " <body>"
                "  <center>"
                "   <p><img src=\"{ICON_PATH}\" width=\"100\" height=\"100\" /></p>"
                "   <p><b><font size=\"20\">{PROG_NAME} {PROG_VERSION}</font></b></p>"
                "   <p><big>A simple program to help you write transcriptions in the IPA.</big></p>"
                "   <p>{COPYRIGHT}</p>"
                "   <p><a href=\"http://florian.me.uk\">http://florian.me.uk</a></p>"
                "  </center>"
                " </body>"
                "</html>"
            ).format(
                ICON_PATH=os.path.join(__path__, "resources", "icons", "application-icon.png"),
                PROG_NAME=shared.__title__,
                PROG_VERSION=shared.__version__,
                COPYRIGHT=shared.__copyright__
            )
        )
        self.tabWidget.addTab(self.aboutTab, "About")

        #Not required at present
        #self.creditsTab = Qt.QLabel()
        #self.tabWidget.addTab(self.creditsTab, "Credits")

        self.licenseTab = Qt.QScrollArea()
        self.licenseLabel = Qt.QLabel()
        self.licenseTab.setWidget(self.licenseLabel)
        self.licenseTab.setWidgetResizable(True)
        self.licenseTab.setHorizontalScrollBarPolicy(1) #AlwaysOff
        self.licenseTab.setVerticalScrollBarPolicy(0)   #AsNeeded
        self.licenseLabel.setMinimumWidth(510)
        self.licenseLabel.setWordWrap(True)
        with open(os.path.join(__path__, "resources", "license.html"), encoding="utf8") as fh:
            self.licenseLabel.setText(fh.read())
        self.tabWidget.addTab(self.licenseTab, "License")

        self.buttonBox = Qt.QDialogButtonBox(Qt.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.layout().addWidget(self.buttonBox)

        self.show()


class CharacterMapDialog(Qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(Qt.QIcon(os.path.join(__path__, "resources", "icons", "apps", "accessories-character-map.png")))
        self.setWindowTitle("IPA Character Map")
        self.resize(500, 700)
        self.setLayout(Qt.QVBoxLayout())

        self.tableViewWidget = Qt.QTableView(self)
        self.viewModel = Qt.QStandardItemModel(0, 3, self.tableViewWidget)
        self.proxyModel = Qt.QSortFilterProxyModel(self.tableViewWidget)
        self.proxyModel.setSourceModel(self.viewModel)
        self.proxyModel.setFilterKeyColumn(1)
        self.tableViewWidget.setModel(self.proxyModel)
        self.tableViewWidget.verticalHeader().setVisible(False) #Hide vertical header
        self.tableViewWidget.horizontalHeader().setStretchLastSection(True) #Make widget stretch horizontally
        self.tableViewWidget.setSortingEnabled(True)
        self.layout().addWidget(self.tableViewWidget)

        self.buildModel()
        self.tableViewWidget.resizeColumnsToContents()
        #self.tableViewWidget.sortByColumn(2, Qt.QTableView.AscendingOrder)

        self.filterLabel = Qt.QLabel("Search:")
        self.filterLabel.setToolTip("Search for a character by it's description (regular expressions are supported)")
        self.filterEdit = Qt.QLineEdit("")
        self.filterEdit.textChanged.connect(self.actionFilter)
        self.filterContainer = Qt.QWidget(self)
        self.filterContainer.setLayout(Qt.QHBoxLayout())
        self.filterContainer.layout().addWidget(self.filterLabel)
        self.filterContainer.layout().addWidget(self.filterEdit)
        self.layout().addWidget(self.filterContainer)

        self.buttonBox = Qt.QDialogButtonBox(Qt.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.layout().addWidget(self.buttonBox)

        self.show()

        self.filterEdit.setFocus()

    def actionFilter(self, text):
        print(text)
        search = Qt.QRegExp(text, Qt.Qt.CaseInsensitive, Qt.QRegExp.RegExp)
        self.proxyModel.setFilterRegExp(search)

    def buildModel(self):
        self.viewModel.setHorizontalHeaderLabels(("Symbol", "Description", "Shortcut"))
        for symbol, description in shared.IPAchars.items():
            item = (
                Qt.QStandardItem(" "+symbol),
                Qt.QStandardItem(description['name']),
                Qt.QStandardItem(description['shortcut'])
            )
            self.viewModel.appendRow(item)


class ChartButton(Qt.QPushButton):
    def __init__(self, label, parent, tooltip=None, statustip=None):
        super().__init__(label, parent)
        self.setToolTip(tooltip)
        self.setStatusTip(statustip)

    def dummy(self):
        raise NotImplementedError


class ChartWidget(Qt.QWidget):
    def __init__(self, parent):
        super().__init__(parent)


class Document(Qt.QTextDocument):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDefaultFont(Qt.QFont("Times, SansSerif", 14))
        self.filename = None

    def fromFile(filename, parent=None):
        with open(filename) as fh:
            text = ''.join(fh.readlines())
        doc = Document(parent)
        doc.setPlainText(text)
        doc.setFilename(filename)
        return doc

    def setFilename(self, filename):
        self.filename = filename

    def getFilename(self):
        return self.filename

class ErrorMessage(Qt.QMessageBox):
    def __init__(self, parent=None, short=None, long=None, detail=None, type=Qt.QMessageBox.Critical):
        if(long is None):
            if(short is None):
                long = "An unknown error occurred."
            else:
                long = ""
        if(short is None):
            short = "Unknown error."
        message = "<p><b>%s</b></p><p>%s</p>" % (short, long)
        if(parent is None):
            super().__init__()
        else:
            super().__init__(parent)
        self.setWindowTitle("Error")
        self.setText(message)
        self.setStandardButtons(Qt.QMessageBox.Ok)
        self.setIcon(type)
        if(detail is not None):
            if(isinstance(detail, Exception)):
                dname = sys.exc_info()[0].__name__
                dmsg = sys.exc_info()[1]
                dtb = traceback.format_exc()
                detail = "%s %s\n\n%s" % (dname, dmsg, dtb)
                print(detail)
                self.setDetailedText(detail)
            else:
                self.setDetailedText(detail)
        self.exec()


class MainWindow(Qt.QMainWindow):
    def __init__(self):
        #Initialise window
        super().__init__()
        #Initialise components
        self.initSettings()
        self.initActions()
        self.initShortcuts()
        self.initUI()
        #Load file or start a new file and enable writer widget
        self.actionNew()

    def actionClear(self):
        self.topWidget.clear()

    def actionClose(self):
        #IMPLEMENT check to make sure file doesn't contain unsaved changes
        self.topWidget.setDocument(Document())
        self.topWidget.setEnabled(False)
        self.updateWindowTitle()

    def actionCopy(self):
        self.topWidget.copy()

    def actionCut(self):
        self.topWidget.cut()

    def actionDisplayAbout(self):
        AboutDialog(self)

    def actionDisplayChrMap(self):
        CharacterMapDialog(self)

    def actionExit(self):
        self.close()

    def actionNew(self):
        #IMPLEMENT check to make sure current file doesn't contain unsaved changes
        doc = Document()
        self.topWidget.setDocument(doc)
        self.topWidget.setEnabled(True)
        self.updateWindowTitle()
        self.statusBar().showMessage("Initialised new document")

    def actionOpen(self):
        #IMPLEMENT check to make sure current file doesn't contain unsaved changes
        #Would be useful to implement an extra field to select encoding
        filename = Qt.QFileDialog.getOpenFileName(self, "Open Document", None, "Text Documents (*.txt);;All Files (*)")
        if filename:
            try:
                doc = Document.fromFile(filename, self)
            except (UnicodeDecodeError, IOError) as err:
                if isinstance(err, UnicodeDecodeError):
                    emsg = "The file's encoding is not compatible with Unicode (UTF-8)."
                if isinstance(err, IOError):
                    emsg = "The file could not be opened."
                ErrorMessage(
                    self,
                    "Error opening file",
                    emsg,
                    err,
                    Qt.QMessageBox.Warning
                )
                return False
            doc.setModified(False)
            self.topWidget.setDocument(doc)
            self.topWidget.setEnabled(True)
            self.updateWindowTitle()
            self.statusBar().showMessage("Successfully loaded %s" % filename)

    def actionPaste(self):
        self.topWidget.paste()

    def actionRedo(self):
        self.topWidget.redo()

    def actionSave(self):
        raise NotImplementedError

    def actionSaveAs(self):
        raise NotImplementedError

    def applySettings(settings, self):
        raise NotImplementedError

    def actionShowToolbar(self, value):
        self.settings.show_toolbar = value
        self.fileToolBar.setVisible(value)
        self.editToolBar.setVisible(value)
        self.bracketsToolBar.setVisible(value)
        if(value):
            self.statusBar().showMessage("Toolbars are now visible")
        else:
            self.statusBar().showMessage("Toolbars are now hidden")

    def actionTypeIPA(self, checked):
        if(checked):
            self.settings.type_ipa = True
            self.topWidget.setTransliterate(True)
            self.statusBar().showMessage("Now typing in IPA mode")
        else:
            self.settings.type_ipa = False
            self.topWidget.setTransliterate(False)
            self.statusBar().showMessage("Now typing in normal text mode")

    def actionUndo(self):
        self.topWidget.undo()

    def actionX(self):
        raise NotImplementedError

    #def action(self):
    #    self.topWidget.()

    def closeEvent(self, event):
        reply = Qt.QMessageBox.question(
            self, __title__,
            "Are you sure you want to quit?",
            Qt.QMessageBox.Yes | Qt.QMessageBox.No,
            Qt.QMessageBox.No
        )
        if reply == Qt.QMessageBox.Yes:
            self.storeSettings()
            event.accept()
        else:
            event.ignore()

    def createMenu(self):
        main = self.menuBar()

        file = main.addMenu("&File")
        file.addAction(self.actions['new'])
        file.addAction(self.actions['open'])
        file.addAction(self.actions['save'])
        file.addAction(self.actions['save_as'])
        file.addAction(self.actions['close'])
        file.addSeparator()
        file.addAction(self.actions['exit'])

        edit = main.addMenu("&Edit")
        edit.addAction(self.actions['undo'])
        edit.addAction(self.actions['redo'])
        edit.addSeparator()
        edit.addAction(self.actions['clear'])
        edit.addAction(self.actions['cut'])
        edit.addAction(self.actions['copy'])
        edit.addAction(self.actions['paste'])
        edit.addSeparator()
        edit.addAction(self.actions['type_ipa'])
        edit_insert = edit.addMenu("&Insert brackets")
        edit_insert.addAction(self.actions['bracket_slash'])
        edit_insert.addAction(self.actions['bracket_sq_open'])
        edit_insert.addAction(self.actions['bracket_sq_close'])
        edit_insert.addAction(self.actions['bracket_angle_open'])
        edit_insert.addAction(self.actions['bracket_angle_close'])

        view = main.addMenu("&View")
        view.addAction(self.actions['use_tabs'])
        view.addAction(self.actions['show_toolbar'])
        view.addSeparator()
        view.addAction(self.actions['show_pul_cons'])
        view.addAction(self.actions['show_npul_cons'])
        view.addAction(self.actions['show_vowels'])
        view.addAction(self.actions['show_others'])
        view.addAction(self.actions['show_suprasegs'])
        view.addAction(self.actions['show_diacs'])
        view.addAction(self.actions['show_tones'])

        help = main.addMenu("&Help")
        help.addAction(self.actions['display_chr_map'])
        help.addSeparator()
        help.addAction(self.actions['display_about'])

    def initActions(self):
        self.actions = {} #Empty dict

        self.actions['exit'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "system-log-out.png")), "&Exit", self)
        self.actions['exit'].setShortcut("Ctrl+Q")
        self.actions['exit'].setStatusTip("Exit %s" % __title__)
        self.actions['exit'].setToolTip("Exit %s (Ctrl+Q)" % __title__)
        self.actions['exit'].triggered.connect(self.actionExit)

        self.actions['new'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "document-new.png")), "&New", self)
        self.actions['new'].setShortcut("Ctrl+N")
        self.actions['new'].setStatusTip("Start a new text")
        self.actions['new'].setToolTip("Start a new text (Ctrl+N)")
        self.actions['new'].triggered.connect(self.actionNew)

        self.actions['open'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "document-open.png")), "&Open", self)
        self.actions['open'].setShortcut("Ctrl+O")
        self.actions['open'].setStatusTip("Open text document")
        self.actions['open'].setToolTip("Open text document (Ctrl+O)")
        self.actions['open'].triggered.connect(self.actionOpen)

        self.actions['save'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "document-save.png")), "&Save", self)
        self.actions['save'].setShortcut("Ctrl+S")
        self.actions['save'].setStatusTip("Save current text")
        self.actions['save'].setToolTip("Save current text (Ctrl+S)")
        self.actions['save'].triggered.connect(self.actionSave)

        self.actions['save_as'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "document-save-as.png")), "S&ave as..", self)
        self.actions['save_as'].setShortcut("Ctrl+Alt+S")
        self.actions['save_as'].setStatusTip("Save current text to a different file")
        self.actions['save_as'].setToolTip("Save current text to a different file (Ctrl+Alt+S)")
        self.actions['save_as'].triggered.connect(self.actionSaveAs)

        self.actions['close'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "document-close.png")), "&Close", self)
        self.actions['close'].setShortcut("Ctrl+F4")
        self.actions['close'].setStatusTip("Close the current document")
        self.actions['close'].setToolTip("Close the current document (Ctrl+F4)")
        self.actions['close'].triggered.connect(self.actionClose)

        self.actions['undo'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "edit-undo.png")), "&Undo", self)
        self.actions['undo'].setShortcut("Ctrl+Z")
        self.actions['undo'].setStatusTip("Undo the last action")
        self.actions['undo'].setToolTip("Undo the last action (Ctrl+Z)")
        self.actions['undo'].setEnabled(False)
        self.actions['undo'].triggered.connect(self.actionUndo)

        self.actions['redo'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "edit-redo.png")), "Re&do", self)
        self.actions['redo'].setShortcut("Shift+Ctrl+Z")
        self.actions['redo'].setStatusTip("Redo the last action")
        self.actions['redo'].setToolTip("Redo the last action (Shift+Ctrl+Z)")
        self.actions['redo'].setEnabled(False)
        self.actions['redo'].triggered.connect(self.actionRedo)

        self.actions['clear'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "edit-clear.png")), "Clea&r", self)
        self.actions['clear'].setShortcut("Ctrl+R")
        self.actions['clear'].setStatusTip("Clear the current text")
        self.actions['clear'].setToolTip("Clear the current text (Ctrl+R)")
        self.actions['clear'].triggered.connect(self.actionClear)

        self.actions['cut'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "edit-cut.png")), "Cu&t", self)
        self.actions['cut'].setShortcut("Ctrl+X")
        self.actions['cut'].setStatusTip("Cut the current text")
        self.actions['cut'].setToolTip("Cut the current text (Ctrl+X)")
        self.actions['cut'].triggered.connect(self.actionCut)

        self.actions['copy'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "edit-copy.png")), "&Copy", self)
        self.actions['copy'].setShortcut("Ctrl+C")
        self.actions['copy'].setStatusTip("Copy the current text to clipboard")
        self.actions['copy'].setToolTip("Copy the current text to clipboard (Ctrl+C)")
        self.actions['copy'].triggered.connect(self.actionCopy)

        self.actions['paste'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "actions", "edit-paste.png")), "&Paste", self)
        self.actions['paste'].setShortcut("Ctrl+V")
        self.actions['paste'].setStatusTip("Past text from clipboard")
        self.actions['paste'].setToolTip("Paste text from clipboard (Ctrl+V)")
        self.actions['paste'].triggered.connect(self.actionPaste)

        self.actions['type_ipa'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "application-icon.png")), "T&ype in IPA", self, checkable=True, checked=self.settings.type_ipa)
        self.actions['type_ipa'].setShortcut("Ctrl+L")
        self.actions['type_ipa'].setStatusTip("Whether to type in IPA or normal text mode")
        self.actions['type_ipa'].setToolTip("Whether to type in IPA or normal text mode (Ctrl+L)")
        self.actions['type_ipa'].triggered.connect(self.actionTypeIPA)

        self.actions['bracket_slash'] = Qt.QAction("/", self)
        self.actions['bracket_slash'].setStatusTip("Insert forward slash bracket")
        self.actions['bracket_slash'].setToolTip("Insert forward slash bracket")
        self.actions['bracket_slash'].triggered.connect(lambda: self.insertText("/"))

        self.actions['bracket_sq_open'] = Qt.QAction("[", self)
        self.actions['bracket_sq_open'].setStatusTip("Insert opening square bracket")
        self.actions['bracket_sq_open'].setToolTip("Insert opening square bracket")
        self.actions['bracket_sq_open'].triggered.connect(lambda: self.insertText("["))

        self.actions['bracket_sq_close'] = Qt.QAction("]", self)
        self.actions['bracket_sq_close'].setStatusTip("Insert closing square bracket")
        self.actions['bracket_sq_close'].setToolTip("Insert closing square bracket")
        self.actions['bracket_sq_close'].triggered.connect(lambda: self.insertText("]"))

        self.actions['bracket_angle_open'] = Qt.QAction("〈", self)
        self.actions['bracket_angle_open'].setStatusTip("Insert opening angle bracket")
        self.actions['bracket_angle_open'].setToolTip("Insert opening angle bracket")
        self.actions['bracket_angle_open'].triggered.connect(lambda: self.insertText("〈"))

        self.actions['bracket_angle_close'] = Qt.QAction("〉", self)
        self.actions['bracket_angle_close'].setStatusTip("Insert closing angle bracket")
        self.actions['bracket_angle_close'].setToolTip("Insert closing angle bracket")
        self.actions['bracket_angle_close'].triggered.connect(lambda: self.insertText("〉"))

        self.actions['use_tabs'] = Qt.QAction("Use &Tabs", self, checkable=True)
        self.actions['use_tabs'].setShortcut("Ctrl+T")
        self.actions['use_tabs'].setStatusTip("Switch between tab and single chart view")
        self.actions['use_tabs'].setToolTip("Switch between tab and single chart view (Ctrl+T)")
        self.actions['use_tabs'].triggered.connect(self.actionX)

        self.actions['show_toolbar'] = Qt.QAction("Show &Toolbar", self, checkable=True, checked=self.settings.show_toolbar)
        self.actions['show_toolbar'].setStatusTip("Show/hide the main window toolbar")
        self.actions['show_toolbar'].setToolTip("Show/hide the main window toolbar")
        self.actions['show_toolbar'].triggered.connect(self.actionShowToolbar)

        self.actions['show_pul_cons'] = Qt.QAction("Show &Pulmonic Consonants", self, checkable=True)
        self.actions['show_pul_cons'].setStatusTip("Whether to show the pulmonic consonants or not")
        self.actions['show_pul_cons'].setToolTip("Whether to show the pulmonic consonants or not")
        self.actions['show_pul_cons'].triggered.connect(self.actionX)

        self.actions['show_npul_cons'] = Qt.QAction("Show &Non-pulmonic Consonants", self, checkable=True)
        self.actions['show_npul_cons'].setStatusTip("Whether to show the non-pulmonic consonants or not")
        self.actions['show_npul_cons'].setToolTip("Whether to show the non-pulmonic consonants or not")
        self.actions['show_npul_cons'].triggered.connect(self.actionX)

        self.actions['show_vowels'] = Qt.QAction("Show &Vowels", self, checkable=True)
        self.actions['show_vowels'].setStatusTip("Whether to show the vowels or not")
        self.actions['show_vowels'].setToolTip("Whether to show the vowels or not")
        self.actions['show_vowels'].triggered.connect(self.actionX)

        self.actions['show_others'] = Qt.QAction("Show &Other Symbols", self, checkable=True)
        self.actions['show_others'].setStatusTip("Whether to show the other symbols or not")
        self.actions['show_others'].setToolTip("Whether to show the other symbols or not")
        self.actions['show_others'].triggered.connect(self.actionX)

        self.actions['show_suprasegs'] = Qt.QAction("Show &Suprasegmentals", self, checkable=True)
        self.actions['show_suprasegs'].setStatusTip("Whether to show the suprasegmental consonants or not")
        self.actions['show_suprasegs'].setToolTip("Whether to show the suprasegmental consonants or not")
        self.actions['show_suprasegs'].triggered.connect(self.actionX)

        self.actions['show_diacs'] = Qt.QAction("Show &Diacritics", self, checkable=True)
        self.actions['show_diacs'].setStatusTip("Whether to show the diacritics or not")
        self.actions['show_diacs'].setToolTip("Whether to show the diactirics or not")
        self.actions['show_diacs'].triggered.connect(self.actionX)

        self.actions['show_tones'] = Qt.QAction("Show Tones and &Word Accents", self, checkable=True, checked=self.settings.show_tones)
        self.actions['show_tones'].setStatusTip("Whether to show the tones and word accents or not")
        self.actions['show_tones'].setToolTip("Whether to show the tones and word accents or not")
        self.actions['show_tones'].triggered.connect(self.actionX)

        self.actions['display_chr_map'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "apps", "accessories-character-map.png")), "IPA Character &Map", self)
        self.actions['display_chr_map'].setShortcut("Ctrl+M")
        self.actions['display_chr_map'].setStatusTip("Show a list of all IPA Characters with their names and shortcuts")
        self.actions['display_chr_map'].setToolTip("Show a list of all IPA Characters with their names and shortcuts (Ctrl+M)")
        self.actions['display_chr_map'].triggered.connect(self.actionDisplayChrMap)

        self.actions['display_about'] = Qt.QAction(Qt.QIcon(os.path.join(__path__, "resources", "icons", "status", "dialog-information.png")), "&About %s" % __title__, self)
        self.actions['display_about'].setStatusTip("Show information about %s" % __title__)
        self.actions['display_about'].setToolTip("Show information about %s" % __title__)
        self.actions['display_about'].triggered.connect(self.actionDisplayAbout)


    def initUI(self):
        #Set up main window layout
        self.resize(self.settings.mw_width, self.settings.mw_height)
        self.setWindowIcon(Qt.QIcon(os.path.join(__path__, "resources", "icons", "application-icon.png")))

        #Set up central layout hbox
        self.setCentralWidget(Qt.QWidget(self))
        vbox = Qt.QVBoxLayout(self)
        self.centralWidget().setLayout(vbox)
        self.topWidget = WriterWidget(self, transliterate=self.settings.type_ipa)
        self.topWidget.setEnabled(False)
        self.bottomWidget = Qt.QWidget(self)
        vbox.addWidget(self.topWidget)
        vbox.addWidget(self.bottomWidget)

        #Set up status bar
        self.statusBar() #Use self.statusBar().showMessage(blah) to set message

        #Set up menu bar
        self.menuBar()
        self.createMenu()

        #Set up tool bar
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.actions['new'])
        self.fileToolBar.addAction(self.actions['open'])
        self.fileToolBar.addAction(self.actions['save'])
        self.fileToolBar.setVisible(self.settings.show_toolbar)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.actions['undo'])
        self.editToolBar.addAction(self.actions['redo'])
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.actions['clear'])
        self.editToolBar.addAction(self.actions['copy'])
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.actions['type_ipa'])
        self.editToolBar.setVisible(self.settings.show_toolbar)

        self.bracketsToolBar = self.addToolBar("Brackets")
        self.bracketsToolBar.addAction(self.actions['bracket_sq_open'])
        self.bracketsToolBar.addAction(self.actions['bracket_sq_close'])
        self.bracketsToolBar.addAction(self.actions['bracket_slash'])
        self.bracketsToolBar.setVisible(self.settings.show_toolbar)

        #btn = IPAChartButton("Test Button", self, "Test Tooltip")
        #btn.resize(btn.sizeHint())
        #self.topWidget.layout().addWidget(btn)
        #self.topWidget.layout().addWidget(Qt.QPushButton("Hello World", self))

        #Make Undo and Redo buttons grey out in accordance with the topWidget Undo stack
        self.topWidget.textEdit.undoAvailable.connect(self.actions['undo'].setEnabled)
        self.topWidget.textEdit.redoAvailable.connect(self.actions['redo'].setEnabled)

        #Update window title
        self.updateWindowTitle()

        #Show window
        self.show()

    def initSettings(self):
        self.settings = Settings()
        try:
            self.settings.loadFromFile(os.path.join(__path__, "resources", "settings.json")) #Need to eventually adjust the path on OS basis to store user settings
        except Exception:
            pass #Settings file doesn't exist or is corrupt, just stick with defaults

    def initShortcuts(self):
        #Initialise shortcuts for all the IPA characters
        self.shortcuts = dict()
        for shortcut, props in shared.IPAshortcuts.items():
            if len(shortcut) > 1 and "+" in shortcut:
                self.shortcuts[shortcut] = Qt.QShortcut(Qt.QKeySequence(shortcut), self)
                fun = lambda x=props['char']: self.insertText(x) #If we connect to this it will pass props['name'] as a custom parameter
                self.connect(self.shortcuts[shortcut], Qt.SIGNAL('activated()'), fun)


    def insertText(self, char):
        self.topWidget.insertText(char)

    def resizeEvent(self, event):
        self.settings.mw_height = event.size().height()
        self.settings.mw_width = event.size().width()

    def storeSettings(self):
        try:
            self.settings.saveToFile(os.path.join(__path__, "resources", "settings.json"))
        except IOError as err:
            ErrorMessage(
                self,
                "Error storing application settings",
                "Could not store the application settings to file `settings.json'.",
                err,
                Qt.QMessageBox.Warning
            )

    def updateWindowTitle(self):
        if self.topWidget.isEnabled():
            doc = self.topWidget.getDocument()
            if isinstance(doc, Document):
                filename = doc.getFilename()
                if filename:
                    title = "%s - %s" % (os.path.basename(filename), __title__)
                    if doc.isModified():
                        title = "*%s" % title
                else:
                    title = "*Untitled document - %s" % __title__
            else:
                title = "*Untitled document - %s" % __title__
        else:
            title = __title__
        self.setWindowTitle(title)


class Settings:
    def __init__(self):
        self.mw_height = 500
        self.mw_width = 800
        self.use_tabs = True
        self.show_toolbar = True
        self.show_pul_cons = True
        self.show_npul_cons = True
        self.show_vowels = True
        self.show_others = True
        self.show_suprasegs = True
        self.show_diacs = True
        self.show_tones = True
        self.type_ipa = True

    def loadFromFile(self, path):
        with open(path, "r", encoding="utf-8") as fh:
            attrs = json.load(fh)
        for aname, avalue in attrs.items():
            setattr(self, aname, avalue)

    def saveToFile(self, path):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.__dict__, fh, indent=2)


class WriterWidget(Qt.QWidget):
    def __init__(self, parent, transliterate=True):
        super().__init__(parent)
        self.setLayout(Qt.QVBoxLayout(parent))

        self.transliterate = transliterate# Whether to try and transliterate to IPA

        self.textEdit = Qt.QTextEdit(parent)
        self.layout().addWidget(self.textEdit)

        self.setFocusProxy(self.textEdit) #Let the textEdit handle all focus requests
        self.textEdit.installEventFilter(self)

        self.setStyleSheet("QTextEdit { font-family:Times; font-size:14pt }")

    def eventFilter(self, obj, event):
        #We want to filter all these keys:
        filteredKeys  = "1234567890-=!\"£$%^&*()_+"
        filteredKeys += "{}[]:;@'~#|\\<>,.?/"
        filteredKeys += "abcdefghijklmnopqrstuvwxzy"
        filteredKeys += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if event.type() == Qt.QEvent.KeyPress:
            if event.text() and event.text() in filteredKeys:
                if event.modifiers() == Qt.Qt.NoModifier or event.modifiers() == Qt.Qt.ShiftModifier:
                    self.insertChar(event.text())
                    return True #Makes sure Qt will consider the event "handled" and not insert text itself
        #If not filtering that key return 0 so event handling will go the normal course
        return 0

    def clear(self):
        return self.textEdit.clear()

    def copy(self):
        #Needs to make sure that iff no text is selected ALL text is copied
        return self.textEdit.copy()

    def cut(self):
        #Needs to make sure that iff no text is selected, ALL text is cut
        return self.textEdit.cut()

    def paste(self):
        return self.textEdit.paste()

    def undo(self):
        return self.textEdit.undo()

    def redo(self):
        return self.textEdit.redo()

    def setDocument(self, document):
        self.textEdit.setDocument(document)

    def setTransliterate(self, transliterate=True):
        self.transliterate = bool(transliterate)

    def getDocument(self):
        return self.textEdit.document()

    def getTransliterate():
        return self.transliterate

    def insertChar(self, char):
        if self.transliterate:
            if char in shared.IPAshortcuts:
                char = shared.IPAshortcuts[char]['char']
        self.textEdit.textCursor().insertText(char)

    def insertText(self, text):
        self.textEdit.textCursor().insertText(text)