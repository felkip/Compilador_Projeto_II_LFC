# MiniLang — Compilador-Intérprete

Projeto da Unidade II de **Linguagens Formais e Compiladores** (Ciência da Computação, UNIT).

**Docente:** Layse Santos Souza.

## Integrantes

| Nome | Matrícula | Parte principal |
|------|-----------|-----------------|
| Luís Felipe Carmelo da Silva | _preencher_ | Correções da letra A e desenvolvimento da letra B (analisador léxico) |
| _Integrante 2_ | _preencher_ | _preencher_ |
| _Integrante 3_ | _preencher_ | _preencher_ |

## Ferramentas de IA utilizadas

Claude Sonnet 5.5 (Anthropic) e ChatGPT (GPT-6, OpenAI) foram utilizados como copilotos durante o planejamento, a revisão documental e o apoio à implementação e aos testes do analisador léxico (item B).

Os usos específicos das ferramentas estão registrados em [`declaracao_IA.md`](declaracao_IA.md) e [`docs/diario_de_bordo.md`](docs/diario_de_bordo.md).

## Contribuições individuais registradas

- **Luís Felipe Carmelo da Silva:** realizou a revisão e as correções da letra A, incluindo ajustes na documentação da gramática e nos exemplos. Desenvolveu a letra B, incluindo a implementação do analisador léxico, seus testes e a documentação correspondente. Também incorporou o reconhecimento de comentários de bloco (`/* ... */`) como extensão da MiniLang, aceita pelo grupo para possibilitar o teste de comentários não fechados.
- **Demais integrantes:** preencher suas contribuições nesta seção conforme as atividades que efetivamente realizaram.

Os registros de uso de IA e o detalhamento das atividades estão disponíveis em [`declaracao_IA.md`](declaracao_IA.md) e [`docs/diario_de_bordo.md`](docs/diario_de_bordo.md). A análise técnica será complementada no relatório final.

## Requisitos

- Python 3.10 ou superior.

## Como executar

```bash
# 1. Clonar e entrar na pasta
git clone <URL-DO-REPOSITORIO>
cd minilang-compilador

# 2. Criar ambiente virtual (opcional)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar um programa MiniLang
python -m src.interpreter exemplos/programa_valido.ml
python -m src.interpreter exemplos/programa_invalido.ml

# 5. Executar a suíte de testes
pytest
```

> **Observação:** o comando de execução dos programas depende da implementação de um ponto de entrada (`main`) no interpretador.

## Estrutura do projeto

```text
docs/        relatório (PDF), gramática, diário de bordo e vídeo
exemplos/    programas .ml de demonstração
src/         lexer (implementado), parser, AST e interpretador
tests/       testes válidos e inválidos
```

## Vídeo de apresentação

_Adicionar o link público do vídeo ou indicar o arquivo `docs/apresentacao.mp4`._
