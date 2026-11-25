# RESULTADO ESPERADO: cada programa de exemplos/erros/ é executado pela linha de
# comando (src.interpreter.main) e deve terminar com o código de saída da sua
# fase e com o diagnóstico indicado (item f; transcrito em docs/execucao_erros.txt):
#   lexico_*     -> código 1, "erro léxico: ..."
#   sintatico_*  -> código 2, "erro sintático: ..."
#   semantico_*  -> código 3, "erro semântico: [Sx] ..."
# Programas com erro léxico ou sintático não imprimem nada (nada é executado).
from pathlib import Path

import pytest

from src.interpreter import main

PASTA = Path(__file__).resolve().parents[2] / "exemplos" / "erros"

CASOS = [
    # (arquivo, código, trecho do diagnóstico em stderr, stdout esperado)
    ("lexico_1_caractere_invalido.ml", 1, "caractere não permitido em 2:7", ""),
    ("lexico_2_numero_malformado.ml", 1, "número malformado: dígito seguido de letra em 2:5", ""),
    ("lexico_3_comentario_aberto.ml", 1, "comentário de bloco não fechado; esperado '*/' em 3:1", ""),
    ("sintatico_1_for_sem_atualizacao.ml", 2, "a cláusula de atualização é obrigatória), encontrado ')' em 2:19", ""),
    ("sintatico_2_expressao_incompleta.ml", 2, "esperada uma expressão, encontrado ';' em 2:10", ""),
    ("sintatico_3_ponto_virgula_ausente.ml", 2, "esperado ';' após a atribuição, encontrado 'print' em 3:1", ""),
    ("semantico_1_while_nao_booleano.ml", 3, "[S4] a condição do 'while' deve ser booleana, mas é int (linha 3)", ""),
    ("semantico_2_for_variavel_indefinida.ml", 3, "[S1] variável 'j' não definida (linha 2)", ""),
    ("semantico_3_divisao_por_zero.ml", 3, "[S6] divisão por zero (linha 3)", "1\n"),
    ("semantico_4_tipo_incompativel.ml", 3, "[S2] o operador '+' exige operandos int", ""),
]


@pytest.mark.parametrize("arquivo, codigo, diagnostico, saida", CASOS)
def test_exemplo_de_erro(arquivo, codigo, diagnostico, saida, capsys):
    assert main([str(PASTA / arquivo)]) == codigo
    capturado = capsys.readouterr()
    assert diagnostico in capturado.err
    assert capturado.out == saida


def test_ha_pelo_menos_tres_exemplos_por_categoria():
    for prefixo in ("lexico_", "sintatico_", "semantico_"):
        assert len(list(PASTA.glob(prefixo + "*.ml"))) >= 3
