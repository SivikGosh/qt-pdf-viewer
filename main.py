import sys
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel
import os
from PyQt5.QtCore import Qt

from design import Ui_MainWindow
from pdf2image import convert_from_path
from PyQt5.QtGui import QPixmap, QPainter


class PDFAppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_file.clicked.connect(self.open_file)
        self.page_list = []
        self.next_page.clicked.connect(lambda: self.show_next_page(self.page_list))
        self.prev_page.clicked.connect(lambda: self.show_prev_page(self.page_list))
        self.count = 0
        self.pos1 = [100, 100]
        self.pos2 = [100, 100]
        self.view_page.setMouseTracking(True)

    def open_file(self):
        self.__clear_tmp_folder()
        self.next_page.setEnabled(True)
        self.prev_page.setEnabled(False)
        self.count = 1

        file_dir = QFileDialog.getOpenFileName(self, 'Open file', '', "PDF files (*.pdf)")[0]
        pages = convert_from_path(file_dir, size=(800,))

        for num, page in enumerate(pages):
            page.save(f'tmp/page_{num+1}.png', 'PNG')
            self.page_list.append(f'page_{num+1}.png')

        pixmap = QPixmap(f'tmp/{self.page_list[0]}')
        self.view_page.setPixmap(pixmap)
        # self.draw_something(pixmap)

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

    def drawPoints(self, pos):
        print("Call draw points")
        pen = Qt.QPen(Qt.Qt.black, 10)
        qp = Qt.QPainter()
        qp.begin(self.image.pixmap())
        qp.setPen(pen)
        qp.drawPoint(pos.x(), pos.y())
        self.image.update()

    def get_pos(self, event):
        X = event.pos().x()
        y = event.pos().y()
        self.drawPoints(event.pos())


def main():
    app = QApplication(sys.argv)
    win = PDFAppWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
