# MiniLang — Compilador-Intérprete

Projeto da Unidade II de **Linguagens Formais e Compiladores** (Ciência da Computação, UNIT).
Docente: Layse Santos Souza.

## Integrantes

| Nome | Matrícula | Parte principal |
|------|-----------|-----------------|
| Luís Felipe Carmelo da Silva | _preencher_ | _preencher_ |
| _Integrante 2_ | _preencher_ | _preencher_ |
| _Integrante 3_ | _preencher_ | _preencher_ |

## Ferramenta de IA utilizada

_Declarar aqui a(s) ferramenta(s) e modelo(s) (ex.: Claude, ChatGPT, Copilot) ou escrever que não houve uso._
Detalhes completos em [`declaracao_IA.md`](declaracao_IA.md), [`docs/diario_de_bordo.md`](docs/diario_de_bordo.md) e `docs/relatorio.pdf`.

## Requisitos

- Python 3.10 ou superior

## Como executar

```bash
# 1. clonar e entrar na pasta
git clone <URL-DO-REPOSITORIO>
cd minilang-compilador

# 2. (opcional) ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. dependências
pip install -r requirements.txt

# 4. rodar um programa MiniLang
python -m src.interpreter exemplos/programa_valido.ml
python -m src.interpreter exemplos/programa_invalido.ml

# 5. rodar toda a suíte de testes
pytest
```

> TODO: confirmar que o passo 4 funciona quando o `interpreter.py` tiver um `main`.

## Estrutura

```
docs/        relatório (PDF), gramática, diário de bordo, vídeo
exemplos/    programas .ml de demonstração
src/         lexer, parser, AST, interpretador
tests/       validos/ e invalidos/
```

## Vídeo de apresentação

_Colar aqui o link público (ou indicar `docs/apresentacao.mp4`)._
