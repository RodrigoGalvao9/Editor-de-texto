import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QAction
from App.paginaInicial import NotePad

@pytest.fixture
def app(qtbot):
    app = NotePad()
    qtbot.addWidget(app)
    return app

def test_botao_negrito(app, qtbot):
    format_menu_action = next((action for action in app.menuBar().actions() if action.text() == "Formatar"), None)
    assert format_menu_action is not None

    format_menu = format_menu_action.menu()
    assert format_menu is not None

    bold_action = next((action for action in format_menu.actions() if action.text() == "Negrito"), None)
    assert bold_action is not None
    assert bold_action.isEnabled()

def test_verificar_ortografia(app, qtbot):
    current_tab = app.get_current_tab()
    current_tab.setPlainText("Texto com erro")

    tools_menu = next((menu for menu in app.menuBar().actions() if menu.text() == "Ferramentas"), None)
    assert tools_menu is not None

    ferramentas_action = next((action for action in tools_menu.menu().actions() if action.text() == "Verificar Ortografia"), None)
    assert ferramentas_action is not None
    ferramentas_action.trigger()

    # Simula a verificação de ortografia (mock necessário para resultados reais)
    assert current_tab.toPlainText() == "Texto com erro"  # Ajuste conforme necessário

def test_nova_aba(app, qtbot):
    initial_count = app.tab_widget.count()
    app.new_tab()
    assert app.tab_widget.count() == initial_count + 1

def test_salvar_arquivo(app, qtbot, tmp_path):
    current_tab = app.get_current_tab()
    current_tab.setPlainText("Conteúdo de teste")

    file_path = tmp_path / "teste.txt"
    app.file_paths[current_tab] = str(file_path)
    app.save_file()

    with open(file_path, "r", encoding="utf-8") as f:
        assert f.read() == "Conteúdo de teste"