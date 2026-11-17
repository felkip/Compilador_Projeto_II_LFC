"""Parser descendente recursivo da MiniLang (item c). TODO

Técnica: análise descendente recursiva preditiva, LL(1). Há uma função para
cada não terminal da gramática (docs/gramatica.md) e, olhando apenas o token
atual (lookahead de 1), sempre dá para decidir qual produção usar.

A precedência vem da hierarquia das funções:

    expressao -> igualdade -> comparacao -> termo -> fator -> unario -> primario

Quem fica mais fundo na cadeia de chamadas (ex.: `*`) é resolvido primeiro.
Os operadores `{ ... }` da EBNF viram laços `while`, o que dá associatividade
à esquerda sem recursão à esquerda.

Erros sintáticos lançam ParseError no primeiro problema (modo pânico simples:
o parser para e informa linha, coluna e o que era esperado).
"""

from typing import List

from .ast_nodes import (
    Assign, Binary, Block, Bool, For, If, Num, Print, Program, Unary, Var, While,
)
from .lexer import Token, tokenize


class ParseError(Exception):
    """Erro sintático com posição e descrição do problema."""

    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        self.line = token.line
        self.column = token.column
        super().__init__(f"{message} em {token.line}:{token.column}")


class Parser:
    OPS_IGUALDADE = ("IGUAL", "DIFERENTE")
    OPS_RELACIONAIS = ("MENOR", "MAIOR", "MENOR_IGUAL", "MAIOR_IGUAL")

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    # ------------------------------------------------------------ utilitários

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _is_at_end(self) -> bool:
        return self._peek().type == "EOF"

    def _check(self, *tipos: str) -> bool:
        return self._peek().type in tipos

    def _advance(self) -> Token:
        token = self._peek()
        if not self._is_at_end():
            self.pos += 1
        return token

    def _match(self, *tipos: str) -> bool:
        """Se o token atual for de um dos tipos, consome e devolve True."""
        if self._check(*tipos):
            self._advance()
            return True
        return False

    def _consume(self, tipo: str, mensagem: str) -> Token:
        """Exige um token do tipo dado; senão, erro sintático."""
        if self._check(tipo):
            return self._advance()
        raise ParseError(f"{mensagem}, encontrado {self._descrever(self._peek())}", self._peek())

    @staticmethod
    def _descrever(token: Token) -> str:
        return "fim do arquivo" if token.type == "EOF" else f"'{token.lexeme}'"

    # --------------------------------------------------------------- comandos

    def parse(self) -> Program:
        """programa = { comando } EOF ;"""
        comandos = []
        while not self._is_at_end():
            comandos.append(self._comando())
        return Program(comandos)

    def _comando(self):
        tipo = self._peek().type
        if tipo == "ID":
            no = self._atribuicao()
            self._consume("PONTO_VIRGULA", "esperado ';' após a atribuição")
            return no
        if tipo == "PRINT":
            return self._print()
        if tipo == "IF":
            return self._if()
        if tipo == "WHILE":
            return self._while()
        if tipo == "FOR":
            return self._for()
        if tipo == "ABRE_CHAVE":
            return self._bloco()
        raise ParseError(
            f"esperado um comando, encontrado {self._descrever(self._peek())}", self._peek()
        )

    def _atribuicao(self) -> Assign:
        """atribuicao = ID "=" expressao ;   (sem o ';', que é do comando)"""
        nome = self._consume("ID", "esperado um identificador")
        self._consume("ATRIB", "esperado '=' na atribuição")
        valor = self._expressao()
        return Assign(nome.lexeme, valor, nome.line)

    def _print(self) -> Print:
        """comando_print = "print" "(" expressao ")" ";" ;"""
        inicio = self._advance()
        self._consume("ABRE_PAR", "esperado '(' após 'print'")
        valor = self._expressao()
        self._consume("FECHA_PAR", "esperado ')' após a expressão do 'print'")
        self._consume("PONTO_VIRGULA", "esperado ';' após o 'print'")
        return Print(valor, inicio.line)

    def _if(self) -> If:
        """comando_if = "if" "(" expressao ")" bloco [ "else" bloco ] ;"""
        inicio = self._advance()
        self._consume("ABRE_PAR", "esperado '(' após 'if'")
        condicao = self._expressao()
        self._consume("FECHA_PAR", "esperado ')' após a condição do 'if'")
        entao = self._bloco()
        senao = self._bloco() if self._match("ELSE") else None
        return If(condicao, entao, senao, inicio.line)

    def _while(self) -> While:
        """comando_while = "while" "(" expressao ")" bloco ;"""
        inicio = self._advance()
        self._consume("ABRE_PAR", "esperado '(' após 'while'")
        condicao = self._expressao()
        self._consume("FECHA_PAR", "esperado ')' após a condição do 'while'")
        corpo = self._bloco()
        return While(condicao, corpo, inicio.line)

    def _for(self) -> For:
        """comando_for = "for" "(" atribuicao ";" expressao ";" atribuicao ")" bloco ;

        As três cláusulas são obrigatórias: cada ';' e cada parte é exigida
        com _consume/_atribuicao, então qualquer cláusula faltando vira erro.
        """
        inicio = self._advance()
        self._consume("ABRE_PAR", "esperado '(' após 'for'")
        init = self._atribuicao()
        self._consume("PONTO_VIRGULA", "esperado ';' após a inicialização do 'for'")
        condicao = self._expressao()
        self._consume(
            "PONTO_VIRGULA",
            "esperado ';' após a condição do 'for' (a cláusula de atualização é obrigatória)",
        )
        update = self._atribuicao()
        self._consume("FECHA_PAR", "esperado ')' após a atualização do 'for'")
        corpo = self._bloco()
        return For(init, condicao, update, corpo, inicio.line)

    def _bloco(self) -> Block:
        """bloco = "{" { comando } "}" ;"""
        abre = self._consume("ABRE_CHAVE", "esperado '{' para iniciar o bloco")
        comandos = []
        while not self._check("FECHA_CHAVE") and not self._is_at_end():
            comandos.append(self._comando())
        self._consume("FECHA_CHAVE", "esperado '}' para fechar o bloco")
        return Block(comandos, abre.line)

    # ------------------------------------------------------------- expressões

    def _expressao(self):
        """expressao = igualdade ;"""
        return self._igualdade()

    def _igualdade(self):
        """igualdade = comparacao { ( "==" | "!=" ) comparacao ; (esquerda)"""
        no = self._comparacao()
        while self._check(*self.OPS_IGUALDADE):
            op = self._advance()
            direita = self._comparacao()
            no = Binary(op.lexeme, no, direita, op.line)
        return no

    def _comparacao(self):
        """comparacao = termo [ ( "<" | ">" | "<=" | ">=" ) termo ] ;  (não associativo)"""
        no = self._termo()
        if self._check(*self.OPS_RELACIONAIS):
            op = self._advance()
            direita = self._termo()
            no = Binary(op.lexeme, no, direita, op.line)
            if self._check(*self.OPS_RELACIONAIS):
                raise ParseError(
                    "operadores relacionais não são associativos (ex.: a < b < c)",
                    self._peek(),
                )
        return no

    def _termo(self):
        """termo = fator { ( "+" | "-" ) fator } ;  (esquerda)"""
        no = self._fator()
        while self._check("MAIS", "MENOS"):
            op = self._advance()
            direita = self._fator()
            no = Binary(op.lexeme, no, direita, op.line)
        return no

    def _fator(self):
        """fator = unario { ( "*" | "/" ) unario } ;  (esquerda)"""
        no = self._unario()
        while self._check("MULT", "DIV"):
            op = self._advance()
            direita = self._unario()
            no = Binary(op.lexeme, no, direita, op.line)
        return no

    def _unario(self):
        """unario = "-" unario | primario ;  (direita)"""
        if self._check("MENOS"):
            op = self._advance()
            return Unary("-", self._unario(), op.line)
        return self._primario()

    def _primario(self):
        """primario = INT | "true" | "false" | ID | "(" expressao ")" ;"""
        token = self._peek()
        if token.type == "INT":
            self._advance()
            return Num(token.literal, token.line)
        if token.type in ("TRUE", "FALSE"):
            self._advance()
            return Bool(token.literal, token.line)
        if token.type == "ID":
            self._advance()
            return Var(token.lexeme, token.line)
        if token.type == "ABRE_PAR":
            self._advance()
            no = self._expressao()
            self._consume("FECHA_PAR", "esperado ')' para fechar a expressão")
            return no
        raise ParseError(
            f"esperada uma expressão, encontrado {self._descrever(token)}", token
        )


def parse(source: str) -> Program:
    """Atalho: texto MiniLang -> AST. Pode lançar LexicalError ou ParseError."""
    return Parser(tokenize(source)).parse()