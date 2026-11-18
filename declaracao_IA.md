# Declaração de uso de IA generativa

**Projeto:** MiniLang — Compilador-Intérprete (Linguagens Formais e Compiladores, Unidade II)  
**Norma:** Portaria CNPq nº 2.664/2026

Nosso grupo utilizou ferramentas de IA generativa como copiloto durante o desenvolvimento deste projeto. A seguir, são apresentadas as ferramentas utilizadas, as etapas em que foram empregadas e suas respectivas finalidades.

## 1. Ferramentas utilizadas

| Ferramenta | Versão/modelo | Como foi acessada |
|------------|---------------|-------------------|
| Claude (Anthropic) | Claude Sonnet 5.5 | Interface de chat (claude.ai) |
| Claude (Anthropic) | Claude Opus 5.5 | Interface de chat (claude.ai) |
| ChatGPT (OpenAI) | GPT-6 | Interface de chat (ChatGPT) |

## 2. Etapas e finalidade

| Etapa do projeto | Finalidade específica do uso |
|------------------|------------------------------|
| Planejamento | Apoio à leitura do enunciado, organização do cronograma e divisão das tarefas entre os integrantes. |
| Estrutura do repositório | Apoio à organização inicial das pastas e dos arquivos, incluindo README, `.gitignore` e templates, sem geração do código do compilador. |
| Gramática EBNF (item a) | ChatGPT (GPT-6): apoio à revisão documental de `docs/gramatica.md`; esclarecimento da distinção entre alfabeto de caracteres e alfabeto de tokens; correção da descrição da saída do exemplo válido. **Responsável pela revisão humana e aplicação das alterações:** Luís Felipe Carmelo da Silva. Não foram alteradas as produções EBNF. |
| Lexer (item b) | ChatGPT (GPT-6) e Claude Sonnet 5.5: apoio à implementação de `src/lexer.py`, definição dos tipos de token, tratamento de comentários, diagnósticos com linha e coluna, escrita da seção léxica do relatório e elaboração dos testes léxicos válidos e inválidos. **Responsável pelas alterações e pela revisão humana nesta etapa:** Luís Felipe Carmelo da Silva. |
| Parser e AST (itens c e d) | Claude Sonnet 5.5: geração da primeira versão de `src/parser.py` e `src/ast_nodes.py`, redação da seção "Análise sintática" do relatório e elaboração dos testes `test_parser_valido.py`, `test_ast.py` e `test_parser_invalido.py`. **Responsáveis pela revisão humana:** Tiago Sales Guimarães (código) e Luís Felipe Carmelo da Silva (testes e seção do relatório). |
| Interpretador e erros (item e) | A implementação de `src/interpreter.py` e da tabela de símbolos foi realizada por Luís Felipe Carmelo da Silva. O ChatGPT (GPT-6) foi utilizado posteriormente como apoio à revisão dos testes e à análise de aspectos técnicos da etapa. **Responsável pelas alterações e pela revisão humana nesta etapa:** Luís Felipe Carmelo da Silva. |
| Testes (etapas B a E) | ChatGPT (GPT-6): apoio à revisão dos testes do analisador léxico, parser, AST e interpretador, identificação de possíveis casos de borda e sugestões de testes complementares para o lexer. As sugestões foram avaliadas e os testes foram executados para conferir os resultados. |
| Relatório | ChatGPT (GPT-6): apoio à revisão e organização de conteúdos técnicos e à análise dos testes das etapas B a E. A elaboração e organização do relatório final em PDF ficaram sob responsabilidade do trio. |

### Itens (c) e (d): parser e nós da AST

- **Ferramenta e modelo:** Claude Sonnet 5.5 (Anthropic).
- **Etapa:** implementação do parser descendente recursivo (`src/parser.py`) e das classes da AST (`src/ast_nodes.py`).
- **Finalidade:** geração da primeira versão dos dois arquivos a partir da gramática EBNF de `docs/gramatica.md` e dos tipos de token de `src/lexer.py`.
- **Revisão humana:** Tiago Sales Guimarães realizou verificações do código, incluindo a execução das árvores de `1 + 2 * 3` e `(1 + 2) * 3` e o teste de um `for` sem a cláusula de atualização, além de adaptar a implementação à gramática e à lógica do projeto.
- **Atualização do item (c) (17/11/2026):**
  - **Ferramenta e modelo:** Claude Sonnet 5.5 (Anthropic).
  - **Etapa:** testes do parser e da AST e seção "Análise sintática" do relatório.
  - **Finalidade:** elaboração do rascunho da seção, abrangendo técnica LL(1), FIRST/FOLLOW, árvores sintáticas, justificativa formal e comparação com LR, além da elaboração dos testes.
  - **Responsável pela revisão humana e incorporação:** Luís Felipe Carmelo da Silva, que executou os testes e conferiu o conteúdo com o código e a documentação do projeto.

### Revisão dos testes das etapas B a E (18/11/2026)

- **Ferramenta e modelo:** ChatGPT GPT-6 (OpenAI).
- **Etapa:** revisão da suíte de testes do analisador léxico, parser, AST e interpretador.
- **Finalidade:** verificar os testes existentes, identificar possíveis situações de borda e sugerir casos complementares para o analisador léxico.
- **O que foi sugerido:** testes adicionais para reconhecimento de operadores e delimitadores, comentários, números malformados e localização de erros léxicos.
- **Validação:** os testes complementares foram incorporados e executados junto à suíte completa. O resultado foi de 213 testes aprovados e 2 ignorados, referentes aos testes da etapa G que ainda possuem implementação pendente.

As linhas referentes ao planejamento e à estrutura do repositório devem ser mantidas somente se essas atividades realmente contaram com auxílio de IA.

## 3. Como tratamos o que a IA gerou

- As sugestões e os trechos gerados por IA foram considerados como material de apoio, sujeitos à revisão dos integrantes.
- O código e os testes foram conferidos em relação à especificação da MiniLang e ao comportamento esperado do compilador.
- As sugestões que não correspondiam à lógica ou aos requisitos do projeto deveriam ser ajustadas ou descartadas.
- Os usos da IA, as dificuldades encontradas e as decisões de revisão estão registrados no `docs/diario_de_bordo.md` e são analisados no `docs/relatorio.pdf`.
- Esta declaração não substitui o diário de bordo, o relatório nem a defesa oral individual.

## 4. Integrantes

- Luís Felipe Carmelo da Silva
- João Paulo Melo Feitosa
- Tiago Sales Guimarães

**Data da última atualização:** 18/11/2026.
