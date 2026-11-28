# MiniLang — Compilador-Intérprete

Projeto da Unidade II de **Linguagens Formais e Compiladores** (Ciência da Computação, UNIT).

**Docente:** Layse Santos Souza.

## Integrantes e contribuições

| Integrante | Principais contribuições |
|---|---|
| Luís Felipe Carmelo da Silva | Revisão e correções da etapa A; desenvolvimento da etapa B (analisador léxico, documentação das expressões regulares e do AFD, testes léxicos); revisão da etapa C, incorporação dos testes do parser e da seção "Análise sintática" do relatório; implementação da etapa E (interpretador); elaboração do relatório em PDF; revisão dos testes das etapas B a E; desenvolvimento e ampliação da suíte de testes da etapa G, com casos de borda para `while` e `for`, limite de iterações, laços infinitos e laços aninhados. |
| Tiago Sales Guimarães | Implementação do parser descendente recursivo (etapa C) e da primeira versão dos nós da AST em `src/ast_nodes.py` (etapa D); catálogo de erros léxicos, sintáticos e semânticos, programas de demonstração em `exemplos/erros/` e testes correspondentes (etapa F). |
| João Paulo Melo Feitosa | Etapa A: alfabeto, gramática EBNF, tabela de precedência e associatividade, 5 exemplos comentados (`docs/gramatica.md`) e programas `exemplos/programa_valido.ml` e `exemplos/programa_invalido.ml`. Etapa D: revisão de `src/ast_nodes.py`, testes da AST (`tests/validos/test_ast.py`), diagrama da AST (`docs/figuras/ast_programa_com_laco.png`) e seção "Árvore sintática abstrata" do relatório. |

## Contribuições individuais registradas

- **Luís Felipe Carmelo da Silva:** realizou a revisão e as correções da letra A, incluindo ajustes na documentação da gramática e nos exemplos. Desenvolveu a letra B (analisador léxico, testes e documentação) e incorporou o reconhecimento de comentários de bloco (`/* ... */`) como extensão da MiniLang, aceita pelo grupo para possibilitar o teste de comentários não fechados. Na letra C, revisou e incorporou os testes do parser e a seção "Análise sintática" do relatório, redigidos com apoio de IA. Também ficou responsável pela implementação da letra E, correspondente ao interpretador, pela elaboração do relatório final em PDF, pela revisão dos testes das etapas B a E e pelo desenvolvimento dos testes da etapa G. Na etapa G, acrescentou testes para `while` que não executa, executa uma vez e executa N vezes; para `for` com atualização da variável de controle; e para o limite de execução de laços infinitos, incluindo `while`, `for`, limite exato e laços aninhados.
- **Tiago Sales Guimarães:** implementou o parser descendente recursivo e a primeira versão dos nós da AST (letras C e D), adaptando a versão gerada com apoio de IA à gramática e à lógica do projeto. Na letra F, montou o catálogo de erros, os programas de demonstração em `exemplos/erros/` e os testes que os executam, conferindo cada mensagem com a execução real.
- **João Paulo Melo Feitosa:** elaborou a letra A (alfabeto, gramática EBNF, precedência e associatividade, exemplos comentados e programas de exemplo). Na letra D, revisou `src/ast_nodes.py` (removendo uma condição redundante em `arvore_texto`), escreveu os 18 testes da AST, gerou o diagrama da AST de um programa com laço e redigiu a seção da AST do relatório.

## Ferramentas utilizadas

- **Python:** linguagem utilizada na implementação do projeto.
- **pytest:** execução dos testes automatizados.
- **Git e GitHub:** controle de versão e hospedagem do repositório.
- **ChatGPT (GPT-6):** apoio à revisão da gramática, análise da implementação do lexer, elaboração e revisão de testes e documentação.
- **Claude (Sonnet 5.5):** apoio à implementação e revisão do parser e da AST, à redação da seção de análise sintática do relatório, aos testes do parser e ao catálogo de erros.
- **Claude (Opus 5.5):** apoio à elaboração da gramática e dos exemplos (etapa A) e, na etapa D, à revisão dos nós da AST, aos testes da AST, ao diagrama e à seção da AST no relatório.

As sugestões geradas pelas ferramentas de IA foram revisadas, compreendidas e verificadas pelos integrantes do grupo. Os usos específicos estão registrados em [`declaracao_IA.md`](declaracao_IA.md) e [`docs/diario_de_bordo.md`](docs/diario_de_bordo.md), e analisados no relatório final.

## Pré-requisitos

- Python 3.10 ou superior.
- Git, para clonar o repositório.

## Como executar

### 1. Clonar e entrar na pasta

```bash
git clone https://github.com/felkip/Compilador_Projeto_II_LFC.git
cd Compilador_Projeto_II_LFC
```

### 2. Criar um ambiente virtual (opcional, mas recomendado)

O ambiente virtual mantém as dependências do projeto isoladas de outras instalações Python.

Windows:

```bash
py -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Após a ativação, o terminal exibirá `(.venv)` no início da linha de comando.

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Executar um programa MiniLang

```bash
python -m src.interpreter exemplos/programa_valido.ml
python -m src.interpreter exemplos/programa_invalido.ml
```

O interpretador também permite definir um limite de iterações para os laços:

```bash
python -m src.interpreter exemplos/programa_valido.ml --max-iteracoes 1000
```

### 5. Executar os testes automatizados

```bash
python -m pytest -v
```

O parâmetro `-v` exibe individualmente os testes executados e seus resultados.

### 6. Encerrar o ambiente virtual

```bash
deactivate
```

## Estrutura do projeto

```text
docs/        relatório (PDF), gramática, diário de bordo, catálogo de erros e figuras
exemplos/    programas .ml de demonstração (inclui exemplos/erros/)
src/         lexer, parser, AST e interpretador
tests/       testes válidos e inválidos
```

## Vídeo de apresentação

[`docs/apresentacao.mp4`](docs/apresentacao.mp4]
