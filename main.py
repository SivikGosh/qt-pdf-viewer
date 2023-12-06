import sys
from PyQt5.QtWidgets import QLabel, QFileDialog, QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyPDF2 import PdfReader, PdfWriter

from design import Ui_MainWindow
from pdf2image import convert_from_path
from PyQt5.QtGui import QPixmap
from PIL import Image


class PDFAppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_file.clicked.connect(self.open_file)
        self.page_list = []
        self.page_count = 0
        self.next_page.clicked.connect(lambda: self.show_next_page(self.page_count, self.page_list))

    def open_file(self):
        file_dir = QFileDialog.getOpenFileName(self, 'Open file', '', "PDF files (*.pdf)")[0]
        pages_list = []
        pages = convert_from_path(file_dir, size=(800,))
        for count, page in enumerate(pages):
            page.save(f'tmp/out{count}.png', 'PNG')
            pages_list.append(f'out{count}.png')
        self.view_page.setPixmap(QPixmap(f'tmp/{pages_list[0]}'))
        self.page_count = len(pages_list)
        self.page_list = pages_list

    def show_next_page(self, i, lis):
        self.view_page.setPixmap(QPixmap(f'tmp/{lis[1]}'))

        # reader = PdfReader(file_dir)
        # for i in range(len(reader.pages)):
        #     writer = PdfWriter()
        #     writer.add_page(reader.pages[i])
        #     with open(f'tmp/{i+1}_page.pdf', 'wb') as f:
        #         writer.write(f)
        #     image = convert_from_path(f'tmp/{i+1}_page.pdf', fmt='png')
        #     print(image.)
        # print(pages_list)
        # self.view_page.setPixmap(QPixmap(fname))
        # images = convert_from_path('test.pdf', fmt='jpg')
        # # images[0].save('test_!!!!.jpg', 'JPEG')
        # # print(images[0].show())
        # # self.view_page.setText(image)
        # self.view_page.setPixmap(QPixmap(file_dir))


def main():
    app = QApplication(sys.argv)
    win = PDFAppWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
