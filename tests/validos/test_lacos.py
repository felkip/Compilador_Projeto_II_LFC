"""Testes de casos validos e de borda para os laços while e for (etapa G).

RESULTADO ESPERADO:
- while com condicao falsa na entrada: o corpo nao executa;
- while cuja condicao fica falsa apos a primeira volta: executa uma vez;
- while com contador: executa N vezes, na ordem esperada;
- for cuja atualizacao incrementa a variavel de controle em mais de uma unidade:
  a variavel e atualizada ao final de cada volta e o laco termina corretamente.
"""

from src.interpreter import Interpretador
from src.parser import parse


def rodar(fonte, max_iteracoes=100):
    """Executa um programa MiniLang e devolve o interpretador para inspecao."""
    interpretador = Interpretador(max_iteracoes=max_iteracoes)
    interpretador.executar(parse(fonte))
    return interpretador


def test_while_com_condicao_falsa_na_entrada_nao_executa():
    interpretador = rodar(
        "x = 0;\n"
        "while (x > 0) {\n"
        "    print(x);\n"
        "    x = x + 1;\n"
        "}"
    )

    assert interpretador.saida == []
    assert interpretador.tabela.valores() == {"x": 0}


def test_while_que_executa_exatamente_uma_vez():
    interpretador = rodar(
        "x = 0;\n"
        "while (x < 1) {\n"
        "    print(x);\n"
        "    x = x + 1;\n"
        "}"
    )

    assert interpretador.saida == ["0"]
    assert interpretador.tabela.valores() == {"x": 1}


def test_while_que_executa_n_vezes():
    interpretador = rodar(
        "contador = 0;\n"
        "while (contador < 5) {\n"
        "    print(contador);\n"
        "    contador = contador + 1;\n"
        "}"
    )

    assert interpretador.saida == ["0", "1", "2", "3", "4"]
    assert interpretador.tabela.valores() == {"contador": 5}


def test_for_atualiza_a_variavel_de_controle_com_passo_maior_que_um():
    interpretador = rodar(
        "for (i = 1; i <= 7; i = i + 3) {\n"
        "    print(i);\n"
        "}"
    )

    # A atualizacao ocorre depois do corpo: 1 -> 4 -> 7 -> 10.
    assert interpretador.saida == ["1", "4", "7"]
    assert interpretador.tabela.valores() == {"i": 10}
