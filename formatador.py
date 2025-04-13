from tkinter import font, colorchooser
import tkinter as tk

class Formatador:
    def __init__(self, text_widget):
        """Inicializa o formatador com o widget de texto e configurações padrão."""
        self.text_widget = text_widget
        self.default_font = font.Font(family="Arial", size=12)  # Fonte padrão
        self.text_widget.configure(font=self.default_font)

    def toggle_bold(self):
        """Alterna entre negrito e normal no texto selecionado."""
        try:
            if "bold" in self.text_widget.tag_names("sel.first"):
                self.text_widget.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text_widget.tag_add("bold", "sel.first", "sel.last")
                self.text_widget.tag_configure("bold", font=(self.default_font.actual()["family"], self.default_font.actual()["size"], "bold"))
        except tk.TclError:
            pass  # Nenhum texto selecionado

    def toggle_italic(self):
        """Alterna entre itálico e normal no texto selecionado."""
        try:
            if "italic" in self.text_widget.tag_names("sel.first"):
                self.text_widget.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text_widget.tag_add("italic", "sel.first", "sel.last")
                self.text_widget.tag_configure("italic", font=(self.default_font.actual()["family"], self.default_font.actual()["size"], "italic"))
        except tk.TclError:
            pass  # Nenhum texto selecionado

    def toggle_underline(self):
        """Alterna entre sublinhado e sem sublinhado no texto selecionado."""
        try:
            if "underline" in self.text_widget.tag_names("sel.first"):
                self.text_widget.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.text_widget.tag_add("underline", "sel.first", "sel.last")
                self.text_widget.tag_configure("underline", font=(self.default_font.actual()["family"], self.default_font.actual()["size"], "underline"))
        except tk.TclError:
            pass  # Nenhum texto selecionado

    def increase_font_size(self):
        """Aumenta o tamanho da fonte do texto selecionado."""
        try:
            new_size = self.default_font.actual()["size"] + 2
            self.default_font.configure(size=new_size)
            self.text_widget.configure(font=self.default_font)
        except tk.TclError:
            pass  # Nenhum texto selecionado

    def decrease_font_size(self):
        """Diminui o tamanho da fonte do texto selecionado."""
        try:
            new_size = max(self.default_font.actual()["size"] - 2, 8)  # Limita o tamanho mínimo a 8
            self.default_font.configure(size=new_size)
            self.text_widget.configure(font=self.default_font)
        except tk.TclError:
            pass  # Nenhum texto selecionado

    def change_text_color(self):
        """Troca a cor do texto selecionado."""
        try:
            color = colorchooser.askcolor(title="Escolha uma cor")[1]  # Abre o seletor de cores
            if color:
                self.text_widget.tag_add("color", "sel.first", "sel.last")
                self.text_widget.tag_configure("color", foreground=color)
        except tk.TclError:
            pass  # Nenhum texto selecionado

    def reset_formatting(self):
        """Remove todas as formatações do texto selecionado."""
        try:
            self.text_widget.tag_remove("bold", "sel.first", "sel.last")
            self.text_widget.tag_remove("italic", "sel.first", "sel.last")
            self.text_widget.tag_remove("underline", "sel.first", "sel.last")
            self.text_widget.tag_remove("color", "sel.first", "sel.last")
        except tk.TclError:
            pass  # Nenhum texto selecionado