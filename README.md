# MiniLang — Compilador-Intérprete

Projeto da Unidade II de **Linguagens Formais e Compiladores** (Ciência da Computação, UNIT).

**Docente:** Layse Santos Souza.

## Integrantes e contribuições

| Integrante | Principais contribuições |
|---|---|
| Luís Felipe Carmelo da Silva | Revisão e correções da etapa A; desenvolvimento da etapa B (analisador léxico, documentação das expressões regulares e do AFD, testes léxicos); revisão da etapa C, incorporação dos testes do parser e da seção "Análise sintática" do relatório. |
| [Tiago Sales Guimaraes] | [Parser descendente recursivo e AST (itens c e d), conforme o diário de bordo.] |
| [Nome do terceiro integrante] | [Descrever as contribuições efetivamente realizadas.] |

## Ferramentas utilizadas

- **Python:** linguagem utilizada na implementação do projeto.
- **pytest:** execução dos testes automatizados.
- **Git e GitHub:** controle de versão e hospedagem do repositório.
- **ChatGPT (GPT-6):** apoio à revisão da gramática, análise da implementação do lexer, elaboração e revisão de testes e documentação.
- **Claude (Sonnet 5.5):** apoio à implementação e revisão do parser e da AST, à redação da seção de análise sintática do relatório e à escrita dos testes do parser e da AST. Detalhes em `declaracao_IA.md`.

As sugestões geradas pelas ferramentas de IA foram utilizadas como apoio, devendo ser revisadas, compreendidas e verificadas pelos integrantes do grupo.
Os usos específicos das ferramentas estão registrados em [`declaracao_IA.md`](declaracao_IA.md) e [`docs/diario_de_bordo.md`](docs/diario_de_bordo.md).

## Contribuições individuais registradas

- **Luís Felipe Carmelo da Silva:** realizou a revisão e as correções da letra A, incluindo ajustes na documentação da gramática e nos exemplos. Desenvolveu a letra B (analisador léxico, testes e documentação) e incorporou o reconhecimento de comentários de bloco (`/* ... */`) como extensão da MiniLang, aceita pelo grupo para possibilitar o teste de comentários não fechados. Na letra C, revisou e incorporou os testes do parser e da AST e a seção "Análise sintática" do relatório, redigidos com apoio de IA (ver `declaracao_IA.md`).
- **Tiago Sales Guimaraes:** implementou o parser descendente recursivo e a AST (letras C e D), adaptando a primeira versão gerada com apoio de IA à gramática e à lógica do projeto.
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
