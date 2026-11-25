"""Teste de seguranca para laço infinito (etapa G).

RESULTADO ESPERADO:
- a execucao e interrompida ao ultrapassar o limite configurado;
- o teste termina sem deixar a suite presa em um laço infinito;
- o corpo executa exatamente o numero maximo de vezes permitido.
"""

import pytest

from src.interpreter import Interpretador, LimiteDeIteracoes
from src.parser import parse


def test_laco_infinito_e_interrompido_pelo_limite_de_iteracoes():
    max_iteracoes = 5
    fonte = (
        "i = 0;\n"
        "while (true) {\n"
        "    print(i);\n"
        "    i = i + 1;\n"
        "}"
    )
    interpretador = Interpretador(max_iteracoes=max_iteracoes)

    with pytest.raises(LimiteDeIteracoes, match="limite de 5 iterações excedido"):
        interpretador.executar(parse(fonte))

    # A sexta tentativa e bloqueada antes de executar o corpo novamente.
    assert interpretador.saida == ["0", "1", "2", "3", "4"]
    assert interpretador.tabela.valores() == {"i": max_iteracoes}


def test_for_infinito_tambem_e_interrompido_pelo_limite():
    max_iteracoes = 4
    fonte = (
        "for (i = 0; true; i = i + 1) {\n"
        "    print(i);\n"
        "}"
    )
    interpretador = Interpretador(max_iteracoes=max_iteracoes)

    with pytest.raises(LimiteDeIteracoes, match="limite de 4 iterações excedido"):
        interpretador.executar(parse(fonte))

    assert interpretador.saida == ["0", "1", "2", "3"]
    # A atualização da quarta volta ocorre; a quinta é bloqueada antes do corpo.
    assert interpretador.tabela.valores() == {"i": max_iteracoes}


def test_laco_finito_que_atinge_exatamente_o_limite_termina_normalmente():
    max_iteracoes = 5
    fonte = (
        "i = 0;\n"
        "while (i < 5) {\n"
        "    print(i);\n"
        "    i = i + 1;\n"
        "}"
    )
    interpretador = Interpretador(max_iteracoes=max_iteracoes)

    interpretador.executar(parse(fonte))

    assert interpretador.saida == ["0", "1", "2", "3", "4"]
    assert interpretador.tabela.valores() == {"i": max_iteracoes}


def test_limite_de_iteracoes_e_compartilhado_entre_lacos_aninhados():
    max_iteracoes = 5
    fonte = (
        "i = 0;\n"
        "while (i < 2) {\n"
        "    j = 0;\n"
        "    while (j < 2) {\n"
        "        print(i * 10 + j);\n"
        "        j = j + 1;\n"
        "    }\n"
        "    i = i + 1;\n"
        "}"
    )
    interpretador = Interpretador(max_iteracoes=max_iteracoes)

    with pytest.raises(LimiteDeIteracoes, match="limite de 5 iterações excedido"):
        interpretador.executar(parse(fonte))

    # As cinco primeiras entradas no laço são contadas globalmente:
    # while externo (1), interno (2), interno (3), externo (4), interno (5).
    # A próxima entrada no laço interno excede o limite antes do corpo.
    assert interpretador.saida == ["0", "1", "10"]
    assert interpretador.tabela.valores() == {"i": 1, "j": 1}
