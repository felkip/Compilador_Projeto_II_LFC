# Diário de bordo

> O enunciado cita um "template da seção Diário de bordo" que não veio no PDF. Peça o template oficial à professora e adapte este arquivo se for diferente.

## Semana 1 — 16/11 a 22/11

- **Fase:** gramática (item a)
- **Quem fez o quê:**
  - João Paulo: alfabeto, gramática EBNF, tabela de precedência/associatividade, 5 exemplos comentados (`docs/gramatica.md`), `exemplos/programa_valido.ml` e `exemplos/programa_invalido.ml`.
- **Decisões tomadas e por quê:**
  - Precedência codificada por níveis de não terminais (`igualdade` → `comparacao` → `termo` → `fator` → `unario` → `primario`) e associatividade à esquerda com repetição `{ }`, para evitar recursão à esquerda, que um parser descendente recursivo não suporta.
  - Operadores relacionais não associativos (`a < b < c` é erro sintático), porque `(a < b) < c` compararia `bool` com `int`.
  - Inclusão de comentário de bloco `/* ... */`: o item (b) exige testar "comentário não fechado", e um comentário `//` sempre termina no fim da linha. *Decisão a validar com o grupo, pois afeta o lexer.*
- **Dificuldades:** separar o que é restrição sintática (gramática) do que é restrição semântica (tipos, variável definida, divisão por zero), que uma gramática livre de contexto não consegue expressar.
- **Uso de IA:**
  - Ferramenta: Claude Opus 5.5 (Anthropic).
  - Prompt resumido: gerar a definição formal da MiniLang a partir do enunciado (alfabeto, EBNF com precedência explícita, while/for e 5 exemplos justificados).
  - O que veio: gramática EBNF, tabela de precedência, restrições semânticas S1–S6 e os 5 exemplos.
  - O que estava errado: a justificativa do exemplo léxico citava estados do autômato (`q0`, `NUM_ERR`) que ainda não estavam definidos no documento, porque pertencem ao item (b).
  - O que foi reescrito e por quê: a justificativa passou a se apoiar só no alfabeto Σ e nas expressões regulares de `INT` e `ID` (conceito: a análise léxica é definida por linguagens regulares; o autômato é a implementação, apresentada no item b).
- **Commits da semana:** item (a): gramática e exemplos.
- **Próximos passos:** validação da gramática pelo grupo; item (d): `src/ast_nodes.py`.

## Semana 2

(repetir o modelo)
