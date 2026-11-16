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
- Commits da semana: item (a): elaboração inicial da gramática e dos exemplos, seguida de revisão e correções na documentação. Registrar os commits específicos ao longo da semana.
- Próximos passos: concluir a validação da gramática pelo grupo; revisar os exemplos; avançar para as próximas etapas do projeto, incluindo o item (b), analisador léxico, e o item (d), src/ast_nodes.py, conforme a divisão de tarefas do grupo.
  
Observação: como a semana vai até 22/11, este registro deve ser complementado conforme novas atividades forem realizadas. Não registrar como concluídas tarefas que ainda estão previstas.

## Semana 2

(repetir o modelo)
