# Definição formal da MiniLang

Este documento define a MiniLang em três níveis, um para cada fase do compilador:

1. **Léxico**: o alfabeto e os tokens, descritos por expressões regulares e reconhecidos por um AFD (seção [Lexer](#lexer)).
2. **Sintático**: uma gramática livre de contexto em EBNF, com precedência e associatividade embutidas na estrutura das produções.
3. **Semântico**: restrições que uma gramática livre de contexto não consegue expressar (tipos, variável definida, divisão por zero). Elas são verificadas pelo interpretador.

---

## 1. Alfabeto

**Alfabeto de caracteres** (Σ): letras ASCII `a–z A–Z`, o sublinhado `_`, dígitos `0–9`, espaço, tabulação, `\r`, `\n` e os símbolos `+ - * / ( ) { } ; < > = !`. Dentro de comentários qualquer caractere é aceito. Fora deles, qualquer caractere que não esteja em Σ (ex.: `@`, `#`, `ç`, `.`) é **erro léxico**.

**Alfabeto de tokens** (os terminais da gramática):

| Categoria | Tokens |
|---|---|
| Literais | `INT`, `TRUE`, `FALSE` |
| Identificador | `ID` |
| Palavras reservadas | `IF`, `ELSE`, `WHILE`, `FOR`, `PRINT` (+ `TRUE`, `FALSE`) |
| Aritméticos | `MAIS` `+`, `MENOS` `-`, `MULT` `*`, `DIV` `/` |
| Relacionais | `MENOR` `<`, `MAIOR` `>`, `MENOR_IGUAL` `<=`, `MAIOR_IGUAL` `>=` |
| Igualdade | `IGUAL` `==`, `DIFERENTE` `!=` |
| Atribuição | `ATRIB` `=` |
| Delimitadores | `ABRE_PAR` `(`, `FECHA_PAR` `)`, `ABRE_CHAVE` `{`, `FECHA_CHAVE` `}`, `PONTO_VIRGULA` `;` |
| Fim | `EOF` |

Espaços em branco e comentários (`// ...` até o fim da linha e `/* ... */`) são reconhecidos e **descartados** pelo lexer. Eles não chegam ao parser.

> **Observação sobre comentários de bloco.** O escopo obrigatório pede só comentários de linha. Mesmo assim, o item (b) exige testar "comentário não fechado", e um comentário `//` sempre termina (no `\n` ou no fim do arquivo). Por isso a MiniLang aceita também `/* ... */`, e o caso de erro é `/*` sem o `*/` correspondente.

---

## 2. Gramática EBNF

Notação: `{ X }` = zero ou mais repetições, `[ X ]` = opcional, `( A | B )` = alternativa, `"x"` = terminal literal, nomes em MAIÚSCULAS = tokens.

```ebnf
(* ---------- Estrutura ---------- *)
programa     = { comando } EOF ;

comando      = atribuicao ";"
             | comando_print
             | comando_if
             | comando_while
             | comando_for
             | bloco ;

atribuicao   = ID "=" expressao ;
comando_print= "print" "(" expressao ")" ";" ;
comando_if   = "if" "(" expressao ")" bloco [ "else" bloco ] ;
bloco        = "{" { comando } "}" ;

(* ---------- Laços ---------- *)
comando_while= "while" "(" expressao ")" bloco ;
comando_for  = "for" "(" atribuicao ";" expressao ";" atribuicao ")" bloco ;
               (*       inicialização  condição     atualização          *)
               (* as três cláusulas são obrigatórias: sem cláusulas vazias *)

(* ---------- Expressões: da MENOR para a MAIOR precedência ---------- *)
expressao    = igualdade ;
igualdade    = comparacao { ( "==" | "!=" ) comparacao } ;
comparacao   = termo [ ( "<" | ">" | "<=" | ">=" ) termo ] ;
termo        = fator { ( "+" | "-" ) fator } ;
fator        = unario { ( "*" | "/" ) unario } ;
unario       = "-" unario
             | primario ;
primario     = INT
             | "true"
             | "false"
             | ID
             | "(" expressao ")" ;

(* ---------- Léxico (expressões regulares) ---------- *)
ID           = letra { letra | digito } ;      (* exceto palavras reservadas *)
INT          = digito { digito } ;
letra        = "a".."z" | "A".."Z" | "_" ;
digito       = "0".."9" ;
```

### Como a gramática codifica precedência e associatividade

- **Precedência por níveis.** Cada nível de precedência é um não terminal. Um operador de nível mais alto só aparece *dentro* dos operandos do nível mais baixo. Por exemplo, `termo` é formado por `fator`s, então `*` fica mais fundo na árvore do que `+` e é avaliado primeiro.
- **Associatividade à esquerda com repetição.** `termo = fator { ("+"|"-") fator }` lê `a - b - c` como a sequência `a, -b, -c`, e o parser monta a árvore acumulando à esquerda: `((a - b) - c)`. Isso dá o mesmo resultado da produção recursiva à esquerda `termo → termo "-" fator`, só que sem recursão à esquerda, que um parser descendente não suporta.
- **Relacionais não associativos.** Em `comparacao` o operador aparece com `[ ]` (no máximo uma vez), então `a < b < c` é **erro sintático**. É uma escolha de projeto: `(a < b) < c` compararia `bool < int` e já seria erro de tipo. Rejeitar isso na sintaxe dá uma mensagem mais clara e mais cedo.
- **Menos unário à direita.** Em `unario = "-" unario` a recursão é à direita, então `- -5 = -(-5)`.

### Tabela de precedência e associatividade

| Nível (1 = menor) | Operadores | Associatividade | Não terminal |
|---|---|---|---|
| 1 | `==` `!=` | esquerda | `igualdade` |
| 2 | `<` `>` `<=` `>=` | **não associativo** | `comparacao` |
| 3 | `+` `-` (binário) | esquerda | `termo` |
| 4 | `*` `/` | esquerda | `fator` |
| 5 | `-` (unário) | direita | `unario` |
| 6 | literais, variáveis, `( )` | — | `primario` |

A atribuição `=` não é operador de expressão (`x = y = 1` é inválido). Ela é um comando.

### Restrições semânticas (fora da gramática)

| Código | Restrição |
|---|---|
| S1 | Toda variável usada numa expressão deve ter sido atribuída antes (na ordem de execução). |
| S2 | `+ - * /`, `-` unário e `< > <= >=` exigem operandos `int`. |
| S3 | `==` e `!=` exigem operandos do **mesmo** tipo. |
| S4 | A condição de `if`, `while` e `for` deve ter tipo `bool`. |
| S5 | O tipo de uma variável é fixado na 1ª atribuição. Reatribuir com outro tipo é erro. |
| S6 | O divisor de `/` não pode ser 0. |

Tipos dos resultados: `+ - * /` e `-` unário produzem `int`. Os operadores relacionais e de igualdade produzem `bool`. A divisão é inteira e **truncada em direção a zero** (`-7 / 2 = -3`).

---

## 3. Cinco programas de exemplo (comentados)

### Exemplo 1 — VÁLIDO (com `while` e `for`)

```c
x = 10;
y = 2 * (x + 5);
while (x > 0) { print(x); x = x - 1; }
soma = 0;
for (i = 0; i < 5; i = i + 1) { soma = soma + i; }
if (soma > 20) { print(soma); } else { print(0); }
```

**Justificativa.** *Léxico:* todos os caracteres pertencem a Σ e cada lexema casa com uma ER da tabela de tokens. *Sintático:* existe derivação a partir de `programa`. Cada linha é um `comando`, e o `for` tem as três cláusulas na ordem `atribuicao ";" expressao ";" atribuicao`. *Semântico:* toda variável é atribuída antes do uso (S1), as condições `x > 0`, `i < 5` e `soma > 20` são `bool` (S4), toda aritmética é entre `int` (S2) e não há divisão. Saída: `10 9 … 1 0`. A versão completa está em `exemplos/programa_valido.ml`.

### Exemplo 2 — INVÁLIDO LÉXICO

```c
a = 3 @ 2;
b = 1x + 1;
```

**Justificativa.** `@ ∉ Σ`: o caractere não pertence ao alfabeto, então nenhuma expressão regular de token casa com ele (*caractere inválido*). `1x` não casa com `INT = digito { digito }` nem com `ID = letra { letra | digito }`, porque um identificador não pode começar com dígito. Um dígito seguido imediatamente de letra não forma nenhum token válido (*token mal formado*). As duas violações são do nível léxico, pois acontecem antes de qualquer regra da gramática ser aplicada. O lexer reporta **os dois** erros.

### Exemplo 3 — INVÁLIDO SINTÁTICO

```c
x = (1 + ;
```

**Justificativa.** Todos os tokens são válidos (`ID ATRIB ABRE_PAR INT MAIS PONTO_VIRGULA`), então o erro não é léxico. Depois do `+`, a produção `termo = fator { ("+"|"-") fator }` exige um `fator`, cujo FIRST é `{ "-", INT, true, false, ID, "(" }`, e o token seguinte é `;`. Nenhuma produção se aplica: *"esperada uma expressão, encontrado ';'"*. Além disso, o `(` nunca é fechado.

### Exemplo 4 — INVÁLIDO SINTÁTICO: laço mal formado

```c
for (i = 0; i < 10) { print(i); }
```

**Justificativa.** A produção `comando_for = "for" "(" atribuicao ";" expressao ";" atribuicao ")" bloco` exige **dois** `;` dentro dos parênteses. Depois da condição `i < 10` o parser espera `";"` e encontra `")"`. Viola a restrição de que as três cláusulas são obrigatórias (não há cláusula vazia na gramática). Ver `exemplos/programa_invalido.ml`.

### Exemplo 5 — INVÁLIDO SEMÂNTICO (laço com condição não booleana e variável não definida)

```c
x = 3;
while (x) { x = x - 1; }
for (i = 0; j < 3; i = i + 1) { print(i); }
```

**Justificativa.** O programa é **léxica e sintaticamente correto**: `while "(" expressao ")" bloco` aceita qualquer `expressao`, inclusive um `ID` sozinho. Uma gramática livre de contexto não sabe que tipo `x` tem. Na execução, a condição `x` vale `3 : int`, o que viola **S4** (*"a condição do 'while' deve ser booleana, mas é int"*). Se o `while` fosse corrigido, o `for` violaria **S1**, porque `j` nunca foi atribuída (*"variável 'j' não definida"*). A primeira violação encontrada interrompe a execução.

---


## Lexer

### Tabela de tokens

| Tipo | Padrão (regex) | Exemplo |
|---|---|---|

### Tabela de transições do AFD

TODO (item b)
