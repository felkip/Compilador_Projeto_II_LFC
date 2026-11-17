"""Nos da AST da MiniLang (item d), incluindo While e For. TODO."""
"""Nós da AST da MiniLang (item d), incluindo While e For.

A AST é a versão "limpa" da árvore sintática: não guarda parênteses, ponto e
vírgula, chaves nem palavras-chave, apenas o que o interpretador precisa para
executar. A precedência e a associatividade ficam codificadas na forma da
árvore (quem está mais fundo é avaliado primeiro).

O campo `line` serve só para mensagens de erro; por isso fica fora da
comparação (compare=False), e dois nós iguais em estrutura são considerados
iguais nos testes.
"""

from dataclasses import dataclass, field, fields, is_dataclass
from typing import List, Optional, Union


# ---------------------------------------------------------------- Expressões

@dataclass(frozen=True)
class Num:
    value: int
    line: int = field(default=0, compare=False)


@dataclass(frozen=True)
class Bool:
    value: bool
    line: int = field(default=0, compare=False)


@dataclass(frozen=True)
class Var:
    name: str
    line: int = field(default=0, compare=False)


@dataclass(frozen=True)
class Unary:
    op: str            # "-"
    operand: "Expr"
    line: int = field(default=0, compare=False)


@dataclass(frozen=True)
class Binary:
    op: str            # + - * / < > <= >= == !=
    left: "Expr"
    right: "Expr"
    line: int = field(default=0, compare=False)


Expr = Union[Num, Bool, Var, Unary, Binary]


# ------------------------------------------------------------------ Comandos

@dataclass(frozen=True)
class Assign:
    name: str
    value: Expr
    line: int = field(default=0, compare=False)


@dataclass(frozen=True)
class Print:
    value: Expr
    line: int = field(default=0, compare=False)


@dataclass(frozen=True)
class Block:
    statements: List["Stmt"]
    line: int = field(default=0, compare=False)


@dataclass(frozen=True)
class If:
    condition: Expr
    then_body: Block
    else_body: Optional[Block] = None
    line: int = field(default=0, compare=False)


@dataclass(frozen=True)
class While:
    condition: Expr
    body: Block
    line: int = field(default=0, compare=False)


@dataclass(frozen=True)
class For:
    init: Assign        # inicialização (atribuição)
    condition: Expr     # condição (deve ser booleana)
    update: Assign      # atualização (atribuição)
    body: Block
    line: int = field(default=0, compare=False)


Stmt = Union[Assign, Print, Block, If, While, For]


@dataclass(frozen=True)
class Program:
    statements: List[Stmt]
    line: int = field(default=1, compare=False)


# ------------------------------------------------------- Impressão da árvore

def _eh_no(valor) -> bool:
    return is_dataclass(valor) or isinstance(valor, (list, tuple))


def arvore_texto(no, nivel: int = 0) -> str:
    """Devolve a árvore como texto indentado (útil para o relatório)."""
    pad = "  " * nivel
    if isinstance(no, (list, tuple)):
        return "".join(arvore_texto(filho, nivel) for filho in no)
    if no is None:
        return f"{pad}(vazio)\n"

    simples = [
        f"{f.name}={getattr(no, f.name)!r}"
        for f in fields(no)
        if f.name != "line" and not _eh_no(getattr(no, f.name))
        and getattr(no, f.name) is not None
    ]
    saida = f"{pad}{type(no).__name__}({', '.join(simples)})\n"
    for f in fields(no):
        valor = getattr(no, f.name)
        if f.name != "line" and (_eh_no(valor) or valor is None and f.name == "else_body"):
            if valor is None:
                continue
            saida += f"{pad}  .{f.name}:\n" + arvore_texto(valor, nivel + 2)
    return saida