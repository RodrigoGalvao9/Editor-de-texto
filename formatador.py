from tkinter import font
import tkinter as tk

def toggle_bold(text_widget):
    """Alterna entre negrito e normal no texto selecionado."""
    try:
        # Verifica se a tag 'bold' já está aplicada
        if "bold" in text_widget.tag_names("sel.first"):
            text_widget.tag_remove("bold", "sel.first", "sel.last")
        else:
            text_widget.tag_add("bold", "sel.first", "sel.last")
            text_widget.tag_configure("bold", font=("Arial", 12, "bold"))
    except tk.TclError:
        pass  # Nenhum texto selecionado

def toggle_italic(text_widget):
    """Alterna entre itálico e normal no texto selecionado."""
    try:
        # Verifica se a tag 'italic' já está aplicada
        if "italic" in text_widget.tag_names("sel.first"):
            text_widget.tag_remove("italic", "sel.first", "sel.last")
        else:
            text_widget.tag_add("italic", "sel.first", "sel.last")
            text_widget.tag_configure("italic", font=("Arial", 12, "italic"))
    except tk.TclError:
        pass  # Nenhum texto selecionado

def toggle_underline(text_widget):
    """Alterna entre sublinhado e sem sublinhado no texto selecionado."""
    try:
        # Verifica se a tag 'underline' já está aplicada
        if "underline" in text_widget.tag_names("sel.first"):
            text_widget.tag_remove("underline", "sel.first", "sel.last")
        else:
            text_widget.tag_add("underline", "sel.first", "sel.last")
            text_widget.tag_configure("underline", font=("Arial", 12, "underline"))
    except tk.TclError:
        pass  # Nenhum texto selecionado