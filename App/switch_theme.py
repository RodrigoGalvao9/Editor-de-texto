# App/style/theme.py

from PySide6.QtWidgets import QApplication
from pathlib import Path

def apply_theme(theme: str):
    app = QApplication.instance()
    if not app:
        print("Erro: Nenhuma instância de QApplication foi encontrada.")
        return

    # Caminho do arquivo de estilo baseado no nome do tema
    style_path = Path(f"App/style/{theme}.qss")

    if style_path.exists():
        stylesheet = style_path.read_text()
        app.setStyleSheet(stylesheet)
        print(f"Tema aplicado: {theme}")
    else:
        print(f"Arquivo de tema '{theme}.qss' não encontrado. Nenhuma modificação foi feita.")
