import pytest
from unittest.mock import patch
from PySide6.QtGui import QTextCursor, QColor
from PySide6.QtWidgets import QTextEdit, QColorDialog
from App.formatador import Formatador

@pytest.fixture
def text_edit():
    return QTextEdit()

@pytest.fixture
def formatter(text_edit):
    return Formatador(text_edit)

def select_word(text_edit):
    cursor = text_edit.textCursor()
    cursor.select(QTextCursor.WordUnderCursor)
    text_edit.setTextCursor(cursor)

def test_toggle_bold(formatter, text_edit):
    text_edit.setText("Texto de teste")
    select_word(text_edit)

    formatter.toggle_bold()
    assert text_edit.textCursor().charFormat().fontWeight() == 700  

    formatter.toggle_bold()
    assert text_edit.textCursor().charFormat().fontWeight() == 400  

def test_toggle_italic(formatter, text_edit):
    text_edit.setText("Texto de teste")
    select_word(text_edit)

    formatter.toggle_italic()
    assert text_edit.textCursor().charFormat().fontItalic() is True

    formatter.toggle_italic()
    assert text_edit.textCursor().charFormat().fontItalic() is False

def test_toggle_underline(formatter, text_edit):
    text_edit.setText("Texto de teste")
    select_word(text_edit)

    formatter.toggle_underline()
    assert text_edit.textCursor().charFormat().fontUnderline() is True

    formatter.toggle_underline()
    assert text_edit.textCursor().charFormat().fontUnderline() is False

def test_increase_font_size(formatter, text_edit):
    text_edit.setText("Texto de teste")
    select_word(text_edit)

    formatter.increase_font_size()
    assert text_edit.textCursor().charFormat().fontPointSize() == 14

    formatter.increase_font_size()
    assert text_edit.textCursor().charFormat().fontPointSize() == 16

def test_decrease_font_size(formatter, text_edit):
    text_edit.setText("Texto de teste")
    select_word(text_edit)

    formatter.increase_font_size() 
    formatter.decrease_font_size()  
    assert text_edit.textCursor().charFormat().fontPointSize() == 12

def test_change_text_color(formatter, text_edit):
    text_edit.setText("Texto de teste")
    select_word(text_edit)

    with patch.object(QColorDialog, 'getColor', return_value=QColor("#FF0000")):
        formatter.change_text_color()
    
    color = text_edit.textCursor().charFormat().foreground().color().name()
    assert color == "#ff0000"

def test_reset_formatting(formatter, text_edit):
    text_edit.setText("Texto de teste")
    cursor = text_edit.textCursor()
    cursor.select(QTextCursor.Document)
    text_edit.setTextCursor(cursor)

    formatter.toggle_bold()
    formatter.toggle_italic()
    formatter.increase_font_size()
    formatter.reset_formatting()

    char_format = text_edit.textCursor().charFormat()
    char_format.setFontPointSize(12)

    assert char_format.fontWeight() == 400
    assert char_format.fontItalic() is False
    assert char_format.fontPointSize() == 12

def test_font_change(formatter, text_edit):
    text_edit.setText("Texto de teste")
    select_word(text_edit)  

    font_families = ["Arial", "Times New Roman", "Courier New"]

    for family in font_families:
        formatter.change_font_family(family)
        cursor = text_edit.textCursor()
        current_family = cursor.charFormat().fontFamilies()
        assert current_family[0] == family, f"Esperado: {family}, mas foi: {current_family}"

    