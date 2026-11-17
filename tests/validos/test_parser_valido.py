"""Parsing valido, incluindo while e for.

RESULTADO ESPERADO: todos os programas abaixo sao aceitos e a AST produzida
tem exatamente a forma indicada em cada teste (precedencia e associatividade
ficam codificadas na forma da arvore).
"""
from pathlib import Path

import pytest

from src.ast_nodes import (Assign, Binary, Block, Bool, For, If, Num, Print,
                           Program, Unary, Var, While)
from src.parser import parse

RAIZ = Path(__file__).resolve().parents[2]
a, b, c, d = Var("a"), Var("b"), Var("c"), Var("d")


def expr(fonte):
    """AST da expressao `fonte`, embrulhada como `x = <fonte>;`."""
    return parse(f"x = {fonte};").statements[0].value


# --------------------------------------------------------------------------
# Precedencia
# --------------------------------------------------------------------------
def test_multiplicacao_tem_precedencia_sobre_soma():
    assert expr("1 + 2 * 3") == Binary("+", Num(1), Binary("*", Num(2), Num(3)))


def test_parenteses_mudam_a_arvore():
    com = expr("(1 + 2) * 3")
    sem = expr("1 + 2 * 3")
    assert com == Binary("*", Binary("+", Num(1), Num(2)), Num(3))
    assert com != sem


@pytest.mark.parametrize("fonte,esperado", [
    # aritmetica acima de relacional
    ("1 + 2 < 3 * 4", Binary("<", Binary("+", Num(1), Num(2)), Binary("*", Num(3), Num(4)))),
    # relacional acima de igualdade
    ("a < b == c < d", Binary("==", Binary("<", a, b), Binary("<", c, d))),
    ("a == b < c", Binary("==", a, Binary("<", b, c))),
    # unario acima de multiplicativo
    ("-2 * 3", Binary("*", Unary("-", Num(2)), Num(3))),
    ("1 - -2", Binary("-", Num(1), Unary("-", Num(2)))),
    ("-(1 + 2)", Unary("-", Binary("+", Num(1), Num(2)))),
])
def test_niveis_de_precedencia(fonte, esperado):
    assert expr(fonte) == esperado


# --------------------------------------------------------------------------
# Associatividade
# --------------------------------------------------------------------------
@pytest.mark.parametrize("fonte,esperado", [
    ("10 - 3 - 2", Binary("-", Binary("-", Num(10), Num(3)), Num(2))),
    ("8 / 2 / 2", Binary("/", Binary("/", Num(8), Num(2)), Num(2))),
    ("1 - 2 + 3", Binary("+", Binary("-", Num(1), Num(2)), Num(3))),
    ("2 * 3 / 4", Binary("/", Binary("*", Num(2), Num(3)), Num(4))),
    ("a + b + c", Binary("+", Binary("+", a, b), c)),
    # igualdade tambem e associativa a esquerda (o erro de tipo e do interpretador)
    ("a == b != c", Binary("!=", Binary("==", a, b), c)),
])
def test_operadores_binarios_associam_a_esquerda(fonte, esperado):
    assert expr(fonte) == esperado


def test_menos_unario_associa_a_direita():
    assert expr("- -5") == Unary("-", Unary("-", Num(5)))
    assert expr("---5") == Unary("-", Unary("-", Unary("-", Num(5))))


def test_parenteses_redundantes_nao_deixam_no_na_arvore():
    assert expr("((7))") == Num(7)
    assert parse("x = (1);") == parse("x = 1;")


def test_literais_booleanos_e_variaveis():
    assert expr("true") == Bool(True)
    assert expr("false") == Bool(False)
    assert expr("true == false") == Binary("==", Bool(True), Bool(False))
    assert expr("soma") == Var("soma")


# --------------------------------------------------------------------------
# Comandos simples
# --------------------------------------------------------------------------
def test_atribuicao():
    assert parse("x = 1;") == Program([Assign("x", Num(1))])


def test_print():
    assert parse("print(x + 1);") == Program([Print(Binary("+", Var("x"), Num(1)))])


def test_programa_vazio_ou_so_comentarios():
    assert parse("") == Program([])
    assert parse("// nada\n/* nada */") == Program([])


def test_comentarios_nao_mudam_a_arvore():
    com = parse("x = 1; // um\n/* dois */ y = 2;")
    sem = parse("x = 1; y = 2;")
    assert com == sem


def test_bloco_avulso_e_blocos_aninhados():
    esperado = Program([Block([Assign("x", Num(1)), Block([Assign("y", Num(2))])])])
    assert parse("{ x = 1; { y = 2; } }") == esperado


def test_bloco_vazio():
    assert parse("if (true) { }") == Program([If(Bool(True), Block([]), None)])


# --------------------------------------------------------------------------
# if / else
# --------------------------------------------------------------------------
def test_if_sem_else():
    no = parse("if (x > 0) { print(x); }").statements[0]
    assert no == If(Binary(">", Var("x"), Num(0)), Block([Print(Var("x"))]), None)
    assert no.else_body is None


def test_if_com_else():
    no = parse("if (soma > 20) { print(soma); } else { print(0); }").statements[0]
    assert no.then_body == Block([Print(Var("soma"))])
    assert no.else_body == Block([Print(Num(0))])


def test_if_dentro_do_else():
    no = parse("if (a) { } else { if (b) { x = 1; } }").statements[0]
    assert no.else_body == Block([If(b, Block([Assign("x", Num(1))]), None)])


# --------------------------------------------------------------------------
# while
# --------------------------------------------------------------------------
def test_while():
    no = parse("while (x > 0) { print(x); x = x - 1; }").statements[0]
    assert no == While(
        Binary(">", Var("x"), Num(0)),
        Block([Print(Var("x")), Assign("x", Binary("-", Var("x"), Num(1)))]),
    )


def test_while_com_condicao_booleana_literal_e_corpo_vazio():
    assert parse("while (false) { }").statements[0] == While(Bool(False), Block([]))


# --------------------------------------------------------------------------
# for: as tres clausulas
# --------------------------------------------------------------------------
def test_for_com_as_tres_clausulas():
    no = parse("for (i = 0; i < 5; i = i + 1) { soma = soma + i; }").statements[0]
    assert isinstance(no, For)
    assert no.init == Assign("i", Num(0))                                    # inicializacao
    assert no.condition == Binary("<", Var("i"), Num(5))                     # condicao
    assert no.update == Assign("i", Binary("+", Var("i"), Num(1)))           # atualizacao
    assert no.body == Block([Assign("soma", Binary("+", Var("soma"), Var("i")))])


def test_for_com_passo_diferente_de_um():
    no = parse("for (i = 10; i > 0; i = i - 2) { print(i); }").statements[0]
    assert no.init == Assign("i", Num(10))
    assert no.update == Assign("i", Binary("-", Var("i"), Num(2)))


def test_for_com_corpo_vazio():
    assert parse("for (i = 0; i < 3; i = i + 1) { }").statements[0].body == Block([])


def test_lacos_aninhados():
    fonte = """
    while (x > 0) {
      for (i = 0; i < 2; i = i + 1) { print(i); }
      x = x - 1;
    }
    """
    no = parse(fonte).statements[0]
    assert isinstance(no, While)
    assert isinstance(no.body.statements[0], For)
    assert isinstance(no.body.statements[1], Assign)


# --------------------------------------------------------------------------
# Posicao (linha) guardada na AST, fora da comparacao
# --------------------------------------------------------------------------
def test_linhas_ficam_nos_nos_mas_nao_entram_na_comparacao():
    no = parse("x = 1;\nfor (i = 0; i < 2; i = i + 1) {\n}\n").statements[1]
    assert no.line == 2 and no.init.line == 2
    assert parse("x = 1;\ny = 2;") == parse("x = 1; y = 2;")


# --------------------------------------------------------------------------
# Programas completos
# --------------------------------------------------------------------------
def test_programa_valido_do_repositorio():
    fonte = (RAIZ / "exemplos" / "programa_valido.ml").read_text(encoding="utf-8")
    prog = parse(fonte)
    assert [type(s).__name__ for s in prog.statements] == [
        "Assign", "Assign", "Print", "While", "Assign", "For", "If",
        "Assign", "Print", "Print",
    ]


def test_exemplo_1_do_gramatica_md():
    fonte = """
    x = 10;
    y = 2 * (x + 5);
    while (x > 0) { print(x); x = x - 1; }
    soma = 0;
    for (i = 0; i < 5; i = i + 1) { soma = soma + i; }
    if (soma > 20) { print(soma); } else { print(0); }
    """
    prog = parse(fonte)
    assert [type(s).__name__ for s in prog.statements] == [
        "Assign", "Assign", "While", "Assign", "For", "If"]
    assert prog.statements[1].value == Binary(
        "*", Num(2), Binary("+", Var("x"), Num(5)))
