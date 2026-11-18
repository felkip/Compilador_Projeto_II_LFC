"""Execucao de programas validos (item e): interpretador e tabela de simbolos.

RESULTADO ESPERADO: todo programa abaixo executa ate o fim, sem erro, e o que
ele imprime (lista de textos em Interpretador.saida) e exatamente o indicado.
Cobre: precedencia e associatividade na avaliacao, divisao truncada em direcao
a zero, comparacoes, booleanos, variaveis, if/else, blocos, while e for, e a
tabela de simbolos. Programas que violam S1 a S6 ficam em
tests/invalidos/test_interpreter_invalido.py.
"""
import contextlib
import io
import tempfile
from pathlib import Path

import pytest

from src.interpreter import (Interpretador, TabelaSimbolos, formatar,
                             interpretar, main, tipo_de)
from src.parser import parse

RAIZ = Path(__file__).resolve().parents[2]


def rodar(fonte):
    """Executa o texto e devolve o objeto Interpretador (saida e tabela)."""
    interpretador = Interpretador(max_iteracoes=10_000)
    interpretador.executar(parse(fonte))
    return interpretador


def saida(fonte):
    return rodar(fonte).saida


# ----------------------------------------------------------- programa do projeto

def test_programa_valido_do_projeto():
    fonte = (RAIZ / "exemplos" / "programa_valido.ml").read_text(encoding="utf-8")
    esperado = ["30"] + [str(n) for n in range(10, 0, -1)] + ["0", "true", "-3"]
    assert saida(fonte) == esperado


def test_main_executa_o_programa_valido_com_codigo_zero():
    caminho = RAIZ / "exemplos" / "programa_valido.ml"
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        codigo = main([str(caminho)])
    assert codigo == 0
    assert err.getvalue() == ""
    assert out.getvalue().split() == saida(caminho.read_text(encoding="utf-8"))


# --------------------------------------------------------------- expressoes

@pytest.mark.parametrize("expressao, esperado", [
    ("2 + 3 * 4", "14"),            # * antes de +
    ("(2 + 3) * 4", "20"),          # parenteses mudam a ordem
    ("2 * 3 + 4 * 5", "26"),
    ("10 - 2 * 3 + 1", "5"),
    ("(1 + 2) * (3 + 4)", "21"),
    ("10 - 3 - 2", "5"),            # - associa a esquerda: (10 - 3) - 2
    ("100 / 10 / 5", "2"),          # / associa a esquerda: (100 / 10) / 5
    ("- -5", "5"),                  # menos unario, recursao a direita
    ("-2 * 3", "-6"),               # unario antes de *
    ("2 - -3", "5"),
    ("1 + 2 < 4", "true"),          # aritmetica antes de comparacao
    ("3 > 1 == true", "true"),      # comparacao antes de igualdade
    ("1 < 2 == 2 < 3", "true"),
])
def test_precedencia_e_associatividade(expressao, esperado):
    assert saida(f"print({expressao});") == [esperado]


@pytest.mark.parametrize("a, b, esperado", [
    (7, 2, 3), (-7, 2, -3), (7, -2, -3), (-7, -2, 3),   # trunca em direcao a zero
    (0, 5, 0), (0, -5, 0), (1, 3, 0), (-1, 3, 0),
])
def test_divisao_inteira_trunca_em_direcao_a_zero(a, b, esperado):
    assert saida(f"print({a} / {b});") == [str(esperado)]


def test_divisao_de_inteiros_grandes_e_exata():
    # com float, int(a / b) erraria; aqui a conta e feita so com inteiros
    assert saida("print(100000000000 * 100000000000 / 3);") == [str(10**22 // 3)]


@pytest.mark.parametrize("expressao, esperado", [
    ("1 < 2", "true"), ("2 < 1", "false"),
    ("2 > 1", "true"), ("1 > 2", "false"),
    ("2 <= 2", "true"), ("3 <= 2", "false"),
    ("2 >= 2", "true"), ("1 >= 2", "false"),
    ("3 == 3", "true"), ("3 == 4", "false"),
    ("3 != 4", "true"), ("3 != 3", "false"),
    ("true == true", "true"), ("true == false", "false"),
    ("true != false", "true"), ("false != false", "false"),
])
def test_comparacoes_e_igualdade(expressao, esperado):
    assert saida(f"print({expressao});") == [esperado]


def test_print_de_booleano_e_de_inteiro_negativo():
    assert saida("print(true);\nprint(false);\nprint(-4);\nprint(007);") == ["true", "false", "-4", "7"]


# ----------------------------------------------------------------- variaveis

def test_atribuicao_e_reatribuicao_do_mesmo_tipo():
    interpretador = rodar("x = 5;\ny = x * 2;\nx = x + 1;\nprint(x);\nprint(y);")
    assert interpretador.saida == ["6", "10"]
    assert interpretador.tabela.valores() == {"x": 6, "y": 10}


def test_variavel_booleana_pode_receber_outro_booleano():
    interpretador = rodar("b = 1 < 2;\nprint(b);\nb = false;\nprint(b);")
    assert interpretador.saida == ["true", "false"]
    assert interpretador.tabela.valores() == {"b": False}


def test_comentarios_sao_ignorados():
    fonte = "// comentario\nx = 1; /* bloco\ncom varias linhas */ print(x); // fim"
    assert saida(fonte) == ["1"]


# ------------------------------------------------------ if, blocos e escopo unico

def test_if_executa_o_ramo_verdadeiro():
    assert saida("x = 3;\nif (x > 2) { print(1); } else { print(2); }") == ["1"]


def test_if_executa_o_else_quando_a_condicao_e_falsa():
    assert saida("x = 1;\nif (x > 2) { print(1); } else { print(2); }") == ["2"]


def test_if_sem_else_e_condicao_falsa_nao_faz_nada():
    assert saida("if (false) { print(1); }") == []
    assert saida("if (true) { }") == []


def test_bloco_solto_e_escopo_unico():
    # nao ha escopo aninhado: a variavel criada no bloco continua existindo
    assert saida("{ x = 1; }\nprint(x);") == ["1"]


def test_ramo_que_nao_executa_nao_e_verificado():
    # a verificacao semantica acontece na execucao: y nunca e lida aqui
    assert saida("if (false) { print(y); }") == []
    assert saida("x = 1;\nwhile (x > 5) { print(z); }") == []


# ---------------------------------------------------------------- while e for

def test_while_executa_n_vezes():
    assert saida("x = 3;\nwhile (x > 0) { print(x); x = x - 1; }") == ["3", "2", "1"]


def test_while_com_condicao_falsa_na_entrada_nao_executa():
    assert saida("x = 0;\nwhile (x > 0) { print(x); }") == []


def test_for_soma_e_atualizacao_depois_do_corpo():
    fonte = "soma = 0;\nfor (i = 0; i < 5; i = i + 1) { soma = soma + i; }\nprint(soma);"
    assert saida(fonte) == ["10"]
    assert saida("for (i = 0; i < 3; i = i + 1) { print(i); }") == ["0", "1", "2"]


def test_for_passo_dois_e_variavel_de_controle_continua_existindo():
    interpretador = rodar("for (i = 0; i < 6; i = i + 2) { print(i); }")
    assert interpretador.saida == ["0", "2", "4"]
    assert interpretador.tabela.valores() == {"i": 6}


def test_for_com_condicao_falsa_executa_so_a_inicializacao():
    interpretador = rodar("for (i = 5; i < 3; i = i + 1) { print(i); }")
    assert interpretador.saida == []
    assert interpretador.tabela.valores() == {"i": 5}


def test_for_que_altera_a_variavel_de_controle_no_corpo():
    fonte = "for (i = 0; i < 10; i = i + 1) { i = i + 4; print(i); }"
    assert saida(fonte) == ["4", "9"]


def test_lacos_aninhados():
    fonte = ("for (i = 0; i < 2; i = i + 1) {\n"
             "  for (j = 0; j < 2; j = j + 1) { print(i * 10 + j); }\n"
             "}")
    assert saida(fonte) == ["0", "1", "10", "11"]


# --------------------------------------------------------- tabela de simbolos

def test_tabela_insere_e_busca():
    tabela = TabelaSimbolos()
    assert not tabela.existe("x") and len(tabela) == 0
    tabela.atribuir("x", 7, linha=3)
    simbolo = tabela.buscar("x", linha=4)
    assert (simbolo.tipo, simbolo.valor, simbolo.linha_criacao) == ("int", 7, 3)
    assert tabela.existe("x") and len(tabela) == 1


def test_tabela_atualiza_valor_e_guarda_a_linha_de_criacao():
    tabela = TabelaSimbolos()
    tabela.atribuir("x", 1, linha=1)
    tabela.atribuir("x", 2, linha=9)
    simbolo = tabela.buscar("x", linha=10)
    assert simbolo.valor == 2 and simbolo.linha_criacao == 1


def test_tipo_de_distingue_bool_de_int():
    # em Python, isinstance(True, int) e True: o teste olha o tipo exato
    assert tipo_de(True) == "bool" and tipo_de(False) == "bool"
    assert tipo_de(1) == "int" and tipo_de(0) == "int"
    assert formatar(True) == "true" and formatar(False) == "false" and formatar(-3) == "-3"


# ------------------------------------------------------- uso do interpretador

def test_executar_reinicia_o_estado():
    interpretador = Interpretador()
    interpretador.executar(parse("x = 1;\nprint(x);"))
    interpretador.executar(parse("print(2);"))
    assert interpretador.saida == ["2"]
    assert len(interpretador.tabela) == 0


def test_ao_imprimir_recebe_cada_linha_na_ordem():
    recebidas = []
    interpretador = Interpretador(ao_imprimir=recebidas.append)
    interpretador.executar(parse("print(1);\nprint(true);"))
    assert recebidas == ["1", "true"] == interpretador.saida


def test_interpretar_aceita_texto_direto():
    assert interpretar("print(1 + 1);") == ["2"]


def test_main_le_arquivo_temporario():
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "p.ml"
        caminho.write_text("print(2 * 21);", encoding="utf-8")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            codigo = main([str(caminho)])
    assert codigo == 0 and out.getvalue().split() == ["42"]
