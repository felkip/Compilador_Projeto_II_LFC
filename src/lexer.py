"""Analisador léxico da MiniLang.

O lexer transforma o código-fonte em uma sequência de tokens. Espaços em
branco e comentários são descartados. Erros léxicos são acumulados para que
mais de um problema possa ser apresentado na mesma execução.
"""

from dataclasses import dataclass
from typing import Any, List


@dataclass(frozen=True)
class Token:
    """Unidade léxica produzida pelo analisador."""

    type: str
    lexeme: str
    line: int
    column: int
    literal: Any = None

    def __repr__(self) -> str:
        return (
            f"Token(type={self.type!r}, lexeme={self.lexeme!r}, "
            f"line={self.line}, column={self.column}, literal={self.literal!r})"
        )


@dataclass(frozen=True)
class LexicalIssue:
    message: str
    lexeme: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.message} em {self.line}:{self.column} ({self.lexeme!r})"


class LexicalError(Exception):
    """Exceção contendo um ou mais erros encontrados durante a análise."""

    def __init__(self, issues: List[LexicalIssue]):
        self.issues = issues
        super().__init__("\n".join(str(issue) for issue in issues))


class Lexer:
    KEYWORDS = {
        "if": "IF",
        "else": "ELSE",
        "while": "WHILE",
        "for": "FOR",
        "print": "PRINT",
        "true": "TRUE",
        "false": "FALSE",
    }

    TWO_CHAR_TOKENS = {
        "<=": "MENOR_IGUAL",
        ">=": "MAIOR_IGUAL",
        "==": "IGUAL",
        "!=": "DIFERENTE",
    }

    ONE_CHAR_TOKENS = {
        "+": "MAIS",
        "-": "MENOS",
        "*": "MULT",
        "/": "DIV",
        "<": "MENOR",
        ">": "MAIOR",
        "=": "ATRIB",
        "(": "ABRE_PAR",
        ")": "FECHA_PAR",
        "{": "ABRE_CHAVE",
        "}": "FECHA_CHAVE",
        ";": "PONTO_VIRGULA",
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.issues: List[LexicalIssue] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1

    def tokenize(self) -> List[Token]:
        """Analisa toda a entrada e devolve tokens terminados por EOF."""
        while not self._is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self._scan_token()

        if self.issues:
            raise LexicalError(self.issues)

        self.tokens.append(Token("EOF", "", self.line, self.column))
        return self.tokens

    def _scan_token(self) -> None:
        char = self._advance()

        if char in " \t\r\n":
            return

        if char.isascii() and char.isdigit():
            self._number()
            return

        if self._is_letter(char):
            self._identifier()
            return

        # Comentários e operador de divisão compartilham o prefixo '/'.
        if char == "/" and self._match("/"):
            self._line_comment()
            return
        if char == "/" and self._match("*"):
            self._block_comment()
            return

        if self.current < len(self.source):
            pair = char + self.source[self.current]
            if pair in self.TWO_CHAR_TOKENS:
                self._advance()
                self._add_token(self.TWO_CHAR_TOKENS[pair])
                return

        if char == "!":
            self._error("'!' isolado; esperado '=' para formar '!='", char)
            return

        token_type = self.ONE_CHAR_TOKENS.get(char)
        if token_type:
            self._add_token(token_type)
            return

        self._error("caractere não permitido", char)

    def _number(self) -> None:
        while self._peek().isascii() and self._peek().isdigit():
            self._advance()

        # A especificação não permite identificadores iniciados por dígitos.
        # '1x' é tratado como um único lexema malformado, não como INT + ID.
        if self._is_letter(self._peek()):
            while self._is_alphanumeric(self._peek()):
                self._advance()
            self._error("número malformado: dígito seguido de letra", self._current_lexeme())
            return

        lexeme = self._current_lexeme()
        self._add_token("INT", int(lexeme))

    def _identifier(self) -> None:
        while self._is_alphanumeric(self._peek()):
            self._advance()

        lexeme = self._current_lexeme()
        token_type = self.KEYWORDS.get(lexeme, "ID")
        literal = True if token_type == "TRUE" else False if token_type == "FALSE" else None
        self._add_token(token_type, literal)

    def _line_comment(self) -> None:
        while not self._is_at_end() and self._peek() != "\n":
            self._advance()
        # A quebra de linha será consumida como espaço em branco na próxima
        # iteração. Comentário de linha também pode terminar no EOF.

    def _block_comment(self) -> None:
        while not self._is_at_end():
            if self._peek() == "*" and self._peek_next() == "/":
                self._advance()
                self._advance()
                return
            self._advance()

        self._error(
            "comentário de bloco não fechado; esperado '*/'",
            self._current_lexeme(),
        )

    def _add_token(self, token_type: str, literal: Any = None) -> None:
        self.tokens.append(
            Token(token_type, self._current_lexeme(), self.start_line, self.start_column, literal)
        )

    def _error(self, message: str, lexeme: str) -> None:
        self.issues.append(
            LexicalIssue(message, lexeme, self.start_line, self.start_column)
        )

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self._advance()
        return True

    def _peek(self) -> str:
        return "\0" if self._is_at_end() else self.source[self.current]

    def _peek_next(self) -> str:
        next_index = self.current + 1
        return "\0" if next_index >= len(self.source) else self.source[next_index]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _current_lexeme(self) -> str:
        return self.source[self.start:self.current]

    @staticmethod
    def _is_letter(char: str) -> bool:
        return char == "_" or (char.isascii() and char.isalpha())

    @classmethod
    def _is_alphanumeric(cls, char: str) -> bool:
        return cls._is_letter(char) or (char.isascii() and char.isdigit())


def tokenize(source: str) -> List[Token]:
    """Atalho público para analisar uma string de código MiniLang."""
    return Lexer(source).tokenize()
