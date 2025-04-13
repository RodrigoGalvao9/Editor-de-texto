from spellchecker import SpellChecker
import tkinter as tk

def check_spelling(text_widget):
    """Verifica a ortografia do texto no widget fornecido."""
    spell = SpellChecker(language='pt')
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