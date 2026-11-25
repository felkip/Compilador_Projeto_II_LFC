# RESULTADO ESPERADO (categoria: erro LEXICO): tokenize() levanta LexicalError
#   @              -> "caractere nao permitido"
#   1x             -> "numero malformado: digito seguido de letra"
#   !  (isolado)   -> "'!' isolado; esperado '=' para formar '!='"
#   /* sem fechar  -> "comentario de bloco nao fechado"
# O lexer acumula todos os erros e so levanta a excecao no fim da leitura.
"""Testes de entradas léxicas inválidas da MiniLang."""
import pytest

from src.lexer import LexicalError, tokenize


def test_caractere_nao_permitido():
    with pytest.raises(LexicalError, match="caractere não permitido"):
        tokenize("x = 2 @ 3;")


def test_numero_iniciado_corretamente_mas_seguido_de_letra():
    with pytest.raises(LexicalError, match="número malformado"):
        tokenize("x = 1x + 2;")


def test_comentario_de_bloco_nao_fechado():
    with pytest.raises(LexicalError, match="comentário de bloco não fechado"):
        tokenize("x = 1; /* comentário sem fechamento")


def test_exclamação_isolada_e_invalida():
    with pytest.raises(LexicalError, match="'!' isolado"):
        tokenize("x ! 2;")


def test_acumula_mais_de_um_erro_lexico():
    with pytest.raises(LexicalError) as error:
        tokenize("x = @; y = 1x;")
    assert len(error.value.issues) == 2
