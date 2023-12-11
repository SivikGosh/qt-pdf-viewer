import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError

from design import Ui_MainWindow


class PDFAppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_file.clicked.connect(self.open_file)
        self.page_list = []
        self.next_page.clicked.connect(lambda: self.show_next_page(self.page_list))
        self.prev_page.clicked.connect(lambda: self.show_prev_page(self.page_list))
        self.count = 0
        self.x = None
        self.y = None

    def open_file(self):
        try:
            self.__clear_tmp_folder()
            self.next_page.setEnabled(True)
            self.prev_page.setEnabled(False)
            self.count = 1

            file_dir = QFileDialog.getOpenFileName(self, 'Open file', '', "PDF files (*.pdf)")[0]
            pages = convert_from_path(file_dir, size=800)

            for num, page in enumerate(pages):
                page.save(f'tmp/page_{num+1}.png', 'PNG')
                self.page_list.append(f'page_{num+1}.png')

            pixmap = QPixmap(f'tmp/{self.page_list[0]}')
            self.view_page.setPixmap(pixmap)
            self.view_page.setMouseTracking(True)
        except PDFPageCountError:
            self.view_page.pixmap()

    @staticmethod
    def __clear_tmp_folder():
        files = os.listdir('tmp')
        for file in files:
            os.remove(f'tmp/{file}')

    def show_next_page(self, lis):
        if self.count < len(lis):
            self.count += 1
        self.view_page.setPixmap(QPixmap(f'tmp/{lis[self.count-1]}'))
        if self.count > 1:
            self.prev_page.setEnabled(True)
        if self.count == len(lis):
            self.next_page.setEnabled(False)

    def show_prev_page(self, lis):
        self.count -= 1
        self.view_page.setPixmap(QPixmap(f'tmp/{lis[self.count-1]}'))
        if self.count < len(lis):
            self.next_page.setEnabled(True)
        if self.count-1 < 1:
            self.prev_page.setEnabled(False)

    def mousePressEvent(self, event):
        pen = QPen(Qt.red, 3)
        qp = QPainter()
        qp.begin(self.view_page.pixmap())
        qp.setPen(pen)
        x = int(event.pos().x())
        y = int(event.pos().y())
        qp.drawPoint(x, y)
        self.x = x
        self.y = y
        self.view_page.update()

    def mouseReleaseEvent(self, event):
        pen = QPen(Qt.red, 3)
        qp = QPainter()
        qp.begin(self.view_page.pixmap())
        qp.setPen(pen)
        x = int(event.pos().x())
        y = int(event.pos().y())
        qp.drawRect(self.x, self.y, x-self.x, y-self.y)
        self.view_page.update()


def main():
    app = QApplication(sys.argv)
    win = PDFAppWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
