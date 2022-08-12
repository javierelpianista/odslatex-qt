# odslatex-qt: a Qt5 interface to odslatex.
#
# Copyright (c) 2022, Javier Garcia.
#
# This file is part of odslatex-qt.
#
# odslatex-qt is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# odslatex-qt is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details.
#
# You should have received a copy of the GNU General Public License along with
# odslatex-qt. If not, see <https://www.gnu.org/licenses/>.

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTextEdit, QShortcut, QMessageBox
from PyQt5 import uic

from odslatex.main import convert_table, beautify_body, list_tables
import sys
import zipfile

if sys.version_info < (3,9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

pkg = importlib_resources.files("odslatex_qt")
ui_file = pkg / "main.ui"

form_class = uic.loadUiType(ui_file)[0]  # Load the UI

class ModQTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setCurrentFont(QtGui.QFont('Deja Vu Sans Mono'))
        self.setFontPointSize(10)
        self.setLineWrapMode(self.NoWrap)

class MyWindowClass(QMainWindow, form_class):
    # Signals
    file_opened = pyqtSignal(str)

    def __init__(self, app, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.tabWidget.clear()
        self.textEdits = []

        self.clipboard = app.clipboard()

        # Keyboard shortcuts
        self.shortcut_quit = QShortcut(QtGui.QKeySequence('Ctrl+Q'), self)
        self.shortcut_quit.activated.connect(self.quit_program)

    def open_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
        if fileName:
            print(fileName)
            self.file_opened.emit(fileName)

    def quit_program(self):
        ret = QMessageBox.question(
                self,
                '',
                'Are you sure you want to quit?',
                QMessageBox.Yes | QMessageBox.No 
                )

        if ret == QMessageBox.Yes:
            sys.exit(0)

    def help(self):
        print('help')

    def show_file(self, fileName):
        try: 
            table_names = list_tables(filename=fileName, return_list=True)
        except zipfile.BadZipFile:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('The selected file does not appear to be a LibreOffice Calc file.')
            msg.setWindowTitle('Error!')
            msg.exec_()
            return
        
        for n, name in enumerate(table_names):
            self.textEdits.append(ModQTextEdit())
            self.tabWidget.addTab(
                    self.textEdits[n],
                    '{:2d}: {}'.format(n, name)
                    )
            text = convert_table( filename = fileName, which = n)

            text = beautify_body(text)
            self.textEdits[n].setText(text)
        
        ntabs = len(table_names)
        if ntabs == 1:
            text_str = 'File {} opened. {} table detected.'
        else:
            text_str = 'File {} opened. {} tables detected.'

        self.statusbar.showMessage(text_str.format(fileName, len(table_names)))


    def copy_to_clipboard(self):
        n = self.tabWidget.currentIndex()

        self.clipboard.setText(self.textEdits[n].toPlainText())
        self.statusbar.showMessage('Table {} copied to clipboard!'.format(n))


def main():
    app = QApplication(sys.argv)
    myWindow = MyWindowClass(app)
    myWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
