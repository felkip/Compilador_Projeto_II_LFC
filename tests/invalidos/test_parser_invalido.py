# RESULTADO ESPERADO (categoria: erro SINTATICO)
#   Todo programa abaixo e lexicamente valido e viola uma producao da gramatica;
#   parse() levanta ParseError (sem executar nada) com mensagem, linha e coluna
#   do token inesperado. O parser para no PRIMEIRO erro.
#   Lacos mal formados:
#     for (i = 0; i < 10) { ... }          -> "esperado ';' apos a condicao do 'for' ..." (1:19)
#     for (; i < 10; i = i + 1) { }        -> "esperado um identificador" (1:6)
#     for (i = 0; ; i = i + 1) { }         -> "esperada uma expressao" (1:13)
#   Outros:
#     x = (1 + ;     -> "esperada uma expressao, encontrado ';'"
#     1 < 2 < 3      -> "operadores relacionais nao sao associativos"
#     x = 1          -> "esperado ';' apos a atribuicao, encontrado fim do arquivo"
# Erros LEXICOS que atravessam parse() continuam sendo LexicalError (outra fase).
from pathlib import Path

import pytest

from src.lexer import LexicalError
from src.parser import ParseError, parse

RAIZ = Path(__file__).resolve().parents[2]


def erro(fonte):
    with pytest.raises(ParseError) as exc:
        parse(fonte)
    return exc.value


# --------------------------------------------------------------------------
# Lacos mal formados (for)
# --------------------------------------------------------------------------
def test_for_sem_clausula_de_atualizacao():
    e = erro("for (i = 0; i < 10) { print(i); }")
    assert "esperado ';' após a condição do 'for'" in e.message
    assert "atualização é obrigatória" in e.message
    assert (e.line, e.column) == (1, 19)


def test_for_sem_inicializacao():
    e = erro("for (; i < 10; i = i + 1) { }")
    assert "esperado um identificador" in e.message and (e.line, e.column) == (1, 6)


def test_for_sem_condicao():
    e = erro("for (i = 0; ; i = i + 1) { }")
    assert "esperada uma expressão" in e.message and (e.line, e.column) == (1, 13)


def test_for_com_clausulas_vazias():
    erro("for (;;) { }")


def test_for_com_atualizacao_que_nao_e_atribuicao():
    e = erro("for (i = 0; i < 3; i + 1) { }")
    assert "esperado '=' na atribuição" in e.message


def test_for_com_ponto_e_virgula_sobrando():
    e = erro("for (i = 0; i < 3; i = i + 1;) { }")
    assert "esperado ')' após a atualização do 'for'" in e.message


def test_for_sem_parenteses():
    assert "esperado '(' após 'for'" in erro("for i = 0; i < 3; i = i + 1 { }").message


def test_for_sem_fechar_parenteses():
    assert "esperado ')'" in erro("for (i = 0; i < 3; i = i + 1 { }").message


def test_for_sem_corpo_em_bloco():
    assert "esperado '{'" in erro("for (i = 0; i < 3; i = i + 1) print(i);").message


# --------------------------------------------------------------------------
# while mal formado
# --------------------------------------------------------------------------
def test_while_sem_condicao():
    assert "esperada uma expressão" in erro("while () { }").message


def test_while_sem_parenteses():
    assert "esperado '(' após 'while'" in erro("while x > 0 { }").message


def test_while_sem_bloco():
    assert "esperado '{'" in erro("while (x > 0) x = x - 1;").message


def test_while_com_bloco_nao_fechado():
    e = erro("while (true) { x = 1;")
    assert "esperado '}'" in e.message and "fim do arquivo" in e.message


# --------------------------------------------------------------------------
# Expressoes
# --------------------------------------------------------------------------
def test_expressao_incompleta_exemplo_3_do_gramatica_md():
    e = erro("x = (1 + ;")
    assert "esperada uma expressão, encontrado ';'" in e.message
    assert (e.line, e.column) == (1, 10)


def test_parentese_nao_fechado():
    assert "esperado ')' para fechar a expressão" in erro("x = (1 + 2;").message


def test_operador_binario_sem_operando():
    assert "esperada uma expressão" in erro("x = * 3;").message
    assert "esperada uma expressão" in erro("x = 3 *;").message


@pytest.mark.parametrize("fonte", ["x = 1 < 2 < 3;", "x = a <= b >= c;", "x = a < b > c;"])
def test_relacionais_nao_sao_associativos(fonte):
    assert "não são associativos" in erro(fonte).message


# --------------------------------------------------------------------------
# Comandos
# --------------------------------------------------------------------------
def test_atribuicao_sem_ponto_e_virgula_no_fim_da_entrada():
    e = erro("x = 1")
    assert "esperado ';' após a atribuição" in e.message and "fim do arquivo" in e.message


def test_atribuicao_encadeada_nao_existe():
    assert "esperado ';' após a atribuição" in erro("x = y = 1;").message


def test_print_sem_ponto_e_virgula():
    assert "esperado ';' após o 'print'" in erro("print(1)").message


def test_print_sem_parenteses():
    assert "esperado '(' após 'print'" in erro("print 1;").message


def test_expressao_solta_nao_e_comando():
    assert "esperado um comando, encontrado '1'" in erro("1 + 2;").message


def test_chave_fechando_sem_abrir():
    assert "esperado um comando, encontrado '}'" in erro("x = 1; }").message


def test_if_sem_parenteses():
    assert "esperado '(' após 'if'" in erro("if x { }").message


def test_if_sem_bloco():
    assert "esperado '{'" in erro("if (x) print(x);").message


def test_else_solto():
    assert "esperado um comando, encontrado 'else'" in erro("else { }").message


def test_else_duplicado():
    erro("if (a) { } else { } else { }")


def test_else_if_nao_existe_na_minilang():
    # a gramatica e `[ "else" bloco ]`: depois de else vem sempre '{'
    assert "esperado '{'" in erro("if (a) { } else if (b) { }").message


# --------------------------------------------------------------------------
# Propriedades gerais
# --------------------------------------------------------------------------
def test_parser_para_no_primeiro_erro():
    e = erro("x = ; y = ;")
    assert (e.line, e.column) == (1, 5)


def test_parse_error_tem_posicao_e_token():
    e = erro("x = 1;\ny = ;")
    assert (e.line, e.column) == (2, 5)
    assert e.token.lexeme == ";"


def test_programa_invalido_do_repositorio():
    fonte = (RAIZ / "exemplos" / "programa_invalido.ml").read_text(encoding="utf-8")
    e = erro(fonte)
    assert "atualização é obrigatória" in e.message
    assert e.line == 6


def test_erro_lexico_atravessa_o_parser_como_lexicalerror():
    with pytest.raises(LexicalError):
        parse("x = 3 @ 2;")
