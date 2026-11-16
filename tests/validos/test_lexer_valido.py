"""Testes de entradas léxicas válidas da MiniLang."""
from src.lexer import tokenize


def test_reconhece_palavras_reservadas_e_identificadores():
    tokens = tokenize("if else while for print true false while1 _valor")
    assert [t.type for t in tokens] == [
        "IF", "ELSE", "WHILE", "FOR", "PRINT", "TRUE", "FALSE", "ID", "ID", "EOF"
    ]
    assert tokens[7].lexeme == "while1"
    assert tokens[8].lexeme == "_valor"


def test_reconhece_inteiros_operadores_e_delimitadores():
    tokens = tokenize("x = 42 + 3 * (10 - 2); a <= b != false;")
    assert [t.type for t in tokens] == [
        "ID", "ATRIB", "INT", "MAIS", "INT", "MULT", "ABRE_PAR", "INT",
        "MENOS", "INT", "FECHA_PAR", "PONTO_VIRGULA", "ID", "MENOR_IGUAL",
        "ID", "DIFERENTE", "FALSE", "PONTO_VIRGULA", "EOF"
    ]
    assert tokens[2].literal == 42
    assert tokens[16].literal is False


def test_descarta_comentarios_de_linha_e_de_bloco():
    tokens = tokenize("x = 1; // comentário de linha\n/* bloco\ncomentado */ print(x);")
    assert [t.type for t in tokens] == [
        "ID", "ATRIB", "INT", "PONTO_VIRGULA", "PRINT", "ABRE_PAR",
        "ID", "FECHA_PAR", "PONTO_VIRGULA", "EOF"
    ]


def test_operador_divisao_nao_e_confundido_com_comentario():
    tokens = tokenize("resultado = 8 / 2;")
    assert any(t.type == "DIV" for t in tokens)


def test_registra_linha_e_coluna_dos_tokens():
    tokens = tokenize("x = 1;\n  print(x);")
    print_token = next(token for token in tokens if token.type == "PRINT")
    assert (print_token.line, print_token.column) == (2, 3)


def test_programa_valido_completo_e_lexicamente_reconhecido():
    from pathlib import Path

    source = Path("exemplos/programa_valido.ml").read_text(encoding="utf-8")
    tokens = tokenize(source)
    assert tokens[-1].type == "EOF"
    assert {"WHILE", "FOR", "IF", "ELSE", "PRINT"}.issubset(
        {token.type for token in tokens}
    )


def test_programa_sintaticamente_invalido_ainda_pode_ser_lexicamente_valido():
    from pathlib import Path

    source = Path("exemplos/programa_invalido.ml").read_text(encoding="utf-8")
    tokens = tokenize(source)
    assert tokens[-1].type == "EOF"
    assert any(token.type == "FOR" for token in tokens)
