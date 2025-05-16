import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QCheckBox, QPushButton,
    QListWidget, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt


class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.setFixedSize(550, 450)
        self.books = []

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("Library Management System")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Input fields
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.year_input = QLineEdit()

        layout.addLayout(self._form_row("Title:", self.title_input))
        layout.addLayout(self._form_row("Author:", self.author_input))
        layout.addLayout(self._form_row("Year:", self.year_input))

        # eBook checkbox + input
        ebook_layout = QHBoxLayout()
        self.ebook_checkbox = QCheckBox("Is eBook?")
        self.ebook_checkbox.stateChanged.connect(self.toggle_ebook_input)
        ebook_layout.addWidget(self.ebook_checkbox)

        self.ebook_input = QLineEdit()
        self.ebook_input.setPlaceholderText("Filename or URL")
        self.ebook_input.setEnabled(False)
        ebook_layout.addWidget(self.ebook_input)
        layout.addLayout(ebook_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Book")
        self.add_btn.clicked.connect(self.add_book)

        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.clicked.connect(self.remove_book)

        self.view_btn = QPushButton("View Books")
        self.view_btn.clicked.connect(self.view_books)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addWidget(self.view_btn)

        layout.addLayout(btn_layout)

        # Book List
        self.book_list = QListWidget()
        layout.addWidget(self.book_list)

        self.setLayout(layout)

    def _form_row(self, label_text, line_edit):
        row = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(60)
        row.addWidget(label)
        row.addWidget(line_edit)
        return row

    def toggle_ebook_input(self, state):
        if state == Qt.Checked:
            self.ebook_input.setEnabled(True)
        else:
            self.ebook_input.setText("")
            self.ebook_input.setEnabled(False)

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        year = self.year_input.text().strip()
        is_ebook = self.ebook_checkbox.isChecked()
        ebook_data = self.ebook_input.text().strip()

        if not title or not author or not year:
            QMessageBox.warning(self, "Error", "Please fill Title, Author, and Year")
            return

        if is_ebook:
            if not ebook_data or not all(c.isalnum() or c in ('_', '.', '/', ':') for c in ebook_data):
                QMessageBox.warning(self, "Error", "Enter a valid eBook filename or URL")
                return
        else:
            ebook_data = None

        book = {
            'Title': title,
            'Author': author,
            'Year': year,
            'eBook': ebook_data
        }
        self.books.append(book)
        QMessageBox.information(self, "Success", f"Book '{title}' added!")
        self.clear_fields()
        self.view_books()

    def remove_book(self):
        selected_items = self.book_list.selectedIndexes()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a book to remove.")
            return

        index = selected_items[0].row()
        book = self.books.pop(index)
        QMessageBox.information(self, "Removed", f"Removed book '{book['Title']}'")
        self.view_books()

    def view_books(self):
        self.book_list.clear()
        for idx, book in enumerate(self.books, 1):
            ebook_str = f" [eBook: {book['eBook']}]" if book['eBook'] else ""
            line = f"{idx}. {book['Title']} by {book['Author']} ({book['Year']}){ebook_str}"
            self.book_list.addItem(line)

    def clear_fields(self):
        self.title_input.clear()
        self.author_input.clear()
        self.year_input.clear()
        self.ebook_checkbox.setChecked(False)
        self.ebook_input.clear()
        self.ebook_input.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
