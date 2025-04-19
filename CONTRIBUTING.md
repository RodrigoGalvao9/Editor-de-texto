# Guia de Contribuição

Obrigado por considerar contribuir para este projeto! Abaixo estão as diretrizes para ajudá-lo a começar.

 Guia para mensagens de commits

## Formato da mensagem

Cada mensagem de commit consiste em um **cabeçalho**, um **corpo** e um **rodapé**. 

## Cabeçalho

Tem um formato pré-definido, que inclui um **tipo** e um **título**:

```
<tipo>(<escopo opcional>): <título>

<corpo opcional>

<rodapé opcional>

Exemplos:
fix(integracao-erp): xxxxxxx
improve(app-toolbox): xxxxxxx
docs: instruções de iniciar projeto com docker
```

O **cabeçalho** é obrigatório.

Qualquer linha da mensagem do commit não pode ter mais de 100 caracteres! Assim fica mais fácil para ler no GitHub, Gitlab e outras ferramentas de git.


### Tipo

Deve ser um dos seguintes:

* **build**: alterações que afetam o sistema de build ou dependências externas
* **static**: alterações no conteúdo de arquivos estáticos (dados .json, imagens, etc)
* **ci**: alterações em nossos arquivos e scripts de configuração de CI
* **cd**: alterações em nossos arquivos e scripts de configuração para CD
* **docs**: somente alterações na documentação
* **feat**: um novo recurso
* **fix**: uma correção de bug da aplicação
* **perf**: alteração de código que melhora o desempenho da aplicação e não altera a forma como o usuário utiliza a aplicação
* **refactor**: alteração de código, que não corrige um bug e nem altera a forma como o usuário utiliza a aplicação
* **improve**: alguma alteração de código que melhore o comportamento de um recurso
* **style**: alterações que não afetam o significado do código (espaço em branco, formatação, ponto e vírgula, etc)
* **test**: adicionando testes ausentes ou corrigindo testes existentes
* **revert**: reverter para um commit anterior

### Título

O título contém uma descrição sucinta da mudança:

* use o imperativo, tempo presente: "mudança" não "mudou" nem "muda"
* não capitalize a primeira letra
* sem ponto (.) no final

## Corpo

Um corpo de mensagem de commit mais longo PODE ser fornecido após o título, fornecendo informações contextuais adicionais sobre as alterações no código. 

Configure a mensagem com um wrap de 80 caracteres

Use para explicar "o que" e "porque" foi realizado essa modificação, ao invez de "como".

O corpo DEVE começar depois de uma linha em branco após a descrição.

## Rodapé

Um rodapé PODE ser fornecido depois de uma linha em branco após o corpo. 

## Reverter um commit
Se o commit reverte um commit anterior, ele deve começar por `revert:`, seguido pelo cabeçalho do commit revertido. 

No corpo, ele deve dizer: `Isso reverte o commit <hash> .`, onde o hash é o SHA do commit sendo revertido.

## Estilo de Código

- Use nomes significativos para variáveis e funções.
- Escreva comentários claros e concisos quando necessário.
- Certifique-se de que seu código seja lintado e formatado antes de enviar.

## Pull Requests

1. Faça um fork do repositório e crie um novo branch para sua funcionalidade ou correção de bug.
2. Certifique-se de que seu branch esteja atualizado com o branch `main`.
3. Escreva uma mensagem de commit clara e descritiva.
4. Envie um pull request com uma descrição detalhada das suas alterações.
5. Seja receptivo ao feedback e faça as alterações solicitadas prontamente.

## Testes

- Escreva testes unitários para qualquer nova funcionalidade.
- Certifique-se de que todos os testes existentes passem antes de enviar suas alterações.
- Use um framework de testes consistente (por exemplo, Jest, Pytest, etc.).
- Execute os testes localmente usando o comando:
    ```bash
    pytest -v
    ```
    ou o equivalente para o projeto.

## Notas Adicionais

- Respeite o código de conduta do projeto.
- Se você não tiver certeza sobre uma alteração, sinta-se à vontade para abrir uma issue para discussão.
- Contribuições de todos os tamanhos são bem-vindas, desde a correção de erros de digitação até a implementação de novas funcionalidades.

Obrigado por suas contribuições!
