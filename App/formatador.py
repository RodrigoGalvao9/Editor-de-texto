from PySide6.QtGui import QTextCursor, QFont, QTextCharFormat, QTextBlockFormat
from PySide6.QtWidgets import QColorDialog

class Formatador:
    def __init__(self, text_edit):
        self.text_edit = text_edit
        self.default_font = QFont("Arial", 12)

    def toggle_bold(self):
        """Alterna entre negrito e normal no texto selecionado."""
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        format = cursor.charFormat()
        if format.fontWeight() == QFont.Bold:
            format.setFontWeight(QFont.Normal)
        else:
            format.setFontWeight(QFont.Bold)
        cursor.setCharFormat(format)

    def toggle_italic(self):
        """Alterna entre itálico e normal no texto selecionado."""
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        format = cursor.charFormat()
        format.setFontItalic(not format.fontItalic())
        cursor.setCharFormat(format)

    def toggle_underline(self):
        """Alterna entre sublinhado e sem sublinhado no texto selecionado."""
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        format = cursor.charFormat()
        format.setFontUnderline(not format.fontUnderline())
        cursor.setCharFormat(format)

    def increase_font_size(self):
        """Aumenta o tamanho da fonte do texto selecionado."""
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        format = cursor.charFormat()
        current_size = format.fontPointSize()
        format.setFontPointSize(current_size + 2 if current_size else 14)
        cursor.setCharFormat(format)

    def decrease_font_size(self):
        """Diminui o tamanho da fonte do texto selecionado."""
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        format = cursor.charFormat()
        current_size = format.fontPointSize()
        format.setFontPointSize(max(current_size - 2, 8) if current_size else 12)
        cursor.setCharFormat(format)

    def change_text_color(self):
        """Abre um diálogo para alterar a cor do texto selecionado."""
        color = QColorDialog.getColor()
        if color.isValid():
            cursor = self.text_edit.textCursor()
            format = cursor.charFormat()
            format.setForeground(color)
            cursor.setCharFormat(format)

    def change_font_family(self, font_family: str) -> None:
        cursor = self.text_edit.textCursor()
        char_format = cursor.charFormat()
        char_format.setFontFamilies([font_family])

        if cursor.hasSelection():
            cursor.mergeCharFormat(char_format)
        else:
            self.text_edit.setCurrentCharFormat(char_format)

    def reset_formatting(self):
        """Reseta a formatação do texto no QTextEdit para o estado original."""
        cursor = self.text_edit.textCursor()
        cursor.beginEditBlock()

        cursor.select(QTextCursor.Document)

        # Reseta a formatação de caracteres (cor, negrito, etc)
        default_format = QTextCharFormat()
        cursor.setCharFormat(default_format)

        # Reseta a formatação de parágrafo (alinhamento, recuo, etc)
        block_format = QTextBlockFormat()
        cursor.setBlockFormat(block_format)

        cursor.endEditBlock()

        self.text_edit.setTextCursor(cursor)