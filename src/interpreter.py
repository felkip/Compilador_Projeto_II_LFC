"""Interpretador e tabela de símbolos da MiniLang (item e).

O interpretador percorre a AST (src/ast_nodes.py) e executa o programa. As
verificações semânticas S1 a S6 de docs/gramatica.md são feitas durante a
execução, na ordem em que os comandos rodam, e a primeira violação interrompe
o programa com um ErroSemantico.

    S1  variável usada sem ter sido atribuída
    S2  operador aritmético, relacional ou '-' unário com operando que não é int
    S3  '==' ou '!=' com operandos de tipos diferentes
    S4  condição de if, while ou for que não é bool
    S5  variável que recebe um valor de tipo diferente do que já tinha
    S6  divisão por zero

Fora das regras da linguagem, existem travas de execução, para um programa
não travar o computador nem a suíte de testes. Elas não são erros semânticos:

    - limite de iterações de laço (LimiteDeIteracoes);
    - limite de tamanho dos inteiros, 10.000 bits (InteiroGrandeDemais). Os
      inteiros da MiniLang são ilimitados na especificação, mas sem essa trava
      um `x = x * x` dentro de um laço dobra o tamanho do número a cada volta
      e trava a máquina muito antes do limite de iterações. Esse limite também
      evita o ValueError que o Python lança ao converter para texto inteiros
      com mais de 4300 dígitos (10.000 bits têm cerca de 3.000 dígitos).
"""

import argparse
import sys
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from .ast_nodes import (
    Assign, Binary, Block, Bool, For, If, Num, Print, Program, Unary, Var, While,
)
from .lexer import LexicalError
from .parser import ParseError, parse

INT = "int"
BOOL = "bool"

# Limite padrão de iterações quando o programa roda pela linha de comando.
LIMITE_PADRAO = 1_000_000

# Maior tamanho (em bits) permitido para o resultado de uma operação inteira.
LIMITE_BITS = 10_000


# ------------------------------------------------------------------- erros

class ErroSemantico(Exception):
    """Violação de uma restrição semântica (S1 a S6)."""

    def __init__(self, codigo: str, mensagem: str, linha: int):
        self.codigo = codigo
        self.mensagem = mensagem
        self.linha = linha
        super().__init__(f"[{codigo}] {mensagem} (linha {linha})")


class LimiteDeExecucao(Exception):
    """Base das travas de execução. Não são erros da linguagem."""


class LimiteDeIteracoes(LimiteDeExecucao):
    """O programa passou do número máximo de voltas de laço permitido."""


class InteiroGrandeDemais(LimiteDeExecucao):
    """O resultado de uma operação passou de LIMITE_BITS bits."""


class ProfundidadeExcedida(LimiteDeExecucao):
    """Expressão ou aninhamento tão fundo que estourou a pilha do Python."""


# ------------------------------------------------------------------- tipos

def tipo_de(valor) -> str:
    """Tipo MiniLang de um valor Python.

    Em Python, True é uma instância de int (isinstance(True, int) é True),
    então o teste precisa olhar o tipo exato. É a única função que decide
    se um valor é bool ou int, para o resto do código não repetir esse teste.
    """
    return BOOL if type(valor) is bool else INT


def formatar(valor) -> str:
    """Texto que o print escreve: true/false em minúsculo, ou o inteiro."""
    if type(valor) is bool:
        return "true" if valor else "false"
    return str(valor)


# --------------------------------------------------------- tabela de símbolos

@dataclass
class Simbolo:
    tipo: str
    valor: object
    linha_criacao: int


class TabelaSimbolos:
    """Associa cada nome de variável ao seu tipo, valor e linha de criação.

    Só existe um escopo (a MiniLang não tem escopo aninhado), então a tabela
    é um dicionário simples. As duas operações carregam as verificações:

        buscar    -> S1: o nome precisa existir
        atribuir  -> insere se for novo; se já existe, aplica S5 (mesmo tipo)
    """

    def __init__(self) -> None:
        self._simbolos: Dict[str, Simbolo] = {}

    def existe(self, nome: str) -> bool:
        return nome in self._simbolos

    def buscar(self, nome: str, linha: int) -> Simbolo:
        simbolo = self._simbolos.get(nome)
        if simbolo is None:
            raise ErroSemantico("S1", f"variável '{nome}' não definida", linha)
        return simbolo

    def atribuir(self, nome: str, valor, linha: int) -> None:
        tipo = tipo_de(valor)
        atual = self._simbolos.get(nome)
        if atual is None:
            self._simbolos[nome] = Simbolo(tipo, valor, linha)
            return
        if atual.tipo != tipo:
            raise ErroSemantico(
                "S5",
                f"a variável '{nome}' foi criada como {atual.tipo} na linha "
                f"{atual.linha_criacao} e não pode receber um valor {tipo}",
                linha,
            )
        atual.valor = valor

    def valores(self) -> Dict[str, object]:
        """Cópia simples nome -> valor, útil nos testes."""
        return {nome: s.valor for nome, s in self._simbolos.items()}

    def __len__(self) -> int:
        return len(self._simbolos)


# ------------------------------------------------------------- interpretador

def _dividir(a: int, b: int) -> int:
    """Divisão inteira truncada em direção a zero (-7 / 2 = -3).

    O // do Python arredonda para baixo (-7 // 2 = -4), então calculamos
    com os valores absolutos e depois aplicamos o sinal.
    """
    quociente = abs(a) // abs(b)
    return quociente if (a < 0) == (b < 0) else -quociente


class Interpretador:
    def __init__(
        self,
        max_iteracoes: int = LIMITE_PADRAO,
        ao_imprimir: Optional[Callable[[str], None]] = None,
    ):
        self.max_iteracoes = max_iteracoes
        self.ao_imprimir = ao_imprimir
        self.tabela = TabelaSimbolos()
        self.saida: List[str] = []
        self._iteracoes = 0

    # ----------------------------------------------------------- entrada

    def executar(self, programa: Program) -> List[str]:
        """Executa o programa do zero e devolve o que foi impresso.

        Se houver erro, o que já foi impresso continua em self.saida.
        """
        self.tabela = TabelaSimbolos()
        self.saida = []
        self._iteracoes = 0
        try:
            for comando in programa.statements:
                self._executar(comando)
        except RecursionError:
            raise ProfundidadeExcedida(
                "o programa é aninhado fundo demais para o interpretador"
            ) from None
        return self.saida

    # ---------------------------------------------------------- comandos

    def _executar(self, no) -> None:
        if isinstance(no, Assign):
            # primeiro avalia o lado direito, depois aplica S5 na tabela
            self.tabela.atribuir(no.name, self._avaliar(no.value), no.line)
        elif isinstance(no, Print):
            self._imprimir(formatar(self._avaliar(no.value)))
        elif isinstance(no, Block):
            for comando in no.statements:
                self._executar(comando)
        elif isinstance(no, If):
            if self._condicao(no.condition, "if", no.line):
                self._executar(no.then_body)
            elif no.else_body is not None:
                self._executar(no.else_body)
        elif isinstance(no, While):
            while self._condicao(no.condition, "while", no.line):
                self._contar_iteracao(no.line)
                self._executar(no.body)
        elif isinstance(no, For):
            # inicialização; testa condição; corpo; atualização; repete
            self._executar(no.init)
            while self._condicao(no.condition, "for", no.line):
                self._contar_iteracao(no.line)
                self._executar(no.body)
                self._executar(no.update)
        else:
            raise TypeError(f"nó de comando desconhecido: {type(no).__name__}")

    def _imprimir(self, texto: str) -> None:
        self.saida.append(texto)
        if self.ao_imprimir is not None:
            self.ao_imprimir(texto)

    def _condicao(self, expressao, comando: str, linha: int) -> bool:
        """Avalia uma condição e aplica S4 (precisa ser bool)."""
        valor = self._avaliar(expressao)
        if tipo_de(valor) != BOOL:
            raise ErroSemantico(
                "S4",
                f"a condição do '{comando}' deve ser booleana, mas é {tipo_de(valor)}",
                linha,
            )
        return valor

    def _contar_iteracao(self, linha: int) -> None:
        self._iteracoes += 1
        if self._iteracoes > self.max_iteracoes:
            raise LimiteDeIteracoes(
                f"limite de {self.max_iteracoes} iterações excedido "
                f"(laço da linha {linha})"
            )

    # ------------------------------------------------------- expressões

    def _avaliar(self, no):
        if isinstance(no, (Num, Bool)):
            return no.value
        if isinstance(no, Var):
            return self.tabela.buscar(no.name, no.line).valor
        if isinstance(no, Unary):
            valor = self._avaliar(no.operand)
            if tipo_de(valor) != INT:
                raise ErroSemantico(
                    "S2",
                    f"o operador '-' exige operando int, mas recebeu {tipo_de(valor)}",
                    no.line,
                )
            return -valor
        if isinstance(no, Binary):
            return self._binario(no)
        raise TypeError(f"nó de expressão desconhecido: {type(no).__name__}")

    @staticmethod
    def _limitar(resultado: int, linha: int) -> int:
        """Trava de tamanho: recusa inteiros com mais de LIMITE_BITS bits."""
        if resultado.bit_length() > LIMITE_BITS:
            raise InteiroGrandeDemais(
                f"o resultado de uma operação passou de {LIMITE_BITS} bits (linha {linha})"
            )
        return resultado

    def _binario(self, no: Binary):
        esquerda = self._avaliar(no.left)
        direita = self._avaliar(no.right)
        op = no.op
        tipo_esq, tipo_dir = tipo_de(esquerda), tipo_de(direita)

        if op in ("==", "!="):
            if tipo_esq != tipo_dir:                                  # S3
                raise ErroSemantico(
                    "S3",
                    f"'{op}' exige operandos do mesmo tipo, mas recebeu "
                    f"{tipo_esq} e {tipo_dir}",
                    no.line,
                )
            return (esquerda == direita) if op == "==" else (esquerda != direita)

        if tipo_esq != INT or tipo_dir != INT:                        # S2
            raise ErroSemantico(
                "S2",
                f"o operador '{op}' exige operandos int, mas recebeu "
                f"{tipo_esq} e {tipo_dir}",
                no.line,
            )
        if op == "+":
            return self._limitar(esquerda + direita, no.line)
        if op == "-":
            return self._limitar(esquerda - direita, no.line)
        if op == "*":
            return self._limitar(esquerda * direita, no.line)
        if op == "/":
            if direita == 0:                                          # S6
                raise ErroSemantico("S6", "divisão por zero", no.line)
            return _dividir(esquerda, direita)
        if op == "<":
            return esquerda < direita
        if op == ">":
            return esquerda > direita
        if op == "<=":
            return esquerda <= direita
        if op == ">=":
            return esquerda >= direita
        raise TypeError(f"operador desconhecido: {op}")


# ------------------------------------------------------------ atalhos e main

def interpretar(fonte: str, max_iteracoes: int = LIMITE_PADRAO) -> List[str]:
    """Texto MiniLang -> saída do programa. Pode lançar qualquer erro do compilador."""
    return Interpretador(max_iteracoes).executar(parse(fonte))


def main(argv: Optional[List[str]] = None) -> int:
    """Linha de comando: python -m src.interpreter arquivo.ml

    Códigos de saída: 0 ok; 1 erro léxico; 2 erro sintático; 3 erro semântico;
    4 trava de execução (iterações, tamanho de inteiro ou profundidade);
    5 arquivo que não pôde ser lido.
    """
    try:  # acentos nas mensagens, mesmo em consoles que não usam UTF-8
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    argumentos = argparse.ArgumentParser(description="Executa um programa MiniLang.")
    argumentos.add_argument("arquivo", help="arquivo .ml")
    argumentos.add_argument(
        "--max-iteracoes", type=int, default=LIMITE_PADRAO,
        help=f"limite de iterações de laço (padrão: {LIMITE_PADRAO})",
    )
    args = argumentos.parse_args(argv)

    try:
        with open(args.arquivo, encoding="utf-8") as f:
            fonte = f.read()
    except OSError as erro:
        print(f"erro: não foi possível ler '{args.arquivo}': {erro.strerror}", file=sys.stderr)
        return 5

    try:
        programa = parse(fonte)
    except RecursionError:
        print("erro de execução: o programa é aninhado fundo demais", file=sys.stderr)
        return 4
    except ValueError:  # int() do lexer com literal de mais de 4300 dígitos
        print("erro léxico: número inteiro grande demais", file=sys.stderr)
        return 1
    except LexicalError as erro:
        for problema in erro.issues:
            print(f"erro léxico: {problema}", file=sys.stderr)
        return 1
    except ParseError as erro:
        print(f"erro sintático: {erro}", file=sys.stderr)
        return 2

    interpretador = Interpretador(args.max_iteracoes, ao_imprimir=print)
    try:
        interpretador.executar(programa)
    except ErroSemantico as erro:
        print(f"erro semântico: {erro}", file=sys.stderr)
        return 3
    except LimiteDeExecucao as erro:
        print(f"erro de execução: {erro}", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
