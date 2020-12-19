# IPA Pad

IPA Pad (ipapad) is a text editor with integrated switchable keyboard remapping into the Internal Phonetic Alphabet. With a little bit of practice this allows you to fluently type text in IPA without the need to install a specific keyboard layout, which can be difficult both to make work and gain permission for on workplace or lab machines.

## Installation

### On Linux, Unix, MacOS via the terminal

If you have Python (version 3.6+) already installed, you can download the wheel (*.whl) file and then run the following command from the terminal to install ipapad:
```bash
pip install ipapad-{version}.whl
```

### On Windows

If you are on Windows you might prefer the windows installer (currently only for Windows 10, 64bit), as this will also create the regular shortcuts in the start menu. The Windows installer includes its own python interpreter, so there's no need to install anything else.

## Usage

### Launching IPA Pad

You can lanuch ipapad either via any menu shortcuts created or simply by typing `ipapad` on the terminal. If you want to monitor the error and debuggin outputs of ipapad, launch it using the command `ipapad-cli`.

### Typing IPA with IPA Pad

 IPA Pad is different to other text editors in that it has an option to dynamically remap your keyboard to allow you to type in IPA. This is called "IPA Mode".

 When you first launch IPA Pad, it will have IPA Mode activated. Go ahead and type `/hEl@U w3:ld/` on your keyboard, and you will see that the text appears as /hɛləʊ wɜːld/. To toggle IPA Mode on or off, either use the menu or toolbar button with the IPA type logo, or press `CTRL+L`. Text you type when IPA Mode is off will be entered as regular keyboard input. The transliteration method is loosely based on the latex package TIPA, but with key combinations instead of sequences for some characters. To see a full (and searchable) list of the mappings, go to Help -> IPA Character Map.

 While IPA Pad has the usual features of a basic text editor like opening/saving files, undo, redo, and so on, there are two shortcuts that you may not find as often. One is an option to copy all the text in the window, and another to clear all the text in the window (careful: there's currently no undo available after doing this!). These two buttons will be useful if you use IPA Pad on the side while writing a document in some other software, e.g. in your favourite office suite. Just type the IPA text in IPA Pad, click copy all, paste it in your document and continue to work.

### Integrating IPA Pad into your own project

You can also use IPA Pad as an interface for another python script, as follows:
```python
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from ipapad.main_window import MainWindow

# Set up IPA Pad
app = QApplication() # This may of course be your own app's instance
ipapad_mw = MainWindow()

# Put some text inside the text editor
ipapad_mw.top_widget.insert_text("Hello, IPA Pad!")

# Run the app
app.exec_()

# Read the contents of the text editor (this returns a PySide6.QtGui.QTextDocument)
ipapad_mw.top_widget.get_document()
```

Another option if your own project is in Qt already would of course be to just use ipapad's `WriterWidget`, which has an API nearly identical to `QTextEdit` but ties in its own derivative of `QTextDocument` and has hooks to activate transliteration. It can be imported simply with `from ipapad import WriterWidget`.

## Contributing

Contributions are welcome. Feel free to make pull requests for smaller changes or implementations of planned features. For larger changes ideally try to get in touch beforehand to discuss what you would like to change.

## License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
