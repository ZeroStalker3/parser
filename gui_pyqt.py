# Программа реализованная на PyQt6
# Парсинг ноутбуков с YandexMarket


import sys
import csv
import os
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QSpinBox,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QFileDialog
)
from PyQt6.QtCore import Qt
from main import *

class ParserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Парсер Яндекс.Маркет — Ноутбуки")
        self.setGeometry(300, 200, 800, 600)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setStyleSheet("font-family: Segoe UI; font-size: 14px;")

        # Заголовок
        self.title = QLabel("📦 Парсер Яндекс.Маркет")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.layout.addWidget(self.title)

        # Выбор количества товаров
        row = QHBoxLayout()
        self.label_count = QLabel("Количество товаров:")
        self.spin_count = QSpinBox()
        self.spin_count.setRange(1, 200)
        self.spin_count.setValue(50)
        row.addWidget(self.label_count)
        row.addWidget(self.spin_count)
        self.layout.addLayout(row)

        # Выбор максимальной и минимальной суммы товара
        row = QHBoxLayout()
        self.entry_min_price_label = QLabel("Минимальная сумма:")
        self.entry_min_price = QSpinBox()
        self.entry_min_price.setRange(1, 2147483647)
        self.entry_min_price.setValue(10000)
        row.addWidget(self.entry_min_price_label)
        row.addWidget(self.entry_min_price)
        self.layout.addLayout(row)

        row = QHBoxLayout()
        self.entry_max_price_label = QLabel("Максимальная сумма:")
        self.entry_max_price = QSpinBox()
        self.entry_max_price.setRange(1, 2147483647)
        self.entry_max_price.setValue(50000)
        row.addWidget(self.entry_max_price_label)
        row.addWidget(self.entry_max_price)
        self.layout.addLayout(row)

        # Кнопки
        self.btn_parse = QPushButton("▶️ Начать парсинг")
        self.btn_open_csv = QPushButton("📂 Открыть CSV")

        self.btn_parse.clicked.connect(self.start_parsing)
        self.btn_open_csv.clicked.connect(self.open_csv)

        row_btns = QHBoxLayout()
        row_btns.addWidget(self.btn_parse)
        row_btns.addWidget(self.btn_open_csv)
        self.layout.addLayout(row_btns)

        # Таблица
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

    def start_parsing(self):
        self.btn_parse.setEnabled(False)
        count = self.spin_count.value()
        min_price = self.entry_min_price.value()
        max_price = self.entry_max_price.value()
        threading.Thread(target=self.parse_and_reload, args=(count, min_price, max_price,), daemon=True).start()

    def parse_and_reload(self, count, min_price, max_price):
        run_parser(count, min_price, max_price)
        self.load_csv()
        self.btn_parse.setEnabled(True)

    def load_csv(self):
        csv_file = 'laptops.csv'
        if not os.path.exists(csv_file):
            return
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        self.table.setColumnCount(len(rows[0]))
        self.table.setHorizontalHeaderLabels(rows[0])
        self.table.setRowCount(len(rows) - 1)

        for row_idx, row_data in enumerate(rows[1:]):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(col_data))

        self.table.resizeColumnsToContents()

    def open_csv(self):
        path = os.path.abspath('laptops.csv')
        if os.path.exists(path):
            QFileDialog.getOpenFileName(self, "Открыть CSV", path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParserApp()
    window.show()
    sys.exit(app.exec())
