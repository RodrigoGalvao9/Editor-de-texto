import pytest
from PySide6.QtWidgets import QApplication, QMenu
from App.paginaInicial import NotePad

@pytest.fixture
def app(qtbot):
    app = NotePad()
    qtbot.addWidget(app)
    return app

def get_menu(app, name: str) -> QMenu:
    """Helper para obter um menu pelo nome"""
    menu_action = next((action for action in app.menuBar().actions() if action.text() == name), None)
    assert menu_action is not None, f"Menu '{name}' não encontrado"
    menu = menu_action.menu()
    assert menu is not None, f"Menu '{name}' não possui submenu"
    return menu

def get_menu_action(app, menu_name: str, action_name: str):
    """Busca uma ação dentro de um menu pelo nome, de forma segura"""
    for action in app.menuBar().actions():
        if action.text() == menu_name:
            menu = action.menu()
            if menu is None:
                raise AssertionError(f"Menu '{menu_name}' não possui submenu")
            for sub_action in menu.actions():
                if sub_action.text() == action_name:
                    return sub_action
            raise AssertionError(f"Ação '{action_name}' não encontrada no menu '{menu_name}'")
    raise AssertionError(f"Menu '{menu_name}' não encontrado")

def test_bold_button_visible_and_enabled(app):
    bold_action = get_menu_action(app, "Formatar", "Negrito")
    assert bold_action.isEnabled(), "A ação 'Negrito' deveria estar habilitada"

def test_spell_check_available(app, qtbot):
    current_tab = app.get_current_tab()
    current_tab.setPlainText("Texto com erro")

    spell_check_action = get_menu_action(app, "Ferramentas", "Verificar Ortografia")
    spell_check_action.trigger()

    assert current_tab.toPlainText() == "Texto com erro", "Texto foi alterado indevidamente"

def test_new_tab_increments_total(app):
    total_before = app.tab_widget.count()
    app.new_tab()
    total_after = app.tab_widget.count()
    assert total_after == total_before + 1, "A nova aba não foi adicionada corretamente"

def test_save_file_creates_valid_file(app, tmp_path):
    current_tab = app.get_current_tab()
    test_content = "Conteúdo de teste"
    current_tab.setPlainText(test_content)

    file_path = tmp_path / "teste.txt"
    app.file_paths[current_tab] = str(file_path)
    app.save_file()

    assert file_path.exists(), "Arquivo não foi criado"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == test_content, "Conteúdo salvo está diferente do esperado"
