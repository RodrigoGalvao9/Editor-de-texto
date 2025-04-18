import os
from PySide6.QtWidgets import QApplication
from App.paginaInicial import NotePad
import App.update_utils as update_utils
import sys

if __name__ == "__main__":
    dev_mode = os.getenv("DEV_MODE", "false").lower() == "false"

    if dev_mode:
        print("Modo de desenvolvimento ativado. Logs serão exibidos no terminal.")

    update_utils.check_for_updates()
    
    app = QApplication(sys.argv)
    main_window = NotePad()
    main_window.show()
    sys.exit(app.exec())
