"""Testes da AST (item d): construcao e verificacao dos nos.

RESULTADO ESPERADO: todos os testes passam.
- A AST de 1 + 2 * 3 tem o '*' mais fundo que o '+' (precedencia).
- A AST de (1 + 2) * 3 tem o '+' mais fundo, e os parenteses NAO viram no.
- O no For guarda as tres clausulas (init, condition, update) e o corpo.
- O no While guarda a condicao e o corpo.
- A AST descarta os simbolos que so servem a sintaxe (';', '(', ')', '{',
  '}', palavras-chave) sem perder nada que a execucao precise.
"""
import dataclasses
from pathlib import Path

import pytest

from src.ast_nodes import (Assign, Binary, Block, Bool, For, If, Num, Print,
                           Program, Unary, Var, While, arvore_texto)
from src.parser import parse

RAIZ = Path(__file__).resolve().parents[2]


def expr(fonte):
    """AST da expressao `fonte`, embrulhada como `x = <fonte>;`."""
    return parse(f"x = {fonte};").statements[0].value


def comando(fonte):
    """AST do unico comando do programa `fonte`."""
    programa = parse(fonte)
    assert len(programa.statements) == 1
    return programa.statements[0]


# --------------------------------------------------------------------------
# 1 + 2 * 3  versus  (1 + 2) * 3
# --------------------------------------------------------------------------
def test_ast_1_mais_2_vezes_3():
    esperado = Binary("+", Num(1), Binary("*", Num(2), Num(3)))
    assert expr("1 + 2 * 3") == esperado


def test_ast_1_mais_2_entre_parenteses_vezes_3():
    esperado = Binary("*", Binary("+", Num(1), Num(2)), Num(3))
    assert expr("(1 + 2) * 3") == esperado


def test_as_duas_arvores_sao_diferentes():
    # Mesmos numeros e operadores, estrutura diferente => resultados diferentes
    # (7 e 9). A ordem de avaliacao esta na FORMA da arvore.
    assert expr("1 + 2 * 3") != expr("(1 + 2) * 3")


def test_parenteses_nao_viram_no():
    # Parenteses so agrupam: depois do parsing, a forma da arvore ja guarda o
    # agrupamento, entao eles podem ser descartados.
    assert expr("((((1))))") == Num(1)
    assert expr("(x)") == Var("x")


def test_associatividade_a_esquerda_na_ast():
    assert expr("10 - 3 - 2") == Binary("-", Binary("-", Num(10), Num(3)), Num(2))


def test_menos_unario_na_ast():
    assert expr("- -5") == Unary("-", Unary("-", Num(5)))


# --------------------------------------------------------------------------
# Lacos: For com as tres clausulas e While
# --------------------------------------------------------------------------
def test_ast_for_com_as_tres_clausulas():
    no = comando("for (i = 0; i < 10; i = i + 1) { print(i); }")
    assert isinstance(no, For)
    assert no.init == Assign("i", Num(0))                                # inicializacao
    assert no.condition == Binary("<", Var("i"), Num(10))                # condicao
    assert no.update == Assign("i", Binary("+", Var("i"), Num(1)))       # atualizacao
    assert no.body == Block([Print(Var("i"))])                           # corpo


def test_campos_do_no_for():
    nomes = [f.name for f in dataclasses.fields(For) if f.name != "line"]
    assert nomes == ["init", "condition", "update", "body"]


def test_ast_while():
    no = comando("while (x < 10) { x = x + 1; }")
    assert no == While(
        Binary("<", Var("x"), Num(10)),
        Block([Assign("x", Binary("+", Var("x"), Num(1)))]),
    )


def test_campos_do_no_while():
    nomes = [f.name for f in dataclasses.fields(While) if f.name != "line"]
    assert nomes == ["condition", "body"]


# --------------------------------------------------------------------------
# Construcao manual = resultado do parser
# --------------------------------------------------------------------------
def test_ast_construida_a_mao_igual_a_do_parser():
    fonte = """
    soma = 0;
    for (i = 0; i < 3; i = i + 1) { soma = soma + i; }
    if (soma == 3) { print(true); } else { print(false); }
    """
    esperado = Program([
        Assign("soma", Num(0)),
        For(
            Assign("i", Num(0)),
            Binary("<", Var("i"), Num(3)),
            Assign("i", Binary("+", Var("i"), Num(1))),
            Block([Assign("soma", Binary("+", Var("soma"), Var("i")))]),
        ),
        If(
            Binary("==", Var("soma"), Num(3)),
            Block([Print(Bool(True))]),
            Block([Print(Bool(False))]),
        ),
    ])
    assert parse(fonte) == esperado


def test_if_sem_else_tem_else_body_vazio():
    assert comando("if (true) { print(1); }") == If(Bool(True), Block([Print(Num(1))]), None)


def test_programa_valido_completo_gera_ast():
    fonte = (RAIZ / "exemplos" / "programa_valido.ml").read_text(encoding="utf-8")
    tipos = [type(c) for c in parse(fonte).statements]
    assert While in tipos and For in tipos and If in tipos


# --------------------------------------------------------------------------
# O que a AST abstrai e o que ela preserva
# --------------------------------------------------------------------------
def test_ast_so_tem_nos_semanticos():
    # Nenhum no da AST representa ';', parenteses, chaves ou palavras-chave.
    fonte = "for (i = 0; i < 2; i = i + 1) { if (i == 1) { print(i); } }"
    permitidos = {Program, Block, Assign, Print, If, While, For,
                  Num, Bool, Var, Unary, Binary}

    def visitar(no):
        if isinstance(no, list):
            for filho in no:
                visitar(filho)
            return
        assert type(no) in permitidos
        for f in dataclasses.fields(no):
            valor = getattr(no, f.name)
            if dataclasses.is_dataclass(valor) or isinstance(valor, list):
                visitar(valor)

    visitar(parse(fonte))


def test_linha_e_guardada_mas_nao_entra_na_comparacao():
    # `line` serve para mensagens de erro; nao muda o significado do no.
    programa = parse("x = 1;\nwhile (x > 0) {\n  x = x - 1;\n}")
    laco = programa.statements[1]
    assert laco.line == 2
    assert laco.body.statements[0].line == 3
    assert Num(1, line=5) == Num(1, line=9)


def test_nos_sao_imutaveis():
    no = Num(1)
    with pytest.raises(dataclasses.FrozenInstanceError):
        no.value = 2


def test_arvore_texto_de_1_mais_2_vezes_3():
    texto = arvore_texto(expr("1 + 2 * 3"))
    assert texto == (
        "Binary(op='+')\n"
        "  .left:\n"
        "    Num(value=1)\n"
        "  .right:\n"
        "    Binary(op='*')\n"
        "      .left:\n"
        "        Num(value=2)\n"
        "      .right:\n"
        "        Num(value=3)\n"
    )


def test_arvore_texto_omite_else_ausente():
    texto = arvore_texto(comando("if (true) { print(1); }"))
    assert ".then_body:" in texto
    assert "else_body" not in texto
