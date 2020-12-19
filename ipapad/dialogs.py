# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget, QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QScrollArea, QDialogButtonBox, QTableView, QLineEdit
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Qt, QRegularExpression, QSortFilterProxyModel
import os
import sys
import traceback
from . import shared

class UnsavedChangesDialog(QMessageBox):
    """
    Dialog to request user input when trying to close unsaved document

    The dialog displays a message to the user telling them that the current
    document has unsaved changes. It asks the user if they want to save those
    changes or discard them. The user can also cancel the action, which should
    be treated as a decision by the user not to go ahead with any potentially
    destructive changes (e.g. simply ignore they clicked "New document" or
    "Exit", etc.).

    The dialog's .run() function returns one of three values: .save, .discard or
    .cancel. These can be combined using binary operators, e.g.
        if(dialog.run() is UnsavedChangesDialog.discard | UnsavedChangedDialog.cancel):
            pass
    """
    #Possible return states
    save    = 0b001
    discard = 0b010
    cancel  = 0b100

    result  = None

    def __init__(self, parent=None):
        """Initialise but don't execute the UnsavedChangesDialog"""
        if(parent is None):
            super().__init__()
        else:
            super().__init__(parent)
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(shared.__title__)
        self.setText("The document contains unsaved changes.\n"
                     "Do you want to save it before closing it?")
        self.setInformativeText("If you do not save the document before closing it "
                                "any changes that have been made since it was last saved "
                                "will be irreversibly lost.")
        #self.setStandardButtons(Qt.QMessageBox.Save | Qt.QMessageBox.Ignore | Qt.QMessageBox.Cancel)
        self.save_button = self.addButton("Save", QMessageBox.YesRole)
        self.discard_button = self.addButton("Don't save", QMessageBox.DestructiveRole)
        self.cancel_button = self.addButton("Cancel", QMessageBox.RejectRole)

    def run(self):
        """Execute the UnsavedChangesDialog and return the user's choice"""
        self.exec()
        if(self.clickedButton() is self.save_button):
            return self.save
        if(self.clickedButton() is self.discard_button):
            return self.discard
        #else:
        return self.cancel



class AboutDialog(QDialog):
    """Simple dialog displaying icon, copyright notice, link to website and license"""
    def __init__(self, parent=None, base_path="./"):
        super().__init__(parent)
        self.setWindowIcon(QIcon(os.path.join(base_path, "resources", "icons", "status", "dialog-information.png")))
        self.setStyleSheet("QLabel { padding:15px; background:white }")
        self.setWindowTitle("About %s" % shared.__title__)
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.setLayout(QVBoxLayout())

        self.tab_widget = QTabWidget()
        self.layout().addWidget(self.tab_widget)

        self.about_tab = QLabel()
        self.about_tab.setText((
            "<html>"
            " <body>"
            "  <center>"
            "   <p><img src=\"application-icon.png\" width=\"100\" height=\"100\" /></p>"
            "   <p><b><font size=\"20\">%s 1.0</font></b></p>"
            "   <p><big>A simple program to help you write transcriptions in the IPA.</big></p>"
            "   <p>(C) 2020 Florian Breit</p>"
            "   <p><a href=\"http://florian.me.uk\">http://florian.me.uk</a></p>"
            "  </center>"
            " </body>"
            "</html>"
        ) % (shared.__title__) )
        self.about_tab.setText(
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
                ICON_PATH=os.path.join(base_path, "resources", "icons", "application-icon.png"),
                PROG_NAME=shared.__title__,
                PROG_VERSION=shared.__version__,
                COPYRIGHT=shared.__copyright__
            )
        )
        self.tab_widget.addTab(self.about_tab, "About")

        #Not required at present
        #self.creditsTab = Qt.QLabel()
        #self.tabWidget.addTab(self.creditsTab, "Credits")

        self.license_tab = QScrollArea()
        self.license_label = QLabel()
        self.license_tab.setWidget(self.license_label)
        self.license_tab.setWidgetResizable(True)
        self.license_tab.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.license_tab.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.license_label.setMinimumWidth(510)
        self.license_label.setWordWrap(True)
        with open(os.path.join(base_path, "resources", "license.html"), encoding="utf8") as file:
            self.license_label.setText(file.read())
        self.tab_widget.addTab(self.license_tab, "License")

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        self.layout().addWidget(self.button_box)

        self.show()


class CharacterMapDialog(QDialog):
    """Dialog displaying a searchable list of all the available IPA characters together with their description and shortcut"""
    def __init__(self, parent=None, base_path="./"):
        super().__init__(parent)
        self.setWindowIcon(QIcon(os.path.join(base_path, "resources", "icons", "apps", "accessories-character-map.png")))
        self.setWindowTitle("IPA Character Map")
        self.resize(500, 700)
        self.setLayout(QVBoxLayout())

        self.table_view_widget = QTableView(self)
        self.view_model = QStandardItemModel(0, 3, self.table_view_widget)
        self.proxy_model = QSortFilterProxyModel(self.table_view_widget)
        self.proxy_model.setSourceModel(self.view_model)
        self.proxy_model.setFilterKeyColumn(1)
        self.table_view_widget.setModel(self.proxy_model)
        self.table_view_widget.verticalHeader().setVisible(False) #Hide vertical header
        self.table_view_widget.horizontalHeader().setStretchLastSection(True) #Make widget stretch horizontally
        self.table_view_widget.setSortingEnabled(True)
        self.layout().addWidget(self.table_view_widget)

        self.buildModel()
        self.table_view_widget.resizeColumnsToContents()
        #self.tableViewWidget.sortByColumn(2, Qt.QTableView.AscendingOrder)

        self.filter_label = QLabel("Search:")
        self.filter_label.setToolTip("Search for a character by it's description (regular expressions are supported)")
        self.filter_edit = QLineEdit("")
        self.filter_edit.textChanged.connect(self.action_filter)
        self.filter_container = QWidget(self)
        self.filter_container.setLayout(QHBoxLayout())
        self.filter_container.layout().addWidget(self.filter_label)
        self.filter_container.layout().addWidget(self.filter_edit)
        self.layout().addWidget(self.filter_container)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        self.layout().addWidget(self.button_box)

        self.show()

        self.filter_edit.setFocus()

    def action_filter(self, text):
        search = QRegularExpression(text, QRegularExpression.CaseInsensitiveOption)
        #search = QRegExp(text, Qt.CaseInsensitive, QRegExp.RegExp) # No longer supported in PySide6?
        self.proxy_model.setFilterRegularExpression(search)

    def buildModel(self):
        self.view_model.setHorizontalHeaderLabels(("Symbol", "Description", "Shortcut"))
        for symbol, description in shared.ipa_chars.items():
            item = (
                QStandardItem(" " + symbol),
                QStandardItem(description["name"]),
                QStandardItem(description["shortcut"])
            )
            self.view_model.appendRow(item)



class ErrorMessageDialog(QMessageBox):
    """Dialog to display an error message to the user"""
    def __init__(self, parent=None, short=None, long=None, detail=None, type=QMessageBox.Critical):
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
        self.setStandardButtons(QMessageBox.Ok)
        self.setIcon(type)
        if(detail is not None):
            if(isinstance(detail, Exception)):
                dname = sys.exc_info()[0].__name__
                dmsg = sys.exc_info()[1]
                dtb = traceback.format_exc()
                detail = "%s %s\n\n%s" % (dname, dmsg, dtb)
                self.setDetailedText(detail)
            else:
                self.setDetailedText(detail)
        self.exec()
