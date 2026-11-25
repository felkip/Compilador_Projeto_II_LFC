---
title: "Catálogo de erros e estratégia de diagnóstico (item f)"
---

# Catálogo de erros e estratégia de diagnóstico

## 1. Critério de classificação

Os erros da MiniLang foram separados conforme a classe de linguagem que a entrada deixa de satisfazer. Cada classe corresponde a uma fase do compilador.

| Categoria | Definição formal | Fase que detecta |
|---|--------------------------|------|
| **Léxico** | Um trecho do texto não pertence à linguagem regular dos tokens (nenhuma expressão regular casa, ou o AFD cai em um estado de erro). | `lexer.py` |
| **Sintático** | Os tokens são válidos, mas a sequência não pertence a L(G), a linguagem livre de contexto da gramática EBNF. No parser LL(1), o token atual não está em nenhum FIRST aplicável. | `parser.py` |
| **Semântico** | A sentença pertence a L(G), mas viola uma restrição que uma gramática livre de contexto não consegue expressar (S1 a S6 em `docs/gramatica.md`). | `interpreter.py` |

A terceira linha é a razão de existir a categoria semântica. Verificar "toda variável é atribuída antes de ser usada" exige lembrar quais nomes já apareceram. Isso é parecido com o problema clássico de reconhecer {ww}, que não é livre de contexto. Uma gramática livre de contexto não tem essa memória. Por isso a verificação foi colocada na tabela de símbolos do interpretador, e não na gramática.

## 2. Catálogo

### 2.1 Erros léxicos

| Cód. | Mensagem | Causa | Exemplo |
|--|--------------|--------------------|-------------|
| L1 | `caractere não permitido` | O caractere não pertence ao alfabeto Σ, então nenhuma ER de token o aceita. | `x = 2 @ 3;` |
| L2 | `número malformado: dígito seguido de letra` | Um `INT` seguido de letra ou `_`. Pelo maior casamento seriam `INT` + `ID`, mas um identificador não pode começar com dígito. | `x = 1x + 2;` |
| L3 | `'!' isolado; esperado '=' para formar '!='` | O único token que começa com `!` é `!=`. | `x ! 2;` |
| L4 | `comentário de bloco não fechado; esperado '*/'` | O AFD chega ao fim da entrada ainda dentro de `/* ...`. | `/* sem fim` |

### 2.2 Erros sintáticos

| Cód. | Mensagem (resumo) | Causa | Exemplo |
|--|--------------|--------------------|-------------|
| P1 | `esperado ';' após a atribuição / o 'print'` | Comando terminado sem `;`. | `x = 1` + nova linha |
| P2 | `esperada uma expressão, encontrado X` | O token não está em FIRST(fator) = { `-`, INT, `true`, `false`, ID, `(` }. | `x = (1 + ;` |
| P3 | `esperado ')' ...` | Parêntese aberto e não fechado (expressão, `if`, `while`, `for`, `print`). | `print(1;` |
| P4 | `esperado '}' para fechar o bloco` | Bloco aberto e chegada ao fim do arquivo. | `while (true) { print(1);` |
| P5 | `esperado '{' para iniciar o bloco` | `if`, `while` e `for` exigem bloco com chaves. | `if (true) print(1);` |
| P6 | `esperado um comando, encontrado X` | Início de comando que não está em { ID, `print`, `if`, `while`, `for`, `{` }. Inclui `else` sem `if`. | `1 + 2;` |
| P7 | `operadores relacionais não são associativos` | `comparacao` aceita no máximo um operador relacional (escolha de projeto). | `x = 1 < 2 < 3;` |
| P8 | `esperado '(' após 'print' / 'if' / 'while' / 'for'` | Falta o parêntese que abre a condição ou o argumento. | `print x;` |
| P9 | **Laço:** `esperado ';' após a condição do 'for' (a cláusula de atualização é obrigatória)`; com cláusula vazia, `esperado um identificador` (inicialização ou atualização) ou `esperada uma expressão` (condição) | O `for` tem exatamente três cláusulas (`atribuicao ";" expressao ";" atribuicao`). Não existe cláusula vazia. | `for (i = 0; i < 10) {...}`; `for (; i < 3; i = i + 1) {...}` |

### 2.3 Erros semânticos

| Cód. | Mensagem | Causa (restrição violada) | Exemplo |
|--|--------------|--------------------|-------------|
| S1 | `variável 'v' não definida` | Uso de variável nunca atribuída antes na ordem de execução. Em um `for`, vale também para a variável de controle. | `print(y);` |
| S2 | `o operador '+' exige operandos int, mas recebeu int e bool` (no `-` unário: `exige operando int, mas recebeu bool`) | Aritmética, `-` unário ou relacional com operando booleano. | `x = 1 + true;` |
| S3 | `'==' exige operandos do mesmo tipo, mas recebeu int e bool` | `==` e `!=` com operandos de tipos diferentes. | `x = 1 == true;` |
| S4 | **Laço:** `a condição do 'while' deve ser booleana, mas é int` (idem para `if` e `for`) | Condição de tipo `int`. | `while (x) {...}` |
| S5 | `a variável 'x' foi criada como int na linha 1 e não pode receber um valor bool` | O tipo da variável é fixado na 1ª atribuição. | `x = 1; x = true;` |
| S6 | `divisão por zero` | O divisor vale 0 em tempo de execução. | `4 / (2 - 2)` |

Existem também as **travas de execução**, que não são erros léxicos, sintáticos nem semânticos e não fazem parte da linguagem: `limite de N iterações excedido (laço da linha L)`, o limite de 10.000 bits dos inteiros e a profundidade máxima de aninhamento (todas com código de saída 4). Elas protegem a máquina e a suíte de testes. Em especial, não há como decidir estaticamente se um laço termina, porque isso equivale ao problema da parada; o limite de iterações é uma proteção prática e não uma análise.

## 3. Demonstração por execução

Cada linha abaixo foi obtida com `python -m src.interpreter exemplos/erros/<arquivo>.ml`. O transcrito completo está em `docs/execucao_erros.txt` (gerado por `sh exemplos/demo_erros.sh`) e as mesmas execuções são conferidas automaticamente em `tests/invalidos/test_exemplos_erros.py`.

| Categoria | Arquivo | Saída (diagnóstico) | Saída do processo |
|----|----------------|------------------------|--|
| Léxico | `lexico_1_caractere_invalido.ml` | `caractere não permitido em 2:7 ('@')` | 1 |
| Léxico | `lexico_2_numero_malformado.ml` | `número malformado: dígito seguido de letra em 2:5 ('1x')` | 1 |
| Léxico | `lexico_3_comentario_aberto.ml` | `comentário de bloco não fechado; esperado '*/' em 3:1` (o lexema reportado vai até o fim do arquivo) | 1 |
| Sintático | `sintatico_1_for_sem_atualizacao.ml` | `esperado ';' após a condição do 'for' (a cláusula de atualização é obrigatória), encontrado ')' em 2:19` | 2 |
| Sintático | `sintatico_2_expressao_incompleta.ml` | `esperada uma expressão, encontrado ';' em 2:10` | 2 |
| Sintático | `sintatico_3_ponto_virgula_ausente.ml` | `esperado ';' após a atribuição, encontrado 'print' em 3:1` | 2 |
| Semântico (laço) | `semantico_1_while_nao_booleano.ml` | `[S4] a condição do 'while' deve ser booleana, mas é int (linha 3)` | 3 |
| Semântico (laço) | `semantico_2_for_variavel_indefinida.ml` | `[S1] variável 'j' não definida (linha 2)` | 3 |
| Semântico | `semantico_3_divisao_por_zero.ml` | imprime `1`, depois `[S6] divisão por zero (linha 3)` | 3 |
| Semântico | `semantico_4_tipo_incompativel.ml` | `[S2] o operador '+' exige operandos int, mas recebeu int e bool (linha 2)` | 3 |

Os demais casos (L3, P3 a P8, P9 com cláusula vazia, S3, S4 em `if` e `for`, S5) estão em `tests/invalidos/test_lexer_invalido.py`, `test_parser_invalido.py` e `test_interpreter_invalido.py`, um arquivo por categoria, cada um com o resultado esperado em comentário no topo.

## 4. Estratégia de recuperação e diagnóstico, e por que foi escolhida

**Fases em cascata, com bloqueio.** Se o lexer encontra erro, o parser não roda. Se o parser encontra erro, nada é executado. A razão é que cada fase assume que sua entrada satisfaz o contrato da anterior. O parser pressupõe tokens do alfabeto de tokens, e o interpretador pressupõe uma AST que veio de uma derivação válida. Executar parcialmente um programa sintaticamente errado produziria efeitos (`print`) baseados em um programa que não existe na linguagem.

**Léxico: registrar, pular o lexema e continuar.** O lexer acumula todos os erros e lança um `LexicalError` com a lista completa no fim. Isso é viável porque um AFD é determinístico e não tem pilha. A decisão sobre cada lexema é local e o ponto de retomada é bem definido: o primeiro caractere fora do trecho problemático. Por isso um erro não contamina o próximo. Com `x = @;` e `y = 1x;` em linhas seguidas, são reportados dois erros independentes (1:5 e 2:5). Em `1x2y`, a sequência inteira é consumida como um erro só, evitando que o mesmo erro seja relatado duas vezes. A exceção é o comentário não fechado: não existe ponto de retomada seguro, porque o resto do arquivo ainda poderia ser texto de comentário, então o lexer consome até o fim e relata um único erro.

**Sintático: parar no primeiro erro (*fail-fast*).** O parser é LL(1) preditivo e tem a propriedade do prefixo viável: tudo que foi lido antes do token ofensor ainda pode ser prefixo de alguma sentença de L(G), e o token ofensor é o primeiro que não consegue estender esse prefixo. Por isso a posição reportada é precisa. A alternativa seria o modo pânico, descartando tokens até um conjunto de sincronização (por exemplo `;` e `}`, derivados de FOLLOW) e continuando. Ela foi descartada por dois motivos. Primeiro, depois de um erro sintático o parser já não sabe em que produção está, e os erros seguintes tendem a ser espúrios (uma `}` faltando pode gerar vários "esperado um comando" em cascata). Segundo, o público da MiniLang é formado por iniciantes, e uma única mensagem correta, com linha, coluna, o que era esperado e o que foi encontrado, ajuda mais do que uma lista longa em que só a primeira é confiável. O custo é aceito: o aluno corrige um erro sintático por vez. Há ainda uma limitação inerente ao método: o erro é relatado onde é *detectado*, que pode ser depois da causa real. Em `x = 1` seguido de `print(x);` na linha seguinte, o erro aparece em `3:1`, no token `print`, e não no fim da linha anterior.

**Semântico: parar no primeiro erro, em tempo de execução.** O interpretador verifica S1 a S6 enquanto avalia cada nó, usando a tabela de símbolos (nome → tipo, valor). Depois de um erro semântico o estado do programa deixa de ser confiável. Se `x` não foi definida, cada uso posterior de `x` seria outro erro, todos consequência do primeiro. Em termos de semântica operacional, a configuração ⟨comando, σ⟩ não tem regra aplicável e a execução termina em erro, e o que já foi impresso continua valendo (`semantico_3_divisao_por_zero.ml` imprime `1` antes do erro). Uma limitação desta escolha é que só se detectam erros nos caminhos que realmente executam: uma variável indefinida dentro de um `if` que não é tomado não gera erro naquela execução. Uma verificação estática antes da execução cobriria todos os caminhos, mas foge ao escopo pedido, em que o interpretador é quem rejeita os programas inválidos.

**Formato do diagnóstico.** Toda mensagem diz onde (linha e coluna nos erros léxicos e sintáticos, linha nos semânticos), o que se esperava, o que foi encontrado e, nos semânticos, o código da restrição violada (S1 a S6), que aponta para `docs/gramatica.md`. O código de saída do processo identifica a fase (1 léxico, 2 sintático, 3 semântico, 4 trava de execução, 5 arquivo ilegível), o que permite testar as categorias automaticamente.
