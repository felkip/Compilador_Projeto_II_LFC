# MiniLang — Compilador-Intérprete

Projeto da Unidade II de **Linguagens Formais e Compiladores** (Ciência da Computação, UNIT).

**Docente:** Layse Santos Souza.

## Integrantes e contribuições

| Integrante | Principais contribuições |
|---|---|
| Luís Felipe Carmelo da Silva | Revisão e correções da etapa A; desenvolvimento da etapa B (analisador léxico, documentação das expressões regulares e do AFD, testes léxicos); revisão da etapa C, incorporação dos testes do parser e da AST e da seção "Análise sintática" do relatório; implementação da etapa E (interpretador); elaboração do relatório em PDF e revisão dos testes das etapas B a E. |
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

- **Luís Felipe Carmelo da Silva:** realizou a revisão e as correções da letra A, incluindo ajustes na documentação da gramática e nos exemplos. Desenvolveu a letra B (analisador léxico, testes e documentação) e incorporou o reconhecimento de comentários de bloco (`/* ... */`) como extensão da MiniLang, aceita pelo grupo para possibilitar o teste de comentários não fechados. Na letra C, revisou e incorporou os testes do parser e da AST e a seção "Análise sintática" do relatório, redigidos com apoio de IA. Também ficou responsável pela implementação da letra E, correspondente ao interpretador, pela elaboração do relatório final em PDF e pela revisão dos testes das etapas B a E.
- **Tiago Sales Guimaraes:** implementou o parser descendente recursivo e a AST (letras C e D), adaptando a primeira versão gerada com apoio de IA à gramática e à lógica do projeto.
- **Demais integrantes:** preencher suas contribuições nesta seção conforme as atividades que efetivamente realizaram.

Os registros de uso de IA e o detalhamento das atividades estão disponíveis em [`declaracao_IA.md`](declaracao_IA.md) e [`docs/diario_de_bordo.md`](docs/diario_de_bordo.md). A análise técnica será complementada no relatório final.

1. Pré-requisitos

Python 3.10 ou superior.

Git para clonar o repositório.

## Como executar

```bash
# 1. Clonar e entrar na pasta
git clone https://github.com/felkip/Compilador_Projeto_II_LFC.git
cd Compilador_Projeto_II_LFC

# 2. Criar ambiente virtual (opcional, mas recomendado)

O ambiente virtual mantém as dependências do projeto isoladas de outras instalações Python.

Windows:

py -m venv .venv
.venv\Scripts\activate

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate

Após a ativação, o terminal exibirá (.venv) no início da linha de comando.

# 3. Instalar as dependências

Com o ambiente virtual ativado, execute:

python -m pip install -r requirements.txt

Caso opte por não utilizar um ambiente virtual, basta executar o comando de instalação diretamente no terminal.

# 4. Executar um programa MiniLang

Para executar os exemplos disponíveis:

python -m src.interpreter exemplos/programa_valido.ml

Para testar um programa com erros:

python -m src.interpreter exemplos/programa_invalido.ml

O interpretador também permite definir um limite personalizado de iterações para os laços:

python -m src.interpreter exemplos/programa_valido.ml --max-iteracoes 1000

# 5. Executar os testes automatizados

Para executar toda a suíte de testes:

python -m pytest -v

O parâmetro -v exibe individualmente os testes executados e seus resultados.

# 6. Encerrar o ambiente virtual

Ao terminar, você pode desativar o ambiente virtual com:

deactivate
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
