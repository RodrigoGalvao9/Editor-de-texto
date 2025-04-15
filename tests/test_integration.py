import pytest
from PySide6.QtWidgets import QApplication, QFileDialog
from App.paginaInicial import NotePad

@pytest.fixture
def notepad_app(qtbot):
    app = NotePad()
    qtbot.addWidget(app)
    return app

def test_open_file(notepad_app, qtbot, tmp_path, monkeypatch):
    file_path = tmp_path / "test_open.txt"
    file_content = "Conteúdo de teste"
    file_path.write_text(file_content, encoding="utf-8")

    monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *args, **kwargs: (str(file_path), ""))

    notepad_app.open_file()

    current_tab = notepad_app.get_current_tab()
    assert current_tab.toPlainText() == file_content

def test_save_file(notepad_app, qtbot, tmp_path):
    file_content = "Conteúdo salvo"
    file_path = tmp_path / "test_save.txt"

    current_tab = notepad_app.get_current_tab()
    current_tab.setPlainText(file_content)

    notepad_app.file_paths[current_tab] = str(file_path)

    notepad_app.save_file()

    assert file_path.read_text(encoding="utf-8") == file_content

def test_save_as_file(notepad_app, qtbot, tmp_path, monkeypatch):
    file_content = "Conteúdo salvo como"
    file_path = tmp_path / "test_save_as.txt"

    current_tab = notepad_app.get_current_tab()
    current_tab.setPlainText(file_content)

    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args, **kwargs: (str(file_path), ""))

    notepad_app.save_as()

    assert file_path.read_text(encoding="utf-8") == file_content

def test_new_tab(notepad_app, qtbot):
    initial_tab_count = notepad_app.tab_widget.count()
    notepad_app.new_tab()
    assert notepad_app.tab_widget.count() == initial_tab_count + 1

def test_close_tab(notepad_app, qtbot):
    notepad_app.new_tab()
    initial_tab_count = notepad_app.tab_widget.count()
    notepad_app.tab_widget.removeTab(0)
    assert notepad_app.tab_widget.count() == initial_tab_count - 1
