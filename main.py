import os
from PySide6.QtWidgets import QApplication
from App.paginaInicial import NotePad
import sys

if __name__ == "__main__":
    dev_mode = os.getenv("DEV_MODE", "false").lower() == "true"

    if dev_mode:
        print("Modo de desenvolvimento ativado. Logs serão exibidos no terminal.")

    app = QApplication(sys.argv)
    main_window = NotePad()
    main_window.show()
    sys.exit(app.exec())
