# region Importações
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os
from formatador import Formatador 
from texto_utils import FerramentasTexto
# endregion

# region Classe Principal
class NotePad:
    def __init__(self, root):
        # region Inicialização
        self.root = root
        self.root.title("Editor de Texto")
        self.root.geometry("800x600")
        self.file_paths = {}  
        self.default_font = font.Font(family="Arial", size=12) 
        self.undo_stack = [] 
        self.redo_stack = []  
        self.root.protocol("WM_DELETE_WINDOW", self.close_tab)
        # endregion
        
        # Atalhos de teclado
        self.root.bind("<Control-z>", lambda event: self.edit_undo())
        self.root.bind("<Control-y>", lambda event: self.edit_redo())
        self.root.bind("<Control-f>", lambda event: self.show_search_bar())
        self.root.bind("<Control-n>", lambda event: self.new_tab())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda event: self.save_as())
        self.root.bind("<Control-q>", lambda event: self.close_tab())
        self.root.bind("<Control-r>", lambda event: self.reset_formatting())
        self.root.bind("<Control-b>", lambda event: self.apply_bold())
        self.root.bind("<Control-i>", lambda event: self.apply_italic())
        self.root.bind("<Control-u>", lambda event: self.apply_underline())
        self.root.bind("<Control-Shift-plus>", lambda event: self.increase_font_size())
        self.root.bind("<Control-underscore>", lambda event: self.decrease_font_size())
        self.root.bind("<Control-Shift-C>", lambda event: self.change_text_color())
        self.root.bind("<Control-Shift-P>", lambda event: self.check_spelling())
        
        # Frame inferior para barra de status e botão
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Barra de status
        self.status_bar = tk.Label(self.bottom_frame, text="Auto-save ativo", anchor="w")
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botão para habilitar/desabilitar auto-save
        self.auto_save_enabled = True 
        self.toggle_auto_save_button = tk.Button(
            self.bottom_frame,
            text="Desativar Auto-save",
            command=self.toggle_auto_save,
            relief=tk.GROOVE,
            width=20
        )
        self.toggle_auto_save_button.pack(side=tk.RIGHT, padx=10)
        
        # Indicador de salvamento
        self.saving_indicator = tk.Label(self.bottom_frame, text="", anchor="e", fg="green")
        self.saving_indicator.pack(side=tk.RIGHT, padx=10)

        # region Menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Menu Arquivo
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.file_menu)
        self.file_menu.add_command(label="Novo", command=self.new_tab)
        self.file_menu.add_command(label="Abrir", command=self.open_file)
        self.file_menu.add_command(label="Salvar", command=self.save_file)
        self.file_menu.add_command(label="Salvar Como", command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Fechar Aba", command=self.close_tab)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=self.root.destroy)

        # Menu Editar
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editar", menu=self.edit_menu)
        self.edit_menu.add_command(label="Resetar Formatação", command=self.reset_formatting)
        self.edit_menu.add_separator()        

       # Menu Formatar
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Formatar", menu=self.format_menu)
        self.format_menu.add_command(label="Negrito", command=self.apply_bold)
        self.format_menu.add_command(label="Itálico", command=self.apply_italic)
        self.format_menu.add_command(label="Sublinhado", command=self.apply_underline)
        self.format_menu.add_separator()
        self.format_menu.add_command(label="Aumentar Fonte", command=self.increase_font_size)
        self.format_menu.add_command(label="Diminuir Fonte", command=self.decrease_font_size)
        self.format_menu.add_command(label="Trocar Cor", command=self.change_text_color)
       
        # Menu Ferramentas
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ferramentas", menu=self.tools_menu)
        self.tools_menu.add_command(label="Verificar Ortografia", command=self.check_spelling)
        self.tools_menu.add_command(label="Buscar Texto", command=lambda: self.search_text(case_sensitive=False))
        self.tools_menu.add_command(label="Buscar Texto (Sensível a Maiúsculas)", command=lambda: self.search_text(case_sensitive=True))
        self.tools_menu.add_separator()
        # endregion

        # region Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.new_tab()
        
        # Inicia o auto-save
        self.auto_save()
        # endregion

    # region Métodos
    def auto_save(self):
        """Salva automaticamente o conteúdo do texto em intervalos regulares."""
        if not self.auto_save_enabled:
            return  # Não faz nada se o auto-save estiver desativado
    
        # Exibe o indicador de salvamento, garantindo que ele esteja visível
        if self.saving_indicator.winfo_ismapped():
            self.saving_indicator.config(text="Salvando...", fg="blue")
            self.root.update_idletasks() 
        else:
            print("Indicador de salvamento não está visível.")
    
        for tab in self.notebook.tabs():
            current_tab = self.notebook.nametowidget(tab)
            text_area = current_tab.winfo_children()[1]
            file_path = self.file_paths.get(current_tab)
    
            # Salva apenas se o arquivo já tiver um caminho associado
            if file_path:
                try:
                    content = text_area.get("1.0", tk.END).strip()
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar automaticamente: {e}")
    
        # Atualiza o indicador de salvamento após o salvamento
        self.saving_indicator.config(text="Salvo", fg="green")
        self.root.update_idletasks()  # Atualiza a interface imediatamente
    
        # Reagendar o auto-save para daqui a 60 segundos
        self.root.after(60000, self.auto_save)
    
    def toggle_auto_save(self):
        """Habilita ou desabilita o auto-save."""
        self.auto_save_enabled = not self.auto_save_enabled
    
        if self.auto_save_enabled:
            self.status_bar.config(text="Auto-save ativo")
            self.toggle_auto_save_button.config(text="Desativar Auto-save")
            self.auto_save()  # Reativa o auto-save
        else:
            self.status_bar.config(text="Auto-save desativado")
            self.toggle_auto_save_button.config(text="Ativar Auto-save")
    
    def new_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="Nova Aba")
        
        text_scroll = tk.Scrollbar(tab)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_area = tk.Text(tab, yscrollcommand=text_scroll.set, wrap="word", undo=True)
        text_area.pack(fill=tk.BOTH, expand=True)
        
        text_scroll.config(command=text_area.yview)
        self.file_paths[tab] = None
        self.notebook.select(tab)

        # Criar um formatador para o widget de texto
        formatador = Formatador(text_area)
        tab.formatador = formatador  # Armazena o formatador na aba

        # Criar ferramentas de texto para o widget de texto
        ferramentas = FerramentasTexto(text_area)
        tab.ferramentas = ferramentas  # Armazena as ferramentas na aba

        # Salvar estado ao modificar o texto
        text_area.bind("<KeyRelease>", lambda event: self.save_state())

        # Verificar ortografia automaticamente ao modificar o texto
        text_area.bind("<KeyRelease>", lambda event: ferramentas.check_spelling(text_area))
        
    def get_current_tab(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        text_area = current_tab.winfo_children()[1]
        return current_tab, text_area

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Arquivo de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.new_tab()
                current_tab, text_area = self.get_current_tab()
                text_area.delete("1.0", tk.END)
                text_area.insert("1.0", content)
                self.file_paths[current_tab] = file_path
                self.notebook.tab(current_tab, text=os.path.basename(file_path))
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")

    def save_file(self):
        current_tab, text_area = self.get_current_tab()
        file_path = self.file_paths[current_tab]
        if file_path:
            try:
                self.saving_indicator.config(text="Salvando...", fg="blue")
                self.root.update_idletasks() 
                
                content = text_area.get("1.0", tk.END)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
    
                self.saving_indicator.config(text="Salvo", fg="green")
                return True
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")
                return False
        else:
            return self.save_as()

    def save_as(self):
        current_tab, _ = self.get_current_tab()
        file_path = filedialog.asksaveasfilename(
            filetypes=[("Arquivo de texto", "*.txt"), ("Todos os arquivos", "*.*")],
            defaultextension=".txt"
        )
        if file_path:
            self.file_paths[current_tab] = file_path
            self.notebook.tab(current_tab, text=os.path.basename(file_path))
            return self.save_file()
        return False

    def auto_save(self):
        """Salva automaticamente o conteúdo do texto em intervalos regulares."""
        for tab in self.notebook.tabs():
            current_tab = self.notebook.nametowidget(tab)
            text_area = current_tab.winfo_children()[1]
            file_path = self.file_paths.get(current_tab)

            # Salva apenas se o arquivo já tiver um caminho associado
            if file_path:
                try:
                    content = text_area.get("1.0", tk.END).strip()
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar automaticamente: {e}")

        # Reagendar o auto-save para daqui a 60 segundos
        self.root.after(60000, self.auto_save)
    
    def close_tab(self):
        current_tab, text_area = self.get_current_tab()
        content = text_area.get("1.0", tk.END).strip()
        file_path = self.file_paths[current_tab]
        if content:
            if file_path:
                with open(file_path, "r", encoding="utf-8") as file:
                    saved_content = file.read()
                if content != saved_content:
                    response = messagebox.askyesnocancel(
                        "Salvar Alterações",
                        "Deseja salvar as alterações antes de fechar?"
                    )
                    if response:
                        if not self.save_file():
                            return
                    elif response is None:
                        return
            else:
                response = messagebox.askyesnocancel(
                    "Salvar Alterações",
                    "Deseja salvar as alterações antes de fechar?"
                )
                if response:
                    if not self.save_as():
                        return
                elif response is None:
                    return
        self.file_paths.pop(current_tab, None)
        self.notebook.forget(current_tab)

    def save_state(self):
        """Salva o estado atual na pilha de desfazer."""
        current_tab, text_area = self.get_current_tab()
        content = text_area.get("1.0", tk.END)
        self.undo_stack.append(content)
        self.redo_stack.clear()  # Limpa a pilha de refazer ao salvar um novo estado

    def edit_undo(self):
        """Desfaz a última operação."""
        if not self.undo_stack:
            messagebox.showinfo("Desfazer", "Nada para desfazer.")
            return
        
        current_tab, text_area = self.get_current_tab()
        current_content = text_area.get("1.0", tk.END)
        self.redo_stack.append(current_content)  # Salva o estado atual na pilha de refazer
        last_state = self.undo_stack.pop()  # Recupera o último estado
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", last_state)

    def edit_redo(self):
        """Refaz a última operação desfeita."""
        if not self.redo_stack:
            messagebox.showinfo("Refazer", "Nada para refazer.")
            return
        
        current_tab, text_area = self.get_current_tab()
        current_content = text_area.get("1.0", tk.END)
        self.undo_stack.append(current_content)  # Salva o estado atual na pilha de desfazer
        next_state = self.redo_stack.pop()  # Recupera o próximo estado
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", next_state)

    # Métodos para aplicar formatações
    def apply_bold(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        current_tab.formatador.toggle_bold()

    def apply_italic(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        current_tab.formatador.toggle_italic()

    def apply_underline(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        current_tab.formatador.toggle_underline()

    def increase_font_size(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        current_tab.formatador.increase_font_size()

    def decrease_font_size(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        current_tab.formatador.decrease_font_size()

    def change_text_color(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        current_tab.formatador.change_text_color()

    def reset_formatting(self):
        """Remove todas as formatações do texto selecionado ou de todo o texto."""
        current_tab, text_area = self.get_current_tab()

        try:
            # Tenta obter o texto selecionado
            start = text_area.index("sel.first")
            end = text_area.index("sel.last")
        except tk.TclError:
            # Se não houver seleção, aplica ao texto inteiro
            start = "1.0"
            end = tk.END

        # Remove todas as tags de formatação
        for tag in text_area.tag_names():
            text_area.tag_remove(tag, start, end)
    
    # Métodos de utilidades de texto
    def check_spelling(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        text_area = current_tab.winfo_children()[1]
        tools = FerramentasTexto(text_area)
        tools.check_spelling(text_area)
    
    def search_text(self, query=None, replace_with=None, case_sensitive=False):
        """Pesquisa e, opcionalmente, substitui texto no widget."""
        current_tab, text_area = self.get_current_tab()

        # Se nenhuma consulta for fornecida, use o texto selecionado
        if not query:
            try:
                query = text_area.selection_get()
            except tk.TclError:
                messagebox.showinfo("Buscar Texto", "Nenhum texto selecionado ou fornecido.")
                return

        ferramentas = FerramentasTexto(text_area)
        ferramentas.search_text(query=query, replace_with=replace_with, case_sensitive=case_sensitive)

    def show_search_bar(self):
        """Exibe uma barra de pesquisa para buscar e substituir texto."""
        search_window = tk.Toplevel(self.root)
        search_window.title("Pesquisar")
        search_window.geometry("300x100")
        search_window.transient(self.root)  # Define como janela filha
        search_window.resizable(False, False)

        # Campo para o texto a ser pesquisado
        tk.Label(search_window, text="Pesquisar:").grid(row=0, column=0, padx=5, pady=5)
        search_entry = tk.Entry(search_window, width=25)
        search_entry.grid(row=0, column=1, padx=5, pady=5)

        # Campo para o texto de substituição
        tk.Label(search_window, text="Substituir por:").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = tk.Entry(search_window, width=25)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botão para executar a pesquisa
        tk.Button(
            search_window,
            text="Pesquisar",
            command=lambda: self.search_text(
                query=search_entry.get(),
                replace_with=None,
                case_sensitive=False
            ),
        ).grid(row=2, column=0, padx=5, pady=5)

        # Botão para substituir o texto
        tk.Button(
            search_window,
            text="Substituir",
            command=lambda: self.search_text(
                query=search_entry.get(),
                replace_with=replace_entry.get(),
                case_sensitive=False
            ),
        ).grid(row=2, column=1, padx=5, pady=5)

        # Atalho para fechar a barra de pesquisa
        search_window.bind("<Escape>", lambda event: search_window.destroy())

    # endregion
# endregion

if __name__ == "__main__":
    root = tk.Tk()
    app = NotePad(root)
    root.mainloop()