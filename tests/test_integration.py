import pytest
from PySide6.QtWidgets import QApplication
from App.paginaInicial import NotePad

@pytest.fixture
def app(qtbot):
    app = NotePad()
    qtbot.addWidget(app)
    return app

def test_abrir_arquivo(app, qtbot, tmp_path):
    # Cria um arquivo temporário
    file_path = tmp_path / "teste_abrir.txt"
    file_path.write_text("Conteúdo de teste", encoding="utf-8")

    # Mock do QFileDialog para retornar o caminho do arquivo
    def mock_get_open_file_name(*args, **kwargs):
        return str(file_path), ""

    app.open_file = lambda: mock_get_open_file_name()
    app.open_file()

    current_tab = app.get_current_tab()
    current_tab.setPlainText(file_path.read_text(encoding="utf-8"))
    assert current_tab.toPlainText() == "Conteúdo de teste"

def test_salvar_arquivo(app, qtbot, tmp_path):
    current_tab = app.get_current_tab()
    current_tab.setPlainText("Conteúdo salvo")

    file_path = tmp_path / "teste_salvar.txt"
    app.file_paths[current_tab] = str(file_path)
    app.save_file()

    assert file_path.read_text(encoding="utf-8") == "Conteúdo salvo"

def test_salvar_como(app, qtbot, tmp_path):
    current_tab = app.get_current_tab()
    current_tab.setPlainText("Conteúdo salvo como")

    file_path = tmp_path / "teste_salvar_como.txt"

    # Mock do QFileDialog para retornar o caminho do arquivo
    def mock_get_save_file_name(*args, **kwargs):
        return str(file_path), ""

    app.save_as = lambda: mock_get_save_file_name()
    app.save_as()

    file_path.write_text(current_tab.toPlainText(), encoding="utf-8")
    assert file_path.read_text(encoding="utf-8") == "Conteúdo salvo como"

def test_nova_aba(app, qtbot):
    initial_count = app.tab_widget.count()
    app.new_tab()
    assert app.tab_widget.count() == initial_count + 1

def test_fechar_aba(app, qtbot):
    app.new_tab()
    initial_count = app.tab_widget.count()
    app.tab_widget.removeTab(0)
    assert app.tab_widget.count() == initial_count - 1