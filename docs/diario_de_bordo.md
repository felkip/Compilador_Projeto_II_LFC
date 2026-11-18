# Diário de bordo

> O enunciado cita um "template da seção Diário de bordo" que não veio no PDF. Peça o template oficial à professora e adapte este arquivo se for diferente.

## Semana 1 — 16/11 a 22/11

- **Fase:** gramática (item a)
- **Período:** em andamento. Registro atualizado até 16/11.
- **Quem fez o quê:**
  - **João Paulo:** elaboração inicial do alfabeto, da gramática EBNF, da tabela de precedência/associatividade e dos 5 exemplos comentados em `docs/gramatica.md`, além dos arquivos `exemplos/programa_valido.ml` e `exemplos/programa_invalido.ml`.
  - **Luís Felipe Carmelo da Silva:** revisão e correções da etapa A, com ajustes na documentação, na definição formal da linguagem e na especificação da gramática.
- **Decisões tomadas e por quê:**
  - Precedência codificada por níveis de não terminais (`igualdade` → `comparacao` → `termo` → `fator` → `unario` → `primario`) e associatividade à esquerda com repetição `{ }`, para evitar recursão à esquerda, que um parser descendente recursivo não suporta.
  - Operadores relacionais não associativos (`a < b < c` é erro sintático), porque `(a < b) < c` compararia `bool` com `int`.
  - Inclusão de comentário de bloco `/* ... */` como extensão da linguagem, aprovada pelo grupo. Essa decisão também permite testar comentários não fechados no lexer. O comentário de linha `//` continua sendo o formato previsto originalmente.
- **Dificuldades:** separar o que é restrição sintática (gramática) do que é restrição semântica (tipos, variável definida, divisão por zero), que uma gramática livre de contexto não consegue expressar.
- **Uso de IA:**
  - **Ferramentas:** Claude Opus 5.5 e Claude Sonnet 5.5 (Anthropic); ChatGPT GPT-6 (OpenAI).
  - **Prompts resumidos:** geração e revisão da definição formal da MiniLang; análise da gramática EBNF e da precedência dos operadores; revisão da documentação; apoio à implementação e análise do lexer; sugestões de testes e verificações de consistência com o enunciado.
  - **O que veio:** sugestões para a gramática EBNF, tabela de precedência, restrições semânticas, exemplos de programas, documentação da linguagem, implementação do analisador léxico e sugestões de testes.
  - **O que precisou ser conferido ou corrigido:** algumas justificativas misturavam conceitos da análise léxica com detalhes de implementação do autômato, como estados (`q0`, `NUM_ERR`) que pertencem ao item (b), e não à definição inicial da gramática. Também foi necessário conferir as sugestões com o enunciado e com as decisões tomadas pelo grupo.
  - **O que foi reescrito e por quê:** as justificativas da etapa A foram ajustadas para se apoiarem no alfabeto Σ e nas expressões regulares de `INT` e `ID`. As sugestões relacionadas ao lexer foram revisadas para manter a coerência com a implementação e com os testes do projeto.
  - **Validação humana:** as respostas das ferramentas foram analisadas e adaptadas antes de serem incorporadas ao projeto. A decisão final sobre o conteúdo e as alterações permaneceu com os integrantes do grupo.
- **Commits da semana:** item (a): elaboração, revisão e correções da gramática e dos exemplos. Item (b): implementação do analisador léxico em `src/lexer.py`, documentação das expressões regulares e do autômato, além da criação da seção de análise léxica no relatorio.pdf e execução dos testes léxicos válidos e inválidos. Os identificadores e as mensagens dos commits devem ser acrescentados conforme o histórico real do Git.
- **Próximos passos:** iniciar o item (c), referente ao analisador sintático, e avançar na integração com a construção da AST (item d). Também será necessário revisar a integração entre as etapas já desenvolvidas e manter os testes atualizados.
- **Resultado parcial:** as etapas (a) e (b) foram desenvolvidas, revisadas e documentadas. O analisador léxico está implementado e seus testes estão passando. As próximas atividades serão direcionadas às etapas seguintes do compilador.
  
Observação: como a semana vai até 22/11, este registro deve ser complementado conforme novas atividades forem realizadas. Não registrar como concluídas tarefas que ainda estão previstas.

///////////////////////////////////////////////////////////////////////////////
- **Fase:** parser (item c) e AST (item d)
- **Quem fez o quê:** [Tiago Sales ]
- **Decisões tomadas e por quê:**
  - Parser descendente recursivo LL(1): uma função por não terminal; a
    precedência vem da cadeia de chamadas e as repetições `{ }` viram `while`
    (associatividade à esquerda, sem recursão à esquerda).
  - Relacionais não associativos: `_comparacao` usa `if` e não `while`.
  - `for` exige as três cláusulas: cada `;` e cada atribuição é obrigatório.
  - O parser para no primeiro erro sintático (ParseError com linha e coluna).
- **Uso de IA:** Claude Sonnet 5.5 gerou a primeira versão de `parser.py` e
  `ast_nodes.py`. [O que foi conferido: árvores de `1 + 2 * 3` e
  `(1 + 2) * 3`, erro do `for` sem atualização.] [Reescrevi a parte do codigo para adaptação ao projeto e conferi os resultados, alterei a parte do ast_nodes.py na parte de expressões e alterei os comandos do ast_nodes.py e parser.py]
- **Próximos passos:** testes do parser e da AST (hoje pulados), depois o
  interpretador (item e).

///////////////////////////////////////////////////////////////////////////////
- **Fase:** parser e AST (itens c e d), testes e seção do relatório
- **Data do registro:** 17/11
- **Quem fez o quê:**
  - **Luís Felipe Carmelo da Silva:** revisão do item (c); incorporação ao repositório dos testes do parser e da AST (`tests/validos/test_parser_valido.py`, `tests/invalidos/test_parser_invalido.py`); revisão e incorporação ao `docs/relatorio.pdf` da seção "Análise sintática".
  - **Tiago Sales Guimaraes:** implementação do parser e da AST (registrada acima).
- **Decisões tomadas e por quê:**
  - A seção do relatório explicita a técnica (descendente recursiva LL(1)) e a justifica pelo cálculo de FIRST/FOLLOW da gramática do item (a), que não apresenta conflitos.
  - A comparação com técnica alternativa foi feita com análise ascendente LR; o motivo da não escolha é que a gramática já é LL(1) e o projeto exige parser auditável.
  - Os testes incluem laços mal formados e `else if`, que a MiniLang não admite.
- **Dificuldades / descobertas:**
  - Ao testar o aninhamento, o parser aceitou 140 níveis de parênteses e falhou com `RecursionError` em 200. Isso foi registrado como limitação conhecida no relatório.
- **Uso de IA:**
  - **Ferramenta:** Claude Sonnet 5.5 (Anthropic), via claude.ai.
  - **Prompt resumido:** redigir a seção do relatório sobre o parser (técnica, compatibilidade LL(1), árvores, justificativa formal, comparação com LR) e escrever os testes do parser e da AST.
  - **O que veio:** os três arquivos de teste (105 testes passando na suíte) e o rascunho da seção do relatório.
  - **O que precisou ser conferido ou corrigido:** os testes passaram na primeira execução; para checar se realmente detectavam defeitos, o parser foi alterado de propósito de 5 formas. Uma dessas alterações foi construída incorretamente pela IA (equivalia ao código original e por isso "passou" sem ser detectada). Foi percebida e refeita, e as 5 alterações passaram a ser detectadas pelos testes. As árvores e as mensagens de erro do relatório foram geradas executando o `parser.py`, e os conjuntos FIRST/FOLLOW foram calculados e conferidos por execução.
  - **O que foi reescrito e por quê:** [descrever o que o Luís Felipe realmente alterou no texto ou nos testes; se nada foi alterado, escrever "nada foi alterado após a conferência"].
  - **Validação humana:** [confirmar: o Luís Felipe leu a seção, executou `pytest` e conferiu as árvores e mensagens com o `parser.py`]. O grupo deve conseguir explicar o cálculo de FIRST/FOLLOW e as provas da seção 5.
- **Commits:** [colar o hash e a mensagem do commit, por exemplo `docs(relatorio): seção de análise sintática (item c)`].
- **Próximos passos:** relatório do item (d) (diagrama da AST e justificativa); item (e), interpretador e tabela de símbolos.
///////////////////////////////////////////////////////////////////////////////
- **Fase:** AST (item d): revisão dos nós, testes e seção do relatório
- **Data do registro:** 18/11
- **Quem fez o quê:**
  - **João Paulo:** revisão de `src/ast_nodes.py` (escrito pelo Tiago junto com o parser); testes da AST em `tests/validos/test_ast.py` (18 testes); diagrama da AST de um programa com laço (`docs/figuras/ast_programa_com_laco.png`); seção "Árvore sintática abstrata" do relatório (definição dos nós, diagrama, árvore concreta × abstrata e justificativa).
- **Decisões tomadas e por quê:**
  - Manter os nós do Tiago sem mudar a estrutura, porque o parser já depende deles e os testes do parser passavam.
  - Testar o que a AST *descarta* (parênteses não viram nó; nenhum nó representa `;`, `{}` ou palavra-chave) e o que ela *preserva* (as três cláusulas do `for` em campos com nome; `1 + 2 * 3` ≠ `(1 + 2) * 3`).
- **Uso de IA:**
  - **Ferramenta:** Claude Opus 5.5 (Anthropic).
  - **Prompt resumido:** revisar `ast_nodes.py`, escrever os testes da AST pedidos no item (d), gerar o diagrama da AST de um programa com laço e redigir a justificativa de que a AST preserva a semântica.
  - **O que veio:** os testes, o diagrama (gerado a partir da AST real produzida pelo parser) e o texto da seção.
  - **O que estava errado ou redundante:** na função `arvore_texto` de `ast_nodes.py` (gerada pelo Claude Sonnet 5.5 na etapa anterior), havia uma condição que deixava passar `else_body = None` só para descartá-lo na linha seguinte: código morto. Ela foi simplificada, e a saída da função continuou idêntica para o programa de exemplo. O docstring também ainda dizia "TODO".
  - **Validação:** para conferir se os testes detectam defeitos de verdade, o parser foi alterado de propósito de 2 formas: trocar `init` com `update` no nó `For` e criar um nó para os parênteses. Os testes da AST falharam nos dois casos e voltaram a passar com o parser original. Suíte completa: 99 testes passando.
- **Commits:** `Item (d): testes da AST`, `Item (d): revisão de ast_nodes.py`, `Item (d): diagrama da AST`.
- **Próximos passos:** a seção da AST vai para o relatório quando ele for consolidado.

## Semana 2

(repetir o modelo)
