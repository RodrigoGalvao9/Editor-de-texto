# region Importações
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os
import formatador  # Importa o módulo de formatação
# endregion

# region Classe NotePad
class NotePad:
    def __init__(self, root):
        # region Inicialização
        self.root = root
        self.root.title("Editor de Texto")
        self.root.geometry("800x600")
        self.file_paths = {}  # Dicionário para armazenar o caminho de arquivos por aba
        self.default_font = font.Font(family="Arial", size=12)  # Fonte padrão
        self.undo_stack = []  # Pilha para desfazer
        self.redo_stack = []  # Pilha para refazer
        self.root.protocol("WM_DELETE_WINDOW", self.close_tab)
        self.root.bind("<Control-z>", lambda event: self.edit_undo())
        self.root.bind("<Control-y>", lambda event: self.edit_redo())
        # endregion

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

        # Menu Formatar
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Formatar", menu=self.format_menu)
        self.format_menu.add_command(label="Negrito", command=self.apply_bold)
        self.format_menu.add_command(label="Itálico", command=self.apply_italic)
        self.format_menu.add_command(label="Sublinhado", command=self.apply_underline)
        # endregion

        # region Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.new_tab()
        # endregion

    # region Métodos
    def new_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="Nova Aba")
        
        text_scroll = tk.Scrollbar(tab)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_area = tk.Text(tab, yscrollcommand=text_scroll.set, wrap="word", undo=True)
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.configure(font=self.default_font)
        
        text_scroll.config(command=text_area.yview)
        self.file_paths[tab] = None
        self.notebook.select(tab)

        # Salvar estado ao modificar o texto
        text_area.bind("<KeyRelease>", lambda event: self.save_state())

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
                content = text_area.get("1.0", tk.END)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
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
        _, text_area = self.get_current_tab()
        formatador.toggle_bold(text_area)

    def apply_italic(self):
        _, text_area = self.get_current_tab()
        formatador.toggle_italic(text_area)

    def apply_underline(self):
        _, text_area = self.get_current_tab()
        formatador.toggle_underline(text_area)
    # endregion
# endregion

if __name__ == "__main__":
    root = tk.Tk()
    app = NotePad(root)
    root.mainloop()