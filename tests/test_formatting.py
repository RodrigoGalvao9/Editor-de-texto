import pytest
from unittest.mock import patch
from PySide6.QtGui import QTextCursor, QColor
from PySide6.QtWidgets import QTextEdit, QColorDialog
from App.formatador import Formatador

@pytest.fixture
def text_edit():
    return QTextEdit()

@pytest.fixture
def formatador(text_edit):
    return Formatador(text_edit)

def test_toggle_bold(formatador, text_edit):
    text_edit.setText("Texto de teste")
    cursor = text_edit.textCursor()
    cursor.select(QTextCursor.WordUnderCursor)
    text_edit.setTextCursor(cursor)

    formatador.toggle_bold()
    assert text_edit.textCursor().charFormat().fontWeight() == 700  # QFont.Bold

    formatador.toggle_bold()
    assert text_edit.textCursor().charFormat().fontWeight() == 400  # QFont.Normal

def test_toggle_italic(formatador, text_edit):
    text_edit.setText("Texto de teste")
    cursor = text_edit.textCursor()
    cursor.select(QTextCursor.WordUnderCursor)
    text_edit.setTextCursor(cursor)

    formatador.toggle_italic()
    assert text_edit.textCursor().charFormat().fontItalic() is True

    formatador.toggle_italic()
    assert text_edit.textCursor().charFormat().fontItalic() is False

def test_toggle_underline(formatador, text_edit):
    text_edit.setText("Texto de teste")
    cursor = text_edit.textCursor()
    cursor.select(QTextCursor.WordUnderCursor)
    text_edit.setTextCursor(cursor)

    formatador.toggle_underline()
    assert text_edit.textCursor().charFormat().fontUnderline() is True

    formatador.toggle_underline()
    assert text_edit.textCursor().charFormat().fontUnderline() is False

def test_increase_font_size(formatador, text_edit):
    text_edit.setText("Texto de teste")
    cursor = text_edit.textCursor()
    cursor.select(QTextCursor.WordUnderCursor)
    text_edit.setTextCursor(cursor)

    formatador.increase_font_size()
    assert text_edit.textCursor().charFormat().fontPointSize() == 14

    formatador.increase_font_size()
    assert text_edit.textCursor().charFormat().fontPointSize() == 16

def test_decrease_font_size(formatador, text_edit):
    text_edit.setText("Texto de teste")
    cursor = text_edit.textCursor()
    cursor.select(QTextCursor.WordUnderCursor)
    text_edit.setTextCursor(cursor)

    formatador.increase_font_size()  # Primeiro aumenta para evitar tamanho zero
    formatador.decrease_font_size()
    assert text_edit.textCursor().charFormat().fontPointSize() == 12

def test_change_text_color(formatador, text_edit):
    text_edit.setText("Texto de teste")
    cursor = text_edit.textCursor()
    cursor.select(QTextCursor.WordUnderCursor)
    text_edit.setTextCursor(cursor)

    with patch.object(QColorDialog, 'getColor', return_value=QColor("#FF0000")):
        formatador.change_text_color()
    assert text_edit.textCursor().charFormat().foreground().color().name() == "#ff0000"

def test_reset_formatting(formatador, text_edit):
    text_edit.setText("Texto de teste")
    cursor = text_edit.textCursor()
    cursor.select(QTextCursor.Document)
    text_edit.setTextCursor(cursor)

    formatador.toggle_bold()
    formatador.reset_formatting()
    assert text_edit.textCursor().charFormat().fontWeight() == 400  # QFont.Normal