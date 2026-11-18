# RESULTADO ESPERADO (categoria: erro SEMANTICO)
#   Todo programa abaixo e lexica e sintaticamente valido (o parser o aceita),
#   mas viola uma restricao semantica de docs/gramatica.md. O interpretador
#   levanta ErroSemantico com o CODIGO da restricao e a LINHA do erro, e para na
#   PRIMEIRA violacao (o que ja foi impresso continua em Interpretador.saida).
#     S1  variavel nao definida .......... x = y + 1;   /   for (i = 0; j < 3; i = i + 1)
#     S2  operando que nao e int ......... 1 + true     /   -true   /   true < false
#     S3  == ou != com tipos diferentes .. 1 == true
#     S4  condicao que nao e booleana .... while (5)    /   if (1)  /   for (i = 0; i; ...)
#     S5  variavel muda de tipo .......... x = 1; x = true;
#     S6  divisao por zero ............... 1 / 0
#   Tambem: o limite de 10.000 bits dos inteiros levanta InteiroGrandeDemais, que
#   e uma trava de execucao (LimiteDeExecucao) e NAO um ErroSemantico.
#   Limite de iteracoes (laco infinito) esta em test_laco_infinito.py.
#   O comando `python -m src.interpreter arquivo.ml` sai com codigo 1 (lexico),
#   2 (sintatico), 3 (semantico), 4 (trava de execucao) ou 5 (arquivo ilegivel).
import contextlib
import io
import tempfile
from pathlib import Path

import pytest

from src.interpreter import (ErroSemantico, Interpretador, InteiroGrandeDemais,
                             LimiteDeExecucao, main)
from src.parser import parse


def executar(fonte, max_iteracoes=10_000):
    interpretador = Interpretador(max_iteracoes=max_iteracoes)
    interpretador.executar(parse(fonte))
    return interpretador


def rejeita(fonte):
    """Executa e devolve o ErroSemantico levantado (falha se nao houver)."""
    with pytest.raises(ErroSemantico) as info:
        executar(fonte)
    return info.value


# ------------------------------------------------------------ S1: nao definida

@pytest.mark.parametrize("fonte", [
    "print(y);",
    "x = y + 1;",
    "x = x + 1;",                                   # x so existe depois da atribuicao
    "while (z < 3) { z = z + 1; }",                 # condicao usa variavel inexistente
    "for (i = 0; j < 3; i = i + 1) { print(i); }",  # variavel de controle da condicao
    "for (i = 0; i < 3; k = k + 1) { print(i); }",  # k so aparece lido na atualizacao
])
def test_s1_variavel_nao_definida(fonte):
    assert rejeita(fonte).codigo == "S1"


def test_s1_mensagem_e_linha():
    erro = rejeita("x = 1;\ny = 2;\nprint(z);")
    assert erro.codigo == "S1" and erro.linha == 3
    assert "variável 'z' não definida" in erro.mensagem


def test_s1_variavel_de_controle_nao_definida_no_for():
    erro = rejeita("x = 3;\nfor (i = 0; j < 3; i = i + 1) { print(i); }")
    assert erro.codigo == "S1" and erro.linha == 2
    assert "variável 'j' não definida" in erro.mensagem


# ----------------------------------------------------------- S2: operando int

@pytest.mark.parametrize("fonte", [
    "print(1 + true);",
    "print(true * 2);",
    "print(true - false);",
    "print(true / 1);",
    "print(-true);",
    "print(true < false);",
    "print(1 < true);",
    "print(true >= 1);",
])
def test_s2_operando_que_nao_e_int(fonte):
    assert rejeita(fonte).codigo == "S2"


def test_s2_mensagem_e_linha():
    erro = rejeita("x = 1;\nprint(1 + true);")
    assert erro.codigo == "S2" and erro.linha == 2
    assert "o operador '+' exige operandos int, mas recebeu int e bool" in erro.mensagem


# ------------------------------------------------------------ S3: ==/!= tipos

@pytest.mark.parametrize("fonte", ["print(1 == true);", "print(true != 1);", "print(0 == false);"])
def test_s3_igualdade_com_tipos_diferentes(fonte):
    assert rejeita(fonte).codigo == "S3"


def test_s3_mensagem():
    erro = rejeita("print(1 == true);")
    assert "'==' exige operandos do mesmo tipo, mas recebeu int e bool" in erro.mensagem


# ------------------------------------------------- S4: condicao nao booleana

@pytest.mark.parametrize("fonte", [
    "while (5) { }",
    "if (1) { }",
    "if (1 + 2) { print(1); }",
    "for (i = 0; i; i = i + 1) { }",
    "x = 3;\nwhile (x) { x = x - 1; }",             # exemplo 5 de docs/gramatica.md
])
def test_s4_condicao_nao_booleana(fonte):
    assert rejeita(fonte).codigo == "S4"


def test_s4_mensagem_do_while():
    erro = rejeita("x = 3;\nwhile (x) { x = x - 1; }")
    assert erro.codigo == "S4" and erro.linha == 2
    assert "a condição do 'while' deve ser booleana, mas é int" in erro.mensagem


def test_s4_condicao_do_for_nao_booleana():
    erro = rejeita("for (i = 0; i + 1; i = i + 1) { }")
    assert "a condição do 'for' deve ser booleana, mas é int" in erro.mensagem


# --------------------------------------------------------- S5: tipo da variavel

@pytest.mark.parametrize("fonte", [
    "x = 1;\nx = true;",
    "b = false;\nb = 1;",
    "x = 1;\nwhile (x < 3) { x = x < 5; }",         # troca de tipo dentro do laco
])
def test_s5_variavel_nao_muda_de_tipo(fonte):
    assert rejeita(fonte).codigo == "S5"


def test_s5_mensagem_cita_a_linha_de_criacao():
    erro = rejeita("x = 1;\nprint(x);\nx = true;")
    assert erro.linha == 3
    assert "foi criada como int na linha 1" in erro.mensagem


# ------------------------------------------------------ S6: divisao por zero

@pytest.mark.parametrize("fonte", [
    "print(1 / 0);",
    "x = 0;\nprint(5 / x);",
    "print(1 / (2 - 2));",
    "print(0 / 0);",
])
def test_s6_divisao_por_zero(fonte):
    erro = rejeita(fonte)
    assert erro.codigo == "S6" and "divisão por zero" in erro.mensagem


# ---------------------------------------------------- para na primeira violacao

def test_saida_anterior_ao_erro_e_preservada_e_nada_roda_depois():
    interpretador = Interpretador()
    with pytest.raises(ErroSemantico):
        interpretador.executar(parse("print(1);\nprint(2 / 0);\nprint(3);"))
    assert interpretador.saida == ["1"]


def test_primeira_violacao_vence():
    # a condicao 'x' (S4) aparece antes do 'j' nao definido (S1)
    fonte = ("x = 3;\nwhile (x) { x = x - 1; }\n"
             "for (i = 0; j < 3; i = i + 1) { print(i); }")
    assert rejeita(fonte).codigo == "S4"


def test_ordem_de_avaliacao_em_operacao_binaria():
    # os dois lados sao avaliados antes da checagem de tipos: S1 vem antes de S2
    assert rejeita("print(y + true);").codigo == "S1"
    # e a checagem de tipos vem antes da divisao por zero
    assert rejeita("print(true / 0);").codigo == "S2"


# ------------------------------------------- travas de execucao (nao semanticas)

def test_inteiro_grande_demais_e_trava_de_execucao():
    with pytest.raises(InteiroGrandeDemais) as info:
        executar("x = 2;\nwhile (true) { x = x * x; }")
    assert isinstance(info.value, LimiteDeExecucao)
    assert not isinstance(info.value, ErroSemantico)


# ------------------------------------------------------------ codigos do main

def rodar_main(fonte, *extra):
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "p.ml"
        caminho.write_text(fonte, encoding="utf-8")
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            codigo = main([str(caminho), *extra])
    return codigo, out.getvalue(), err.getvalue()


def test_main_erro_lexico_codigo_1_e_mostra_todos_os_erros():
    codigo, _, err = rodar_main("a = 1 @ 2;\nb = 1x;")
    assert codigo == 1
    assert "erro léxico" in err and "'@'" in err and "'1x'" in err


def test_main_erro_sintatico_codigo_2():
    codigo, _, err = rodar_main("for (i = 0; i < 10) { print(i); }")
    assert codigo == 2 and "erro sintático" in err


def test_main_erro_semantico_codigo_3_mantem_a_saida_anterior():
    codigo, out, err = rodar_main("print(1);\nprint(y);")
    assert codigo == 3 and out.split() == ["1"] and "[S1]" in err


def test_main_trava_de_execucao_codigo_4():
    codigo, _, err = rodar_main("while (true) { }", "--max-iteracoes", "50")
    assert codigo == 4 and "limite de 50 iterações" in err


def test_main_arquivo_inexistente_codigo_5():
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        codigo = main(["arquivo_que_nao_existe.ml"])
    assert codigo == 5 and "não foi possível ler" in err.getvalue()
