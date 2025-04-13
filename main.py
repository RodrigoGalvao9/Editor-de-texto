from PySide6.QtWidgets import QApplication
from App.paginaInicial import NotePad
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = NotePad()
    main_window.show()
    sys.exit(app.exec())
