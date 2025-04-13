# Bloco de Notas com Formatação e Correção Ortográfica

Este é um editor de texto avançado desenvolvido em Python utilizando a biblioteca `PySide6`. Ele oferece funcionalidades como criação de múltiplas abas, formatação de texto rica, correção ortográfica automatizada e manipulação eficiente de arquivos, proporcionando uma experiência de edição completa e intuitiva.

## Funcionalidades

- **Criação de Abas**: 
  - Permite abrir múltiplas abas para edição de texto.(`Ctrl+N`)
- **Formatação de Texto**
  - Negrito (`Ctrl+B`)
  - Itálico (`Ctrl+I`)
  - Sublinhado (`Ctrl+U`)
  - Aumentar e diminuir tamanho da fonte (`Ctrl+Shift++` / `Ctrl+_`)
  - Alterar cor do texto (`Ctrl+Shift+C`)
  - Resetar formatações (`Ctrl+R`)
- **Correção Ortográfica**:
  - Destaca palavras incorretas no texto com sublinhado e cor vermelha.(`Ctrl+Shift+P`)
- **Manipulação de Arquivos**:
  - Abrir arquivos de texto existentes(`Ctrl+O`).
  - Salvar arquivos no disco.(`Ctrl+Shift+S`)
  - Salvar como um novo arquivo(`Ctrl+S`).
- **Desfazer e Refazer**:
  - Suporte para desfazer (`Ctrl+Z`) e refazer (`Ctrl+Y`) alterações.
- **Pesquisar e Substituir**:
  - Pesquisar por palavras no texto e substituir elas(`Ctrl+F`)
- **Salvamento Automático de Alterações**:
  - Se o arquivo já existir, as alterações serão salvas automaticamente.
  - Botão para ativar ou desativar o salvamento automático.
  - Barra de status indicando se o salvamento automático está ativado ou desativado.
  - Barra de status exibindo mensagens como "Salvando..." ou "Alterações salvas" para informar o status do salvamento.

- **Atalhos de Teclado**:
  - `Ctrl+N`: Nova aba
  - `Ctrl+Q`: Fechar aba atual
  - `Ctrl+O`: Abrir arquivo
  - `Ctrl+S`: Salvar arquivo
  - `Ctrl+Shift+S`: Salvar como
  - `Ctrl+Z`: Desfazer
  - `Ctrl+Y`: Refazer
  - `Ctrl+F`: Pesquisar e substituir
  - `Ctrl+R`: Resetar formatações
  - `Ctrl+B`: Aplicar negrito
  - `Ctrl+I`: Aplicar itálico
  - `Ctrl+U`: Aplicar sublinhado
  - `Ctrl+Shift++`: Aumentar tamanho da fonte
  - `Ctrl+_`: Diminuir tamanho da fonte
  - `Ctrl+Shift+C`: Alterar cor do texto
  - `Ctrl+Shift+P`: Verificar ortografia

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **PySide6**: Biblioteca para criação da interface gráfica.
- **SpellChecker**: Biblioteca para verificação ortográfica.

## Estrutura do Projeto
Bloco-de-notas/ │ ├── App/ │ ├── paginaInicial.py # Arquivo principal do editor de texto │ ├── formatador.py # Classe para formatação de texto │ ├── texto_utils.py # Funções utilitárias, como correção ortográfica ├── README.md # Documentação do projeto └── requirements.txt # Dependências do projeto

## Como Executar

1. Certifique-se de ter o Python instalado (versão 3.8 ou superior).
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o arquivo Principal:
   ```bash
   python App/paginaInicial.py
   ```

## Dependências

As dependências do projeto estão listadas no arquivo requirements.txt. Certifique-se de instalar as seguintes bibliotecas:

- PySide6
- pyspellchecker

## Capturas de Tela

### Editor de Texto com Abas
![Editor com Abas](ainda_vou_colocar)

### Formatação de Texto
![Formatação de Texto](ainda_vou_colocar)

### Correção Ortográfica
![Correção Ortográfica](ainda_vou_colocar)

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests. Para mais detalhes sobre como contribuir, consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença
Este projeto é licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.