from __future__ import annotations

import os
from typing import List, Optional

from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from src.design import Ui_MainWindow


class PDFAppWindow(QMainWindow, Ui_MainWindow):

    def __init__(self: PDFAppWindow) -> None:
        super().__init__()
        self.setupUi(self)
        self._init_state()
        self._connect_signals()

    def _init_state(self: PDFAppWindow) -> None:
        self.pages = []
        self.count = 0
        self.x_pos = None
        self.y_pos = None

    def _connect_signals(self: PDFAppWindow) -> None:
        self.load_file.clicked.connect(self.open_file)
        self.next_page.clicked.connect(lambda: self._to_next_page(self.pages))
        self.prev_page.clicked.connect(lambda: self._to_prev_page(self.pages))

    def open_file(self: PDFAppWindow) -> None:
        try:
            self._clear_temporary_folder()
            self.next_page.setEnabled(True)
            self.prev_page.setEnabled(False)
            self.count = 1
            file_dir = QFileDialog.getOpenFileName(self, filter='PDF (*.pdf)')
            pages = convert_from_path(file_dir[0], size=800)
            for num, page in enumerate(pages):
                page.save(f'tmp/page_{num+1}.png', 'PNG')
                self.pages.append(f'page_{num+1}.png')
            pixmap = QPixmap(f'tmp/{self.pages[0]}')
            self.view_page.setPixmap(pixmap)
            self.view_page.setMouseTracking(True)
        except PDFPageCountError:
            self.view_page.pixmap()

    def _to_next_page(self: PDFAppWindow, pages: List) -> None:
        if self.count < len(pages):
            self.count += 1
        self.view_page.setPixmap(QPixmap(f'tmp/{pages[self.count-1]}'))
        if self.count > 1:
            self.prev_page.setEnabled(True)
        if self.count == len(pages):
            self.next_page.setEnabled(False)

    def _to_prev_page(self: PDFAppWindow, pages: List) -> None:
        self.count -= 1
        self.view_page.setPixmap(QPixmap(f'tmp/{pages[self.count-1]}'))
        if self.count < len(pages):
            self.next_page.setEnabled(True)
        if self.count-1 < 1:
            self.prev_page.setEnabled(False)

    def _clear_temporary_folder(self: PDFAppWindow) -> None:
        files = os.listdir('tmp')
        for file in files:
            os.remove(f'tmp/{file}')

    def mousePressEvent(
        self: PDFAppWindow,
        event: Optional[QMouseEvent]
    ) -> None:
        pen = QPen(Qt.red, 3)
        painter = QPainter()
        painter.begin(self.view_page.pixmap())
        painter.setPen(pen)
        x_pos = int(event.pos().x())
        y_pos = int(event.pos().y())
        painter.drawPoint(x_pos, y_pos)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.view_page.update()

    def mouseReleaseEvent(
        self: PDFAppWindow,
        event: Optional[QMouseEvent]
    ) -> None:
        pen = QPen(Qt.red, 3)
        painter = QPainter()
        painter.begin(self.view_page.pixmap())
        painter.setPen(pen)
        x_pos = int(event.pos().x())
        y_pos = int(event.pos().y())
        painter.drawRect(
            self.x_pos,
            self.y_position,
            x_pos - self.x_pos,
            y_pos - self.y_pos
        )
        self.view_page.update()
