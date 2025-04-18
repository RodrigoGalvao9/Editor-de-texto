from PySide6.QtWidgets import ( QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QTabWidget, QFileDialog, QMessageBox, QMenuBar, QApplication)
from PySide6.QtGui import QFont, QKeySequence, QAction  
from PySide6.QtCore import QTimer
from App.formatador import Formatador
from App.texto_utils import FerramentasTexto
from App.switch_theme import apply_theme
from App.update_utils import check_for_updates
import os

class NotePad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor de Texto")
        self.setGeometry(100, 100, 800, 600)

        self.file_paths = {}  
        self.default_font = QFont("Arial", 12) 
        self.auto_save_enabled = True
        
        self.default_theme = "dark"  

        self.init_ui()
        self.apply_default_theme()
        self.init_auto_save()

    def init_ui(self):
        # Layout principal
        central_widget = QVBoxLayout()
        container = self.centralWidget()
        if not container:
            container = QTabWidget()
            self.setCentralWidget(container)
        container.setLayout(central_widget)

        # Tabs
        self.tab_widget = QTabWidget()
        central_widget.addWidget(self.tab_widget)

        # Barra inferior
        bottom_layout = QHBoxLayout()
        self.status_label = QLabel("Auto-save ativo")
        bottom_layout.addWidget(self.status_label)

        self.toggle_auto_save_button = QPushButton("Desativar Auto-save")
        self.toggle_auto_save_button.clicked.connect(self.toggle_auto_save)
        bottom_layout.addWidget(self.toggle_auto_save_button)

        central_widget.addLayout(bottom_layout)

        # Nova aba inicial
        self.new_tab()

        # Menu
        self.init_menu()

    def init_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menu Arquivo
        file_menu = menu_bar.addMenu("Arquivo")

        new_action = QAction("Nova Aba", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_action)

        open_action = QAction("Abrir", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Salvar", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Salvar Como", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)
        
        save_as_action = QAction("Fechar Aba", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Q"))
        save_as_action.triggered.connect(self.close_tab)
        file_menu.addAction(save_as_action)

        # Menu Editar
        edit_menu = menu_bar.addMenu("Editar")

        undo_action = QAction("Desfazer", self)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Refazer", self)
        redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)

        # Menu Formatar
        format_menu = menu_bar.addMenu("Formatar")

        bold_action = QAction("Negrito", self)
        bold_action.setShortcut(QKeySequence("Ctrl+B"))
        bold_action.triggered.connect(self.toggle_bold)
        format_menu.addAction(bold_action)

        italic_action = QAction("Itálico", self)
        italic_action.setShortcut(QKeySequence("Ctrl+I"))
        italic_action.triggered.connect(self.toggle_italic)
        format_menu.addAction(italic_action)

        underline_action = QAction("Sublinhado", self)
        underline_action.setShortcut(QKeySequence("Ctrl+U"))
        underline_action.triggered.connect(self.toggle_underline)
        format_menu.addAction(underline_action)

        increase_font_action = QAction("Aumentar Fonte", self)
        increase_font_action.setShortcut(QKeySequence("Ctrl+="))
        increase_font_action.triggered.connect(self.increase_font_size)
        format_menu.addAction(increase_font_action)

        decrease_font_action = QAction("Diminuir Fonte", self)
        decrease_font_action.setShortcut(QKeySequence("Ctrl+_"))
        decrease_font_action.triggered.connect(self.decrease_font_size)
        format_menu.addAction(decrease_font_action)

        change_color_action = QAction("Alterar Cor", self)
        change_color_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
        change_color_action.triggered.connect(self.change_text_color)
        format_menu.addAction(change_color_action)

        reset_format_action = QAction("Resetar Formatação", self)
        reset_format_action.setShortcut(QKeySequence("Ctrl+R"))
        reset_format_action.triggered.connect(self.reset_formatting)
        format_menu.addAction(reset_format_action)

        font_menu = format_menu.addMenu("Fonte")

        times_new_roman_action = QAction("Times New Roman", self)
        times_new_roman_action.triggered.connect(lambda: self.change_font("Times New Roman"))
        font_menu.addAction(times_new_roman_action)

        arial_action = QAction("Arial", self)
        arial_action.triggered.connect(lambda: self.change_font("Arial"))
        font_menu.addAction(arial_action)

        courier_action = QAction("Courier New", self)
        courier_action.triggered.connect(lambda: self.change_font("Courier New"))
        font_menu.addAction(courier_action)

        # Menu Ferramentas
        tools_menu = menu_bar.addMenu("Ferramentas")

        spell_check_action = QAction("Verificar Ortografia", self)
        spell_check_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        spell_check_action.triggered.connect(self.check_spelling)
        tools_menu.addAction(spell_check_action)

        search_action = QAction("Pesquisar e Substituir", self)
        search_action.setShortcut(QKeySequence("Ctrl+F"))
        search_action.triggered.connect(self.search_and_replace)
        tools_menu.addAction(search_action)
        
        check_update_action = QAction("Verificar Atualizações", self)
        check_update_action.triggered.connect(self.check_for_updates)
        tools_menu.addAction(check_update_action)

        # Menu Temas
        theme_menu = menu_bar.addMenu("Temas")

        themes = {
            "Claro": "light",
            "Escuro": "dark",
            "Solarizado": "solarized",
            "Midnight": "midnight",
            "Dracula": "dracula"
        }

        for label, theme_key in themes.items():
            action = QAction(label, self)
            action.triggered.connect(lambda checked, theme=theme_key: apply_theme(theme))
            theme_menu.addAction(action)
            
    def apply_default_theme(self):
        apply_theme(self.default_theme)

    # métodos de manipulação de abas(Arquivo)
    def new_tab(self):
        text_edit = QTextEdit()
        text_edit.setFont(self.default_font)
        self.tab_widget.addTab(text_edit, "Nova Aba")
        self.file_paths[text_edit] = None

    def get_current_tab(self):
        current_widget = self.tab_widget.currentWidget()
        return current_widget

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Arquivos de Texto (*.txt);;Todos os Arquivos (*)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    
                if self.tab_widget.count() == 0:
                    self.new_tab()
                
                current_tab = self.get_current_tab()
                current_tab.setPlainText(content)
                self.file_paths[current_tab] = file_path
                self.tab_widget.setTabText(self.tab_widget.currentIndex(), os.path.basename(file_path))
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível abrir o arquivo: {e}")

    def close_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            current_tab = self.tab_widget.widget(current_index)
            file_path = self.file_paths.get(current_tab)
            
            if not file_path:
                self.tab_widget.removeTab(current_index)
                del self.file_paths[current_tab]
                return

            msg_box = QMessageBox(self)  
            msg_box.setWindowTitle("Fechar Aba")
            msg_box.setText("Deseja salvar as alterações antes de fechar?")
            msg_box.setIcon(QMessageBox.Question)

            btn_yes = msg_box.addButton("Sim", QMessageBox.YesRole)
            btn_no = msg_box.addButton("Não", QMessageBox.NoRole)
            btn_cancel = msg_box.addButton("Cancelar", QMessageBox.RejectRole)

            msg_box.exec_()

            if msg_box.clickedButton() == btn_yes:
                self.save_file()
            elif msg_box.clickedButton() == btn_cancel:
                return 

            self.tab_widget.removeTab(current_index)
            del self.file_paths[current_tab]

    def save_file(self):
        current_tab = self.get_current_tab()
        file_path = self.file_paths.get(current_tab)
        if file_path:
            try:
                content = current_tab.toPlainText()
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                self.status_label.setText("Salvo")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível salvar o arquivo: {e}")
        else:
            self.save_as()

    def save_as(self):
        current_tab = self.get_current_tab()
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Como", "", "Arquivos de Texto (*.txt);;Todos os Arquivos (*)")
        if file_path:
            self.file_paths[current_tab] = file_path
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), os.path.basename(file_path))
            self.save_file()


    # métodos de edição(Editar)
    def undo(self):
        current_tab = self.get_current_tab()
        current_tab.undo()

    def redo(self):
        current_tab = self.get_current_tab()
        current_tab.redo()
    
    # métodos de formatação(Formatação)
    def toggle_auto_save(self):
        self.auto_save_enabled = not self.auto_save_enabled
        if self.auto_save_enabled:
            self.status_label.setText("Auto-save ativo")
            self.toggle_auto_save_button.setText("Desativar Auto-save")
        else:
            self.status_label.setText("Auto-save desativado")
            self.toggle_auto_save_button.setText("Ativar Auto-save")

    def init_auto_save(self):
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(60000)  # 60 segundos

    def auto_save(self):
        if not self.auto_save_enabled:
            return

        for i in range(self.tab_widget.count()):
            text_edit = self.tab_widget.widget(i)
            file_path = self.file_paths.get(text_edit)
            if file_path:
                try:
                    content = text_edit.toPlainText()
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao salvar automaticamente: {e}")

    def toggle_bold(self):
        current_tab = self.get_current_tab()
        formatador = Formatador(current_tab)
        formatador.toggle_bold()

    def toggle_italic(self):
        current_tab = self.get_current_tab()
        formatador = Formatador(current_tab)
        formatador.toggle_italic()

    def toggle_underline(self):
        current_tab = self.get_current_tab()
        formatador = Formatador(current_tab)
        formatador.toggle_underline()

    def increase_font_size(self):
        current_tab = self.get_current_tab()
        formatador = Formatador(current_tab)
        formatador.increase_font_size()

    def decrease_font_size(self):
        current_tab = self.get_current_tab()
        formatador = Formatador(current_tab)
        formatador.decrease_font_size()

    def change_text_color(self):
        current_tab = self.get_current_tab()
        formatador = Formatador(current_tab)
        formatador.change_text_color()

    def reset_formatting(self):
        current_tab = self.get_current_tab()
        formatador = Formatador(current_tab)
        formatador.reset_formatting()

    def change_font(self, font_family):
        current_tab = self.get_current_tab()
        formatador = Formatador(current_tab)
        formatador.change_font_family(font_family)

    # Métodos de utilidade de texto(Ferramentas)
    def check_spelling(self):
        current_tab = self.get_current_tab()
        ferramentas = FerramentasTexto(current_tab)
        ferramentas.check_spelling()

    def search_and_replace(self):
        current_tab = self.get_current_tab()
        ferramentas = FerramentasTexto(current_tab)
        ferramentas.search_and_replace()

    def check_for_updates(self):
        try:
            check_for_updates()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao verificar atualizações: {e}")
