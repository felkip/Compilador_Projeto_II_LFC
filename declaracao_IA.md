# Declaração de uso de IA generativa

**Projeto:** MiniLang — Compilador-Intérprete (Linguagens Formais e Compiladores, Unidade II)
**Norma:** Portaria CNPq nº 2.664/2026

Nosso grupo **utilizou** ferramentas de IA generativa neste projeto, como copiloto de desenvolvimento.
Abaixo estão a ferramenta, as etapas e a finalidade de cada uso.

## 1. Ferramenta utilizada

| Ferramenta | Versão/modelo | Como foi acessada |
|------------|---------------|-------------------|
| Claude (Anthropic) | Claude Sonnet 5.5 | Interface de chat (claude.ai) |
| Claude (Anthropic) | Claude Opus 5.5 | Interface de chat (claude.ai) |
| ChatGPT (OpenAI) | GPT-6 | Interface de chat (ChatGPT) |


## 2. Etapas e finalidade

| Etapa do projeto | Finalidade específica do uso |
|------------------|------------------------------|
| Planejamento | Ler o enunciado, organizar o cronograma e dividir as tarefas entre os integrantes |
| Estrutura do repositório | Montar o esqueleto de pastas e arquivos (README, `.gitignore`, templates), sem código do compilador |
| Gramática EBNF (item a) | ChatGPT (GPT-6): apoio à revisão documental de `docs/gramatica.md`; esclarecimento da distinção entre alfabeto de caracteres e alfabeto de tokens; correção da descrição da saída do exemplo válido. **Responsável pela revisão humana e aplicação das alterações:** Luís Felipe Carmelo da Silva. Não foram alteradas as produções EBNF. |
| Lexer (item b) | ChatGPT (GPT-6): apoio à implementação de `src/lexer.py`, definição dos tipos de token, tratamento de comentários, diagnósticos com linha/coluna e elaboração dos testes léxicos válidos e inválidos. **Responsável pelas alterações e pela revisão humana nesta etapa:** Luís Felipe Carmelo da Silva. A implementação e os testes devem ser revisados e compreendidos por todos os integrantes do grupo. |
| _Parser e AST_ | _preencher quando usar_ |
| _Interpretador e erros_ | _preencher quando usar_ |
| _Testes_ | _preencher quando usar_ |
| _Relatório_ | _preencher quando usar_ |

As linhas em itálico são para ser completadas ao longo do projeto. Se alguma etapa acabar sem uso de IA,
apaguem a linha ou escrevam "sem uso de IA".

## 3. Como tratamos o que a IA gerou

- Tudo que veio da IA foi lido, testado e é explicável por todos do grupo.
- Os usos, os erros da IA e o que reescrevemos estão registrados no `docs/diario_de_bordo.md`
  e analisados no `docs/relatorio.pdf`.
- Esta declaração não substitui o diário, o relatório nem a defesa oral individual.

## 4. Integrantes

- Luís Felipe Carmelo da Silva
- João Paulo Melo Feitosa
- Tiago Sales Guimarães

Data: 15/11/2026
