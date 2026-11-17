# MiniLang — Compilador-Intérprete

Projeto da Unidade II de **Linguagens Formais e Compiladores** (Ciência da Computação, UNIT).

**Docente:** Layse Santos Souza.

## Integrantes e contribuições

| Integrante | Principais contribuições |
|---|---|
| Luís Felipe Carmelo da Silva | Revisão e correções da etapa A; desenvolvimento da etapa B, incluindo implementação do analisador léxico, documentação das expressões regulares e do AFD e elaboração dos testes léxicos. |
| [Tiago Sales Guimaraes] | [Parser descendente recursivo e AST (itens c e d), conforme o diário de bordo.] |
| [Nome do terceiro integrante] | [Descrever as contribuições efetivamente realizadas.] |

## Ferramentas utilizadas

- **Python:** linguagem utilizada na implementação do projeto.
- **pytest:** execução dos testes automatizados.
- **Git e GitHub:** controle de versão e hospedagem do repositório.
- **ChatGPT (GPT-6):** apoio à revisão da gramática, análise da implementação do lexer, elaboração e revisão de testes e documentação.
- **Claude:** ferramenta de apoio utilizada durante o desenvolvimento. O modelo e as etapas específicas de utilização devem corresponder ao registro da declaração de IA.

As sugestões geradas pelas ferramentas de IA foram utilizadas como apoio, devendo ser revisadas, compreendidas e verificadas pelos integrantes do grupo.
Os usos específicos das ferramentas estão registrados em [`declaracao_IA.md`](declaracao_IA.md) e [`docs/diario_de_bordo.md`](docs/diario_de_bordo.md).

## Contribuições individuais registradas

- **Luís Felipe Carmelo da Silva:** realizou a revisão e as correções da letra A, incluindo ajustes na documentação da gramática e nos exemplos. Desenvolveu a letra B, incluindo a implementação do analisador léxico, seus testes e a documentação correspondente. Também incorporou o reconhecimento de comentários de bloco (`/* ... */`) como extensão da MiniLang, aceita pelo grupo para possibilitar o teste de comentários não fechados.
- **Tiago Sales Guimaraes:** realizou a revisão da letra C,.
- **Demais integrantes:** preencher suas contribuições nesta seção conforme as atividades que efetivamente realizaram.

Os registros de uso de IA e o detalhamento das atividades estão disponíveis em [`declaracao_IA.md`](declaracao_IA.md) e [`docs/diario_de_bordo.md`](docs/diario_de_bordo.md). A análise técnica será complementada no relatório final.

## Requisitos

- Python 3.10 ou superior.

## Como executar

```bash
# 1. Clonar e entrar na pasta
git clone <URL-DO-REPOSITORIO>
cd Compilador_Projeto_II_LFC

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
