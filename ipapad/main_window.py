# -*- coding: utf-8 -*-
"""Main Window for IPAPad"""

import sys
import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon, QAction, QShortcut, QKeySequence
from PySide6.QtCore import SIGNAL
from . import shared
from .writer_widget import WriterWidget
from .dialogs import UnsavedChangesDialog, AboutDialog, CharacterMapDialog, ErrorMessageDialog
from .document_handler import Document
from .settings import SettingsManager


# Dependencies: Document

class MainWindow(QMainWindow):
    """IPAPad main window and main program logic"""

    def __init__(self, parent=None, base_path="./"):
        super().__init__(parent)
        self.base_path = base_path
        self.init_settings()
        self.init_actions()
        self.init_shortcuts()
        self.init_ui()
        self.toggle_editing_actions(False)
        # Load file or start a new file and enable writer widget
        self.action_new()

    def action_clear(self):
        """Clear the contents of the currently active IPAtype Document."""
        self.top_widget.clear()

    def action_close(self):
        """
        Close the current document

        Check if the current Document contains any unsaved changes. If
        so ask user if they really want to close it and lose all unsaved
        changes, otherwise close the document and grey out the document widget.
        """
        doc = self.top_widget.get_document()
        if(doc.isModified()):
            dialog = UnsavedChangesDialog(parent=self)
            result = dialog.run()
            if(result is UnsavedChangesDialog.cancel):
                return False
            elif(result is UnsavedChangesDialog.save):
                if(self.action_save() is False):
                    return False
            #else (==user chose to discard): proceed with below code to close document
        #Set Document to empty document and disable document widget
        self.top_widget.set_document(Document())
        self.top_widget.setEnabled(False)
        #Disable all the buttons that operate on individual documents
        self.toggle_editing_actions(False)
        self.update_window_title()
        return True

    def action_copy(self):
        """Copy text selection to clipboard"""
        self.top_widget.copy()

    def action_cut(self):
        """Cut text selection to clipboard"""
        self.top_widget.cut()

    def action_display_about(self):
        """Display about dialog with information about this program"""
        AboutDialog(self, base_path=self.base_path)

    def action_display_chr_map(self):
        """Display dialog with list of available IPA characters and shortcuts"""
        CharacterMapDialog(self, self.base_path)

    def action_exit(self):
        """Quit the program"""
        # Ensure that any open documents are saved first
        if self.action_close():
            self.close()
            return True
        else:
            return False

    def action_new(self):
        """Start a new IPAtype document"""
        #Check whether the current document contains unsaved changes, if so
        #close it first, checking whether the user wants to save it or not
        doc = self.top_widget.get_document()
        if(doc.isModified()):
            if(self.action_close() is False):
                return False

        #Create new document
        doc = Document()
        self.top_widget.set_document(doc)
        self.top_widget.setEnabled(True)
        self.update_window_title()
        self.statusBar().showMessage("Initialised new document")

        #Enable/disable all the appropriate buttons
        self.toggle_editing_actions(True)
        self.check_undo_redo_available()

    def action_open(self):
        """Open a text file as a new IPAtype Document"""
        #Check whether the current document contains unsaved changes, if so
        #close it first, checking whether the user wants to save it or not
        doc = self.top_widget.get_document()
        if(doc.isModified()):
            if(self.action_close() is False):
                return False

        #TODO: Would be useful to implement an extra field to select encoding
        filename = QFileDialog.getOpenFileName(self, "Open Document", None, "Text Documents (*.txt);;All Files (*)")
        if filename[0]:
            try:
                doc = Document.from_file(filename[0], self)
            except (UnicodeDecodeError, IOError) as err:
                if isinstance(err, UnicodeDecodeError):
                    emsg = "The file's encoding is not compatible with Unicode (UTF-8)."
                if isinstance(err, IOError):
                    emsg = "The file could not be opened."
                ErrorMessageDialog(
                    self,
                    "Error opening file",
                    emsg,
                    err,
                    QMessageBox.Warning
                )
                return False
            doc.setModified(False)
            self.top_widget.set_document(doc)
            self.top_widget.setEnabled(True)
            self.update_window_title()
            self.statusBar().showMessage(f"Successfully loaded { filename[0] }")
            #Enable/disable all the appropriate buttons
            self.toggle_editing_actions(True)
            self.check_undo_redo_available()
            return True
        return False

    def action_paste(self):
        """Paste from clipboard"""
        #TODO: Implement continuous check whether (a) there is something in the
        #clipboard that can be pasted and (b) there is a document to paste it in
        #(i.e. the topWidget is not disabled).
        self.top_widget.paste()

    def action_redo(self):
        """Redo the last modification to the current document"""
        self.top_widget.redo()

    def action_save(self):
        """Save the current document to file."""
        filename = self.top_widget.get_document().get_filename()
        if filename:
            doc = self.top_widget.get_document()
            try:
                status = doc.save_to_file(filename)
            except (Exception) as err:
                if isinstance(err, PermissionError):
                    emsg = "You do not have the permission to write to this file."
                else:
                    emsg = "The file could not be saved."
                ErrorMessageDialog(
                    self,
                    "Error saving file",
                    emsg,
                    err,
                    QMessageBox.Warning
                )
                self.statusBar().showMessage("Error: could not save to " + filename)
                self.update_window_title()
                return False
            if status:
                self.statusBar().showMessage("File saved as " + filename)
                self.update_window_title()
                return True
            else:
                return False
        else:
            return self.action_save_as()
        return False

    def action_save_as(self):
        """Save the current document to a different file"""
        basepath = self.top_widget.get_document().get_filename()
        if basepath is not None:
            basepath = os.path.dirname(basepath)

        #TODO: Would be useful to implement an extra field to select encoding
        filename = QFileDialog.getSaveFileName(self, "Save Document as ...", basepath, "Text Documents (*.txt);;All Files (*)")
        if filename[0]:
            doc = self.top_widget.get_document()
            try:
                status = doc.save_to_file(filename[0])
            except (Exception) as err:
                if isinstance(err, PermissionError):
                    emsg = "You do not have the permission to write to this file."
                else:
                    emsg = "The file could not be saved."
                ErrorMessageDialog(
                    self,
                    "Error saving file",
                    emsg,
                    err,
                    QMessageBox.Warning
                )
                self.statusBar().showMessage(f"Error: could not save to { filename[0] }")
                self.update_window_title()
                return False
            if status:
                self.statusBar().showMessage(f"File saved as { filename[0] }")
                self.update_window_title()
                return True
        return False

    def apply_settings(settings, self):
        """Reload and apply settings from configuration"""
        raise NotImplementedError

    def action_show_toolbar(self, value):
        """Display a toolbar at the top of the main window"""
        self.settings.show_toolbar = value
        self.file_toolbar.setVisible(value)
        self.edit_toolbar.setVisible(value)
        self.brackets_toolbar.setVisible(value)
        if value:
            self.statusBar().showMessage("Toolbars are now visible")
        else:
            self.statusBar().showMessage("Toolbars are now hidden")

    def action_type_ipa(self, checked):
        """Switch between transliterating and not transliterating input into IPA"""
        if checked:
            self.settings.type_ipa = True
            self.top_widget.set_transliterate(True)
            self.statusBar().showMessage("Now typing in IPA mode")
        else:
            self.settings.type_ipa = False
            self.top_widget.set_transliterate(False)
            self.statusBar().showMessage("Now typing in normal text mode")

    def action_undo(self):
        """Undo the last modification of the current document"""
        self.top_widget.undo()

    def action_x(self):
        raise NotImplementedError

    def check_undo_redo_available(self):
        """Check if undo/redo actions are available and update enabled status of GUI actions"""
        document = self.top_widget.get_document()
        if document.availableUndoSteps():
            self.actions['undo'].setEnabled(True)
        else:
            self.actions['undo'].setEnabled(False)
        if document.availableRedoSteps():
            self.actions['redo'].setEnabled(True)
        else:
            self.actions['redo'].setEnabled(False)

    def closeEvent(self, event):
        """Overwrite closeEvent handler to redirect to self.action_exit()"""
        if self.action_exit():
            self.store_settings()
            event.accept()
        else:
            event.ignore()

    def create_menu(self):
        """Create the main menu for the main window."""
        main = self.menuBar()

        file = main.addMenu("&File")
        file.addAction(self.actions["new"])
        file.addAction(self.actions["open"])
        file.addAction(self.actions["save"])
        file.addAction(self.actions["save_as"])
        file.addAction(self.actions["close"])
        file.addSeparator()
        file.addAction(self.actions["exit"])

        edit = main.addMenu("&Edit")
        edit.addAction(self.actions["undo"])
        edit.addAction(self.actions["redo"])
        edit.addSeparator()
        edit.addAction(self.actions["clear"])
        edit.addAction(self.actions["cut"])
        edit.addAction(self.actions["copy"])
        edit.addAction(self.actions["paste"])
        edit.addSeparator()
        edit.addAction(self.actions["type_ipa"])
        edit_insert = edit.addMenu("&Insert brackets")
        edit_insert.addAction(self.actions["bracket_slash"])
        edit_insert.addAction(self.actions["bracket_sq_open"])
        edit_insert.addAction(self.actions["bracket_sq_close"])
        edit_insert.addAction(self.actions["bracket_angle_open"])
        edit_insert.addAction(self.actions["bracket_angle_close"])

        view = main.addMenu("&View")
        view.addAction(self.actions["use_tabs"])
        view.addAction(self.actions["show_toolbar"])
        view.addSeparator()
        view.addAction(self.actions["show_pul_cons"])
        view.addAction(self.actions["show_npul_cons"])
        view.addAction(self.actions["show_vowels"])
        view.addAction(self.actions["show_others"])
        view.addAction(self.actions["show_suprasegs"])
        view.addAction(self.actions["show_diacs"])
        view.addAction(self.actions["show_tones"])

        help = main.addMenu("&Help")
        help.addAction(self.actions["display_chr_map"])
        help.addSeparator()
        help.addAction(self.actions["display_about"])

    def init_actions(self):
        """Initialise a dict containing all the actions active in the main window."""
        self.actions = {}

        self.actions["exit"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "system-log-out.png")), "&Exit", self)
        self.actions["exit"].setShortcut("Ctrl+Q")
        self.actions["exit"].setStatusTip("Exit %s" % shared.__title__)
        self.actions["exit"].setToolTip("Exit %s (Ctrl+Q)" % shared.__title__)
        self.actions["exit"].triggered.connect(self.action_exit)

        self.actions["new"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "document-new.png")), "&New", self)
        self.actions["new"].setShortcut("Ctrl+N")
        self.actions["new"].setStatusTip("Start a new text")
        self.actions["new"].setToolTip("Start a new text (Ctrl+N)")
        self.actions["new"].triggered.connect(self.action_new)

        self.actions["open"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "document-open.png")), "&Open", self)
        self.actions["open"].setShortcut("Ctrl+O")
        self.actions["open"].setStatusTip("Open text document")
        self.actions["open"].setToolTip("Open text document (Ctrl+O)")
        self.actions["open"].triggered.connect(self.action_open)

        self.actions["save"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "document-save.png")), "&Save", self)
        self.actions["save"].setShortcut("Ctrl+S")
        self.actions["save"].setStatusTip("Save current text")
        self.actions["save"].setToolTip("Save current text (Ctrl+S)")
        self.actions["save"].setEnabled(False)
        self.actions["save"].triggered.connect(self.action_save)

        self.actions["save_as"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "document-save-as.png")), "S&ave as..", self)
        self.actions["save_as"].setShortcut("Ctrl+Alt+S")
        self.actions["save_as"].setStatusTip("Save current text to a different file")
        self.actions["save_as"].setToolTip("Save current text to a different file (Ctrl+Alt+S)")
        self.actions["save_as"].triggered.connect(self.action_save_as)

        self.actions["close"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "document-close.png")), "&Close", self)
        self.actions["close"].setShortcut("Ctrl+F4")
        self.actions["close"].setStatusTip("Close the current document")
        self.actions["close"].setToolTip("Close the current document (Ctrl+F4)")
        self.actions["close"].triggered.connect(self.action_close)

        self.actions["undo"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "edit-undo.png")), "&Undo", self)
        self.actions["undo"].setShortcut("Ctrl+Z")
        self.actions["undo"].setStatusTip("Undo the last action")
        self.actions["undo"].setToolTip("Undo the last action (Ctrl+Z)")
        self.actions["undo"].triggered.connect(self.action_undo)

        self.actions["redo"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "edit-redo.png")), "Re&do", self)
        self.actions["redo"].setShortcut("Shift+Ctrl+Z")
        self.actions["redo"].setStatusTip("Redo the last action")
        self.actions["redo"].setToolTip("Redo the last action (Shift+Ctrl+Z)")
        self.actions["redo"].triggered.connect(self.action_redo)

        self.actions["clear"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "edit-clear.png")), "Clea&r", self)
        self.actions["clear"].setShortcut("Ctrl+R")
        self.actions["clear"].setStatusTip("Clear the current text")
        self.actions["clear"].setToolTip("Clear the current text (Ctrl+R)")
        self.actions["clear"].triggered.connect(self.action_clear)

        self.actions["cut"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "edit-cut.png")), "Cu&t", self)
        self.actions["cut"].setShortcut("Ctrl+X")
        self.actions["cut"].setStatusTip("Cut the current text")
        self.actions["cut"].setToolTip("Cut the current text (Ctrl+X)")
        self.actions["cut"].triggered.connect(self.action_cut)

        self.actions["copy"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "edit-copy.png")), "&Copy", self)
        self.actions["copy"].setShortcut("Ctrl+C")
        self.actions["copy"].setStatusTip("Copy the current text to clipboard")
        self.actions["copy"].setToolTip("Copy the current text to clipboard (Ctrl+C)")
        self.actions["copy"].triggered.connect(self.action_copy)

        self.actions["paste"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "actions", "edit-paste.png")), "&Paste", self)
        self.actions["paste"].setShortcut("Ctrl+V")
        self.actions["paste"].setStatusTip("Past text from clipboard")
        self.actions["paste"].setToolTip("Paste text from clipboard (Ctrl+V)")
        self.actions["paste"].triggered.connect(self.action_paste)

        self.actions["type_ipa"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "application-icon.png")), "T&oggle IPA Mode", self, checkable=True, checked=self.settings.type_ipa)
        self.actions["type_ipa"].setShortcut("Ctrl+L")
        self.actions["type_ipa"].setStatusTip("Whether to type in IPA or normal text mode")
        self.actions["type_ipa"].setToolTip("Whether to type in IPA or normal text mode (Ctrl+L)")
        self.actions["type_ipa"].triggered.connect(self.action_type_ipa)

        self.actions["bracket_slash"] = QAction("/", self)
        self.actions["bracket_slash"].setStatusTip("Insert forward slash bracket")
        self.actions["bracket_slash"].setToolTip("Insert forward slash bracket")
        self.actions["bracket_slash"].triggered.connect(lambda: self.insert_text("/"))

        self.actions["bracket_sq_open"] = QAction("[", self)
        self.actions["bracket_sq_open"].setStatusTip("Insert opening square bracket")
        self.actions["bracket_sq_open"].setToolTip("Insert opening square bracket")
        self.actions["bracket_sq_open"].triggered.connect(lambda: self.insert_text("["))

        self.actions["bracket_sq_close"] = QAction("]", self)
        self.actions["bracket_sq_close"].setStatusTip("Insert closing square bracket")
        self.actions["bracket_sq_close"].setToolTip("Insert closing square bracket")
        self.actions["bracket_sq_close"].triggered.connect(lambda: self.insert_text("]"))

        self.actions["bracket_angle_open"] = QAction("〈", self)
        self.actions["bracket_angle_open"].setStatusTip("Insert opening angle bracket")
        self.actions["bracket_angle_open"].setToolTip("Insert opening angle bracket")
        self.actions["bracket_angle_open"].triggered.connect(lambda: self.insert_text("〈"))

        self.actions["bracket_angle_close"] = QAction("〉", self)
        self.actions["bracket_angle_close"].setStatusTip("Insert closing angle bracket")
        self.actions["bracket_angle_close"].setToolTip("Insert closing angle bracket")
        self.actions["bracket_angle_close"].triggered.connect(lambda: self.insert_text("〉"))

        self.actions["use_tabs"] = QAction("Use &Tabs", self, checkable=True)
        self.actions["use_tabs"].setShortcut("Ctrl+T")
        self.actions["use_tabs"].setStatusTip("Switch between tab and single chart view")
        self.actions["use_tabs"].setToolTip("Switch between tab and single chart view (Ctrl+T)")
        self.actions["use_tabs"].triggered.connect(self.action_x)

        self.actions["show_toolbar"] = QAction("Show &Toolbar", self, checkable=True, checked=self.settings.show_toolbar)
        self.actions["show_toolbar"].setStatusTip("Show/hide the main window toolbar")
        self.actions["show_toolbar"].setToolTip("Show/hide the main window toolbar")
        self.actions["show_toolbar"].triggered.connect(self.action_show_toolbar)

        self.actions["show_pul_cons"] = QAction("Show &Pulmonic Consonants", self, checkable=True)
        self.actions["show_pul_cons"].setStatusTip("Whether to show the pulmonic consonants or not")
        self.actions["show_pul_cons"].setToolTip("Whether to show the pulmonic consonants or not")
        self.actions["show_pul_cons"].triggered.connect(self.action_x)

        self.actions["show_npul_cons"] = QAction("Show &Non-pulmonic Consonants", self, checkable=True)
        self.actions["show_npul_cons"].setStatusTip("Whether to show the non-pulmonic consonants or not")
        self.actions["show_npul_cons"].setToolTip("Whether to show the non-pulmonic consonants or not")
        self.actions["show_npul_cons"].triggered.connect(self.action_x)

        self.actions["show_vowels"] = QAction("Show &Vowels", self, checkable=True)
        self.actions["show_vowels"].setStatusTip("Whether to show the vowels or not")
        self.actions["show_vowels"].setToolTip("Whether to show the vowels or not")
        self.actions["show_vowels"].triggered.connect(self.action_x)

        self.actions["show_others"] = QAction("Show &Other Symbols", self, checkable=True)
        self.actions["show_others"].setStatusTip("Whether to show the other symbols or not")
        self.actions["show_others"].setToolTip("Whether to show the other symbols or not")
        self.actions["show_others"].triggered.connect(self.action_x)

        self.actions["show_suprasegs"] = QAction("Show &Suprasegmentals", self, checkable=True)
        self.actions["show_suprasegs"].setStatusTip("Whether to show the suprasegmental consonants or not")
        self.actions["show_suprasegs"].setToolTip("Whether to show the suprasegmental consonants or not")
        self.actions["show_suprasegs"].triggered.connect(self.action_x)

        self.actions["show_diacs"] = QAction("Show &Diacritics", self, checkable=True)
        self.actions["show_diacs"].setStatusTip("Whether to show the diacritics or not")
        self.actions["show_diacs"].setToolTip("Whether to show the diactirics or not")
        self.actions["show_diacs"].triggered.connect(self.action_x)

        self.actions["show_tones"] = QAction("Show Tones and &Word Accents", self, checkable=True, checked=self.settings.show_tones)
        self.actions["show_tones"].setStatusTip("Whether to show the tones and word accents or not")
        self.actions["show_tones"].setToolTip("Whether to show the tones and word accents or not")
        self.actions["show_tones"].triggered.connect(self.action_x)

        self.actions["display_chr_map"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "apps", "accessories-character-map.png")), "IPA Character &Map", self)
        self.actions["display_chr_map"].setShortcut("Ctrl+M")
        self.actions["display_chr_map"].setStatusTip("Show a list of all IPA Characters with their names and shortcuts")
        self.actions["display_chr_map"].setToolTip("Show a list of all IPA Characters with their names and shortcuts (Ctrl+M)")
        self.actions["display_chr_map"].triggered.connect(self.action_display_chr_map)

        self.actions["display_about"] = QAction(QIcon(os.path.join(self.base_path, "resources", "icons", "status", "dialog-information.png")), "&About %s" % shared.__title__, self)
        self.actions["display_about"].setStatusTip("Show information about %s" % shared.__title__)
        self.actions["display_about"].setToolTip("Show information about %s" % shared.__title__)
        self.actions["display_about"].triggered.connect(self.action_display_about)

    def init_ui(self):
        """Initialise the layout and GUI elements of the main window"""
        # Main window layout
        self.resize(self.settings.mw_width, self.settings.mw_height)
        self.setWindowIcon(
            QIcon(os.path.join(self.base_path, "resources", "icons", "application-icon.png")))

        # Set up central layout hbox
        self.setCentralWidget(QWidget())
        vbox = QVBoxLayout()
        self.centralWidget().setLayout(vbox)
        self.top_widget = WriterWidget(transliterate=self.settings.type_ipa)
        self.top_widget.setEnabled(False)
        self.bottom_widget = QWidget()
        vbox.addWidget(self.top_widget)
        vbox.addWidget(self.bottom_widget)

        # Set up status bar
        self.statusBar()  # Use self.statusBar().showMessage("foo") to set message

        # Set up menu bar
        self.menuBar() # Initialise menu bar
        self.create_menu()

        # Set up toolbar
        self.file_toolbar = self.addToolBar("File")
        self.file_toolbar.addAction(self.actions["new"])
        self.file_toolbar.addAction(self.actions["open"])
        self.file_toolbar.addAction(self.actions["save"])
        self.file_toolbar.setVisible(self.settings.show_toolbar)

        self.edit_toolbar = self.addToolBar("Edit")
        self.edit_toolbar.addAction(self.actions["undo"])
        self.edit_toolbar.addAction(self.actions["redo"])
        self.edit_toolbar.addSeparator()
        self.edit_toolbar.addAction(self.actions["clear"])
        self.edit_toolbar.addAction(self.actions["copy"])
        self.edit_toolbar.addSeparator()
        self.edit_toolbar.addAction(self.actions["type_ipa"])
        self.edit_toolbar.setVisible(self.settings.show_toolbar)

        self.brackets_toolbar = self.addToolBar("Brackets")
        self.brackets_toolbar.addAction(self.actions["bracket_sq_open"])
        self.brackets_toolbar.addAction(self.actions["bracket_sq_close"])
        self.brackets_toolbar.addAction(self.actions["bracket_slash"])
        self.brackets_toolbar.setVisible(self.settings.show_toolbar)

        # Link Undo and Redo buttons to top_widget's Undo-stack
        self.top_widget.text_edit.undoAvailable.connect(
            self.actions["undo"].setEnabled)
        self.top_widget.text_edit.redoAvailable.connect(
            self.actions["redo"].setEnabled)

        # Update window title
        self.update_window_title()

        # Show Window
        self.show()


    def init_settings(self):
        """Load program settings from file"""
        self.settings = SettingsManager()
        try:
            # TODO: adjust the path on OS basis to store user settings
            self.settings.loadFromFile(os.path.join(
                SettingsManager.get_user_path(shared.__title__), "settings.json"))
        except Exception:
            pass  # Settings file doesn't exist or is corrupt, just use defaults

    def init_shortcuts(self):
        """Initialise shortcuts for the IPA characters in shared.IPAshortcuts."""
        self.shortcuts = {}
        for shortcut, props in shared.ipa_shortcuts.items():
            if len(shortcut) > 1 and "+" in shortcut:
                self.shortcuts[shortcut] = QShortcut(QKeySequence(shortcut), self)
                fun = lambda x=props['char']: self.insert_text(x) #If we connect to this it will pass props['name'] as a custom parameter
                self.connect(self.shortcuts[shortcut], SIGNAL('activated()'), fun)

    def insert_text(self, char):
        """Insert text at current cursor position in document."""
        self.top_widget.insert_text(char)

    def resizeEvent(self, event):
        """Resize the main window and store new width/height"""
        self.settings.mw_height = event.size().height()
        self.settings.mw_width = event.size().width()

    def store_settings(self):
        """Save the current settings to file"""
        try:
            self.settings.save_to_file(os.path.join(SettingsManager.get_user_path(shared.__title__), "settings.json"))
        except IOError as err:
            ErrorMessage(
                self,
                "Error storing application settings",
                "Could not store the application settings to file `settings.json'.",
                err,
                Qt.QMessageBox.Warning
            )

    def toggle_editing_actions(self, enabled):
        """Enable or disable all the actions that apply only when a document is open for editing"""
        self.actions["undo"].setEnabled(enabled)
        self.actions["redo"].setEnabled(enabled)
        self.actions["clear"].setEnabled(enabled)
        self.actions["cut"].setEnabled(enabled)
        self.actions["copy"].setEnabled(enabled)
        self.actions["close"].setEnabled(enabled)
        self.actions["paste"].setEnabled(enabled)
        self.actions["save"].setEnabled(enabled)
        self.actions["save_as"].setEnabled(enabled)
        self.actions["bracket_slash"].setEnabled(enabled)
        self.actions["bracket_sq_open"].setEnabled(enabled)
        self.actions["bracket_sq_close"].setEnabled(enabled)
        self.actions["bracket_angle_open"].setEnabled(enabled)
        self.actions["bracket_angle_close"].setEnabled(enabled)

    def update_window_title(self):
        """
        Automatically generate window title of the main window

        This function will automatically generate and update the main window
        title to reflect the current status. If no document is opened it will
        simply show the program name, e.g. "IPAtype". If a document is open but
        has not been saved it will show "Untitled document - IPAtype". If a
        document is open and does have an associated filename, it will show
        "filename.ext - IPAtype". If the currently open document has unsaved
        changes, it is additionally prefixed with an asterisk, e.g.
        "*filename.ext - IPAtype".
        """
        # TODO: Implement some mechanism that monitors whether document has been
        # modified to update title adding asterisk dynamically after opening a
        # file
        if(self.top_widget.isEnabled()):
            doc = self.top_widget.get_document()
            if(isinstance(doc, Document)):
                filename = doc.get_filename()
                if filename:
                    title = "%s - %s" % (os.path.basename(filename), shared.__title__)
                    if(doc.isModified()):
                        title = "*%s" % title
                else:
                    title = "*Untitled document - %s" % shared.__title__
            else:
                title = "*Untitled document - %s" % shared.__title__
        else:
            title = shared.__title__
        self.setWindowTitle(title)
