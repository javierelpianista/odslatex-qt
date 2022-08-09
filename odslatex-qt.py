from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTextEdit, QShortcut, QMessageBox
from PyQt5 import uic

from odslatex.main import convert_table, beautify_body, list_tables
import sys


form_class = uic.loadUiType("main.ui")[0]  # Load the UI

class ModQTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setCurrentFont(QtGui.QFont('Deja Vu Sans Mono'))
        self.setFontPointSize(10)
        self.setLineWrapMode(self.NoWrap)

class MyWindowClass(QMainWindow, form_class):
    # Signals
    file_opened = pyqtSignal(str)

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.tabWidget.clear()
        self.textEdits = []

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
        table_names = list_tables(filename=fileName, return_list=True)
        
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

        clipboard.setText(self.textEdits[n].toPlainText())
        self.statusbar.showMessage('Table copied to clipboard!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clipboard = app.clipboard()
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()
