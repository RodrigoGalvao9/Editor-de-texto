import pytest
from PySide6.QtWidgets import QApplication
import sys
import os

# Adiciona o diretório raiz ao path para permitir importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa a classe principal
from App.paginaInicial import NotePad  # Substitua pelo nome real da classe

@pytest.fixture(scope="session", autouse=True)
def app():
    """Cria uma instância do QApplication para os testes."""
    app = QApplication.instance() or QApplication([])
    yield app
    app.quit()

@pytest.fixture
def editor(app, qtbot):
    """Cria uma instância limpa do editor para cada teste."""
    window = NotePad()
    qtbot.addWidget(window)
    yield window
    window.close()