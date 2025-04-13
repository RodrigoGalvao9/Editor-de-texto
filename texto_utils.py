from spellchecker import SpellChecker
import tkinter as tk
import threading

class FerramentasTexto:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.tag_config("misspelled", foreground="red", underline=True)
        self.text_widget.tag_config("search", background="yellow")
        self.debounce_timer = None
            
    def check_spelling(self, text_widget):
        """Verifica a ortografia com debounce."""
        if self.debounce_timer:
            self.debounce_timer.cancel()

        self.debounce_timer = threading.Timer(0.5, lambda: self._check_spelling(text_widget))
        self.debounce_timer.start()

    def _check_spelling(self, text_widget):
        """Verifica a ortografia do texto no widget fornecido."""
        spell = SpellChecker(language='pt')

        # Remove marcações anteriores
        text_widget.tag_remove("misspelled", "1.0", tk.END)

        text = text_widget.get("1.0", tk.END)
        words = text.split()
        misspelled = spell.unknown(words)
        
        for word in misspelled:
            # Encontrar todas as ocorrências da palavra no texto
            start_pos = "1.0"
            while True:
                start_pos = text_widget.search(word, start_pos, tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word)}c"
                # Marcar as palavras incorretas
                text_widget.tag_add("misspelled", start_pos, end_pos)
                start_pos = end_pos
        
        # Configurar a tag para destacar palavras incorretas
        text_widget.tag_config("misspelled", foreground="red", underline=True)
        
    def search_text(self, query, replace_with=None, case_sensitive=False):
        """Pesquisa e, opcionalmente, substitui texto no widget."""
        self.text_widget.tag_remove("search", "1.0", tk.END)  

        if not query:
            return  

        start_pos = "1.0"
        while True:
            start_pos = self.text_widget.search(
                query, start_pos, tk.END, nocase=(not case_sensitive)
            )
            if not start_pos:
                break

            end_pos = f"{start_pos}+{len(query)}c"
            self.text_widget.tag_add("search", start_pos, end_pos)

            # Substituir texto, se necessário
            if replace_with:
                self.text_widget.delete(start_pos, end_pos)
                self.text_widget.insert(start_pos, replace_with)
                end_pos = f"{start_pos}+{len(replace_with)}c"

            start_pos = end_pos  # Continua a busca após a última ocorrência

        # Configurar a tag para destacar as ocorrências
        self.text_widget.tag_config("search", background="yellow", foreground="black")
        
    def show_search_bar(self):
        """Exibe uma barra de pesquisa para buscar e substituir texto."""
        search_window = tk.Toplevel(self.root)
        search_window.title("Pesquisar")
        search_window.geometry("300x100")
        search_window.transient(self.root)  
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