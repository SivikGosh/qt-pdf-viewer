import sys
from PyQt5.QtWidgets import QLabel, QFileDialog, QMainWindow, QApplication
from PyQt5.QtGui import QPixmap

from design import Ui_MainWindow
from pdf2image import convert_from_path
from PyQt5.QtGui import QPixmap

class PDFAppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_file.clicked.connect(self.open_file)

    def open_file(self):
        images = convert_from_path('test.pdf', fmt='jpg')
        # images[0].save('test_!!!!.jpg', 'JPEG')
        # print(images[0].show())
        # self.view_page.setText(image)
        self.view_page.setPixmap(QPixmap(images[0].))


def main():
    app = QApplication(sys.argv)
    win = PDFAppWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
