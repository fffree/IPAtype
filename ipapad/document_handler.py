
# -*- coding: utf-8 -*-

from PySide6.QtGui import QTextDocument, QFont


class Document(QTextDocument):
    """Document handler for IPAPad Documents."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # TODO: Make fonts available in settings
        self.setDefaultFont(QFont("Times, SansSerif", 14))
        self.filename = None

    @staticmethod
    def from_file(filename, parent=None):
        """
        Initialise a new IPAtype document from a file.

        Reads the file specified by filename, then initialises and returns a new
        instance of the IPAtype Document class with the files contents.
        Curretnly only supports plain text files.
        """
        with open(filename, encoding="utf-8") as file:
            text = ''.join(file.readlines())
        doc = Document(parent)
        doc.setPlainText(text)
        doc.set_filename(filename)
        doc.setModified(False)
        return doc

    def save_to_file(self, filename):
        """
        Save the IPA Document's contents to a file.

        Saves the contents of the IPA Document to the file specified by
        filename. Currently saves content as plain text only, in UTF-8 without
        BOM. Any existing file is overwritten without warning or confirmation.
        """
        with open(filename, "w", encoding="utf-8") as file:
            doc = self.toPlainText()
            file.write(doc)
        self.set_filename(filename)
        self.setModified(False)
        return True

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename
