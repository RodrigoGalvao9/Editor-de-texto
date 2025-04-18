from PySide6.QtGui import QTextCursor, QTextDocument, QTextCharFormat
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton
from spellchecker import SpellChecker

class FerramentasTexto:
    def __init__(self, text_edit):
        self.text_edit = text_edit
        self.spell_checker = SpellChecker(language='pt')

    def check_spelling(self):
        """Verifica a ortografia do texto no QTextEdit e sublinha palavras incorretas."""
        document = self.text_edit.document()
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        text = cursor.selectedText()

        words = text.split()
        misspelled = self.spell_checker.unknown(words)

        # Limpa formatação anterior
        cursor.beginEditBlock()
        cursor.setCharFormat(QTextCharFormat())
        cursor.endEditBlock()

        for word in misspelled:
            # Cria um novo cursor para busca
            highlight_cursor = QTextCursor(document)
            flags = QTextDocument.FindCaseSensitively | QTextDocument.FindWholeWords

            while True:
                highlight_cursor = document.find(word, highlight_cursor, flags)
                if highlight_cursor.isNull():
                    break

                format = QTextCharFormat()
                format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
                format.setUnderlineColor(Qt.red)
                highlight_cursor.mergeCharFormat(format)

    def search_text(self, query, replace_with=None):
        """Pesquisa e, opcionalmente, substitui texto no QTextEdit."""
        document = self.text_edit.document()
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.Start) 

        flags = QTextDocument.FindCaseSensitively | QTextDocument.FindWholeWords

        while True:
            found_cursor = document.find(query, cursor, flags)

            if found_cursor.isNull():
                break

            self.text_edit.setTextCursor(found_cursor) 
            if replace_with:
                found_cursor.insertText(replace_with)
            else:
                # Realça o texto encontrado
                highlight_format = QTextCharFormat()
                highlight_format.setBackground(Qt.yellow)
                found_cursor.mergeCharFormat(highlight_format)

            cursor = found_cursor

    def search_and_replace(self):
        """Caixa de diálogo para pesquisar e substituir texto."""
        dialog = QDialog()
        dialog.setWindowTitle("Pesquisar e Substituir")
        dialog_layout = QVBoxLayout()

        search_label = QLabel("Procurar:")
        search_input = QLineEdit()
        dialog_layout.addWidget(search_label)
        dialog_layout.addWidget(search_input)

        replace_label = QLabel("Substituir por:")
        replace_input = QLineEdit()
        dialog_layout.addWidget(replace_label)
        dialog_layout.addWidget(replace_input)

        button_layout = QHBoxLayout()
        search_button = QPushButton("Procurar")
        replace_button = QPushButton("Substituir")
        button_layout.addWidget(search_button)
        button_layout.addWidget(replace_button)
        dialog_layout.addLayout(button_layout)

        dialog.setLayout(dialog_layout)

        # Conectar ações dos botões
        def search():
            query = search_input.text()
            if query:
                self.search_text(query)

        def replace():
            query = search_input.text()
            replace_with = replace_input.text()
            if query and replace_with:
                self.search_text(query, replace_with=replace_with)

        search_button.clicked.connect(search)
        replace_button.clicked.connect(replace)

        # Pré-preenche o campo com texto selecionado, se houver
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            search_input.setText(selected_text)

        dialog.exec()