import sys

from PyQt5.QtWidgets import QApplication

from .windows import PDFAppWindow


def main() -> None:
    application = QApplication(sys.argv)
    window = PDFAppWindow()
    window.show()
    application.exec_()


if __name__ == '__main__':
    main()
