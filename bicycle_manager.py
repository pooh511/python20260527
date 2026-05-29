import os
import sqlite3

from openpyxl import Workbook
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QSpinBox,
)

DB_PATH = os.path.join(os.path.dirname(__file__), "bicycle_manager.db")


class BicycleManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚲 자전거 관리 앱")
        self.resize(1000, 700)

        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self._setup_database()

        central = QWidget()
        central.setObjectName("root")
        self.setCentralWidget(central)

        central.setStyleSheet(
            """
            QWidget#root {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #020617, stop:0.45 #031224, stop:1 #00060f);
            }
            QWidget#card {
                background: rgba(6, 12, 24, 0.82);
                border: 1px solid rgba(56, 189, 248, 0.28);
                border-radius: 24px;
            }
            QLabel#title {
                color: #f8fafc;
                font: 700 30px "Segoe UI";
            }
            QLabel#subtitle {
                color: #93c5fd;
                font: 500 12px "Segoe UI";
            }
            QLabel#status {
                color: #67e8f9;
                font: 600 12px "Segoe UI";
            }
            QLabel {
                color: #e2e8f0;
            }
            QLineEdit, QSpinBox {
                background: rgba(2, 6, 23, 0.96);
                color: #f8fafc;
                border: 1px solid rgba(96, 165, 250, 0.32);
                border-radius: 12px;
                padding: 10px 12px;
                min-height: 20px;
            }
            QLineEdit:focus, QSpinBox:focus {
                border-color: #22c55e;
            }
            QPushButton {
                border-radius: 12px;
                padding: 11px 16px;
                color: #fff;
                font: 700 11px "Segoe UI";
            }
            QPushButton#primary {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #14b8a6);
            }
            QPushButton#secondary {
                background: rgba(14, 28, 46, 0.94);
                border: 1px solid rgba(148, 163, 184, 0.28);
            }
            QPushButton#danger {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #fb7185, stop:1 #ef4444);
            }
            QPushButton:hover {
                opacity: 0.92;
            }
            QTableWidget {
                background: rgba(2, 6, 23, 0.9);
                border: 1px solid rgba(56, 189, 248, 0.28);
                border-radius: 18px;
                color: #f8fafc;
                gridline-color: rgba(14, 116, 144, 0.32);
            }
            QHeaderView::section {
                background-color: rgba(8, 15, 28, 0.96);
                color: #d0f2ff;
                padding: 12px 10px;
                border: none;
                font: 700 11px "Segoe UI";
            }
            QTableWidget::item {
                padding: 10px 12px;
                border-bottom: 1px solid rgba(14, 116, 144, 0.2);
            }
            QTableWidget::item:selected {
                background: rgba(8, 145, 178, 0.55);
                color: #ffffff;
            }
            QTableWidget::alternate-background {
                background: rgba(3, 9, 18, 0.75);
            }
            """
        )

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(18)

        header_widget = QWidget()
        header_widget.setObjectName("card")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 18, 20, 18)
        header_layout.setSpacing(6)

        title_label = QLabel("🚲 자전거 재고 관리")
        title_label.setObjectName("title")
        subtitle_label = QLabel("SQLite 기반 재고 관리 · 입력, 수정, 삭제, 검색을 한 화면에서")
        subtitle_label.setObjectName("subtitle")
        self.status_label = QLabel("초기 데이터 로딩 중")
        self.status_label.setObjectName("status")

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addWidget(self.status_label)
        main_layout.addWidget(header_widget)

        form_widget = QWidget()
        form_widget.setObjectName("card")
        form_layout = QFormLayout(form_widget)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.id_edit = QSpinBox()
        self.id_edit.setRange(1, 1000000)
        self.id_edit.setValue(1)
        form_layout.addRow("ID", self.id_edit)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("예: 자전거 101")
        form_layout.addRow("이름", self.name_edit)

        self.price_edit = QSpinBox()
        self.price_edit.setRange(0, 100000000)
        self.price_edit.setValue(100000)
        self.price_edit.setPrefix("₩")
        form_layout.addRow("가격", self.price_edit)

        self.qty_edit = QSpinBox()
        self.qty_edit.setRange(0, 100000)
        self.qty_edit.setValue(1)
        form_layout.addRow("수량", self.qty_edit)

        main_layout.addWidget(form_widget)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.add_btn = QPushButton("추가")
        self.update_btn = QPushButton("수정")
        self.delete_btn = QPushButton("삭제")
        self.clear_btn = QPushButton("초기화")
        self.search_btn = QPushButton("검색")
        self.export_btn = QPushButton("엑셀로 출력")

        self.add_btn.setObjectName("primary")
        self.update_btn.setObjectName("primary")
        self.delete_btn.setObjectName("danger")
        self.clear_btn.setObjectName("secondary")
        self.search_btn.setObjectName("secondary")
        self.export_btn.setObjectName("primary")

        self.add_btn.clicked.connect(self.add_record)
        self.update_btn.clicked.connect(self.update_record)
        self.delete_btn.clicked.connect(self.delete_record)
        self.clear_btn.clicked.connect(self.clear_form)
        self.search_btn.clicked.connect(self.search_records)
        self.export_btn.clicked.connect(self.export_to_excel)

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.search_btn)
        button_layout.addWidget(self.export_btn)
        main_layout.addLayout(button_layout)

        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        search_label = QLabel("검색어")
        search_label.setStyleSheet("font: 700 11px 'Segoe UI'; color: #f8fafc;")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("이름 또는 ID를 입력하세요")
        self.search_box.setClearButtonEnabled(True)
        self.search_box.setMinimumHeight(38)
        self.search_box.returnPressed.connect(self.search_records)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)
        main_layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "이름", "가격", "수량"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.cellClicked.connect(self.fill_form_from_row)
        main_layout.addWidget(self.table)

        self.refresh_table()

    def _setup_database(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Bycle (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                qty INTEGER NOT NULL
            )
            """
        )

        existing = cur.execute("SELECT COUNT(*) FROM Bycle").fetchone()[0]
        if existing == 0:
            sample_rows = []
            for idx in range(1, 101):
                name = f"자전거 {idx:03d}"
                price = 50000 + (idx * 350)
                qty = (idx % 10) + 1
                sample_rows.append((idx, name, price, qty))
            cur.executemany(
                "INSERT INTO Bycle(id, name, price, qty) VALUES (?, ?, ?, ?)",
                sample_rows,
            )
            self.conn.commit()

    def refresh_table(self, rows=None):
        if rows is None:
            rows = self.fetch_all()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "이름", "가격", "수량"])

        for row_idx, row in enumerate(rows):
            id_item = QTableWidgetItem(str(row["id"]))
            name_item = QTableWidgetItem(str(row["name"]))
            price_item = QTableWidgetItem(f"{row['price']:,}")
            qty_item = QTableWidgetItem(str(row["qty"]))

            id_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

            self.table.setItem(row_idx, 0, id_item)
            self.table.setItem(row_idx, 1, name_item)
            self.table.setItem(row_idx, 2, price_item)
            self.table.setItem(row_idx, 3, qty_item)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.resizeRowsToContents()

        if rows:
            self.status_label.setText(f"현재 {len(rows)}건의 자전거가 등록되어 있습니다.")
        else:
            self.status_label.setText("검색 결과가 없습니다.")

    def fetch_all(self):
        cur = self.conn.cursor()
        return cur.execute("SELECT id, name, price, qty FROM Bycle ORDER BY id").fetchall()

    def add_record(self):
        try:
            item_id = int(self.id_edit.value())
            name = self.name_edit.text().strip()
            price = int(self.price_edit.value())
            qty = int(self.qty_edit.value())
        except ValueError:
            QMessageBox.warning(self, "입력 오류", "숫자 필드에 올바른 값을 입력하세요.")
            return

        if not name:
            QMessageBox.warning(self, "입력 오류", "이름을 입력하세요.")
            return

        cur = self.conn.cursor()
        existing = cur.execute("SELECT 1 FROM Bycle WHERE id = ?", (item_id,)).fetchone()
        if existing:
            QMessageBox.warning(self, "중복 오류", f"ID {item_id}는 이미 존재합니다.")
            return

        cur.execute(
            "INSERT INTO Bycle(id, name, price, qty) VALUES (?, ?, ?, ?)",
            (item_id, name, price, qty),
        )
        self.conn.commit()
        QMessageBox.information(self, "추가 완료", "데이터가 추가되었습니다.")
        self.refresh_table()
        self.clear_form()

    def update_record(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "수정 오류", "수정할 행을 선택하세요.")
            return

        try:
            item_id = int(self.id_edit.value())
            name = self.name_edit.text().strip()
            price = int(self.price_edit.value())
            qty = int(self.qty_edit.value())
        except ValueError:
            QMessageBox.warning(self, "입력 오류", "숫자 필드에 올바른 값을 입력하세요.")
            return

        if not name:
            QMessageBox.warning(self, "입력 오류", "이름을 입력하세요.")
            return

        cur = self.conn.cursor()
        cur.execute(
            "UPDATE Bycle SET name=?, price=?, qty=? WHERE id=?",
            (name, price, qty, item_id),
        )
        if cur.rowcount == 0:
            QMessageBox.warning(self, "수정 오류", "해당 ID의 데이터가 없습니다.")
            return

        self.conn.commit()
        QMessageBox.information(self, "수정 완료", "데이터가 수정되었습니다.")
        self.refresh_table()
        self.clear_form()

    def delete_record(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "삭제 오류", "삭제할 행을 선택하세요.")
            return

        item_id = int(self.table.item(selected, 0).text())
        cur = self.conn.cursor()
        cur.execute("DELETE FROM Bycle WHERE id = ?", (item_id,))
        self.conn.commit()
        QMessageBox.information(self, "삭제 완료", "데이터가 삭제되었습니다.")
        self.refresh_table()
        self.clear_form()

    def clear_form(self):
        self.id_edit.setValue(1)
        self.name_edit.clear()
        self.price_edit.setValue(100000)
        self.qty_edit.setValue(1)
        self.table.clearSelection()

    def fill_form_from_row(self, row, column):
        item_id = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        price = self.table.item(row, 2).text().replace(",", "")
        qty = self.table.item(row, 3).text()

        self.id_edit.setValue(int(item_id))
        self.name_edit.setText(name)
        self.price_edit.setValue(int(price))
        self.qty_edit.setValue(int(qty))

    def search_records(self):
        keyword = self.search_box.text().strip()
        if not keyword:
            self.refresh_table()
            return

        cur = self.conn.cursor()
        try:
            item_id = int(keyword)
            rows = cur.execute(
                "SELECT id, name, price, qty FROM Bycle WHERE id = ? ORDER BY id",
                (item_id,),
            ).fetchall()
        except ValueError:
            rows = cur.execute(
                "SELECT id, name, price, qty FROM Bycle WHERE name LIKE ? ORDER BY id",
                (f"%{keyword}%",),
            ).fetchall()

        self.refresh_table(rows)

    def export_to_excel(self):
        default_path = os.path.join(os.path.dirname(__file__), "bicycle_export.xlsx")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "엑셀 파일 저장",
            default_path,
            "Excel 파일 (*.xlsx)",
        )

        if not file_path:
            self.status_label.setText("엑셀 저장을 취소했습니다.")
            return

        if not file_path.lower().endswith(".xlsx"):
            file_path = f"{file_path}.xlsx"

        try:
            rows = self.fetch_all()
            wb = Workbook()
            ws = wb.active
            ws.title = "Bycle"
            ws.append(["ID", "이름", "가격", "수량"])

            for row in rows:
                ws.append([row["id"], row["name"], row["price"], row["qty"]])

            ws.freeze_panes = "A2"
            wb.save(file_path)

            self.status_label.setText(f"엑셀 저장 완료: {os.path.basename(file_path)}")
            QMessageBox.information(self, "엑셀 저장", f"엑셀 파일이 저장되었습니다.\n{file_path}")
        except Exception as exc:
            self.status_label.setText("엑셀 저장 실패")
            QMessageBox.warning(self, "엑셀 저장 오류", f"엑셀 저장 중 오류가 발생했습니다.\n{exc}")

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        event.accept()


def main():
    import sys

    app = QApplication(sys.argv)
    window = BicycleManagerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
