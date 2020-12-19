# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import Qt, QEvent
from . import shared


class WriterWidget(QWidget):
    """Widget hosting the actual Document that the user is modifying."""

    def __init__(self, parent=None, transliterate=True):
        """Initialise the WriterWidget."""
        super().__init__(parent)
        self.setLayout(QVBoxLayout(parent))

        self.transliterate = transliterate  # Whether to try and transliterate to IPA

        self.text_edit = QTextEdit(parent)
        self.layout().addWidget(self.text_edit)

        # Let the text_edit handle all focus requests
        self.setFocusProxy(self.text_edit)
        self.text_edit.installEventFilter(self)

        # TODO: Add settngs options for WriterWidget font family and size
        self.setStyleSheet("QTextEdit { font-family:Times; font-size:14pt }")

    def eventFilter(self, obj, event):
        """Filter keyboard input to feed into transliteration mechanism if applicable"""
        # We want to filter all these keys:
        filtered_keys = "1234567890-=!\"£$%^&*()_+"
        filtered_keys += "{}[]:;@'~#|\\<>,.?/"
        filtered_keys += "abcdefghijklmnopqrstuvwxzy"
        filtered_keys += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if event.type() == QEvent.KeyPress:
            if event.text() and event.text() in filtered_keys:
                if event.modifiers() == Qt.NoModifier or event.modifiers() == Qt.ShiftModifier:
                    self.insert_char(event.text())
                    return True  # Make sure Qt will consider the event "handled" and not insert text itself
        # If not filtering that key return 0 so event handling will go the normal course
        return 0

    def clear(self):
        """Clear the text in the current document."""
        # TODO: Somehow change this so that the clearing becomes part of the Undo/Redo stack.
        # Currently after calling .clear() there's no Undo available. Why?
        # Maybe just replace all the text with nothing manually?
        return self.text_edit.clear()

    def copy(self):
        """Copy current selection to clipboard. If no slection, copy everything."""
        # TODO: Needs to make sure that iff no text is selected ALL text is copied
        return self.text_edit.copy()

    def cut(self):
        """Cut current selection to clipboard. If no selection, cut everything."""
        # Needs to make sure that iff no text is selected, ALL text is cut
        return self.text_edit.cut()

    def paste(self):
        """Paste clipboard contents at current cursor position."""
        return self.text_edit.paste()

    def undo(self):
        """Undo the last modification of the document."""
        return self.text_edit.undo()

    def redo(self):
        """Redo the last modification of the document."""
        return self.text_edit.redo()

    def set_document(self, document):
        """Replace the document edited by the widget with document."""
        self.text_edit.setDocument(document)

    def set_transliterate(self, transliterate=True):
        """Turn IPA transliteration mode on or off."""
        self.transliterate = bool(transliterate)

    def get_document(self):
        """Get the current document edited by the widget."""
        return self.text_edit.document()

    def get_transliterate():
        """Indicate whether IPA transliteration is active or not."""
        return self.transliterate

    def insert_char(self, char):
        """Insert character at current curser position, inc. transliteration if applicable."""
        if self.transliterate:
            if char in shared.ipa_shortcuts:
                char = shared.ipa_shortcuts[char]['char']
        self.text_edit.textCursor().insertText(char)

    def insert_text(self, text):
        """Insert text at current cursor position without transliteration."""
        self.text_edit.textCursor().insertText(text)
