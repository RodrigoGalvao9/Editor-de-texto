# Bloco de Notas com Formatação e Correção Ortográfica

Este é um editor de texto simples desenvolvido em Python usando a biblioteca `tkinter`. Ele suporta funcionalidades como criação de abas, formatação de texto, correção ortográfica e manipulação de arquivos.

## Funcionalidades

- **Criação de Abas**: Permite abrir múltiplas abas para edição de texto.
- **Formatação de Texto**:
  - Negrito
  - Itálico
  - Sublinhado
  - Aumentar e diminuir tamanho da fonte
  - Alterar cor do texto
  - Resetar formatações
- **Correção Ortográfica**:
  - Destaca palavras incorretas no texto com sublinhado e cor vermelha.
- **Manipulação de Arquivos**:
  - Abrir arquivos de texto existentes.
  - Salvar arquivos no disco.
  - Salvar como um novo arquivo.
- **Desfazer e Refazer**:
  - Suporte para desfazer (`Ctrl+Z`) e refazer (`Ctrl+Y`) alterações.
- **Atalhos de Teclado**:
  - `Ctrl+N`: Nova aba
  - `Ctrl+O`: Abrir arquivo
  - `Ctrl+S`: Salvar arquivo
  - `Ctrl+Z`: Desfazer
  - `Ctrl+Y`: Refazer

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Tkinter**: Biblioteca para criação da interface gráfica.
- **SpellChecker**: Biblioteca para verificação ortográfica.

## Estrutura do Projeto
Bloco-de-notas/ │ ├── paginaInicial.py # Arquivo principal do editor de texto ├── formatador.py # Classe para formatação de texto ├── texto_utils.py # Funções utilitárias, como correção ortográfica ├── README.md # Documentação do projeto └── requirements.txt # Dependências do projeto


## Como Executar

1. Certifique-se de ter o Python instalado (versão 3.8 ou superior).
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
3. Execute o arquivo Principal
    python paginaInicial.py

# Dependências

As dependências do projeto estão listadas no arquivo requirements.txt. Certifique-se de instalar as seguintes bibliotecas:

tkinter (incluso no Python)
pyspellchecker

# Capturas de Tela
Editor de Texto com Abas
<img alt="Editor com Abas" src="ainda vou colocar">
Formatação de Texto
<img alt="Formatação de Texto" src="ainda vou colocar">
Correção Ortográfica
<img alt="Correção Ortográfica" src="ainda vou colocar">


# Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests. Para mais detalhes sobre como contribuir, consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md).

# Licença
Este projeto é licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
