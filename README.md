# README do Projeto Final SBD2

## Descrição

O **Projeto-Final-SBD2** é um sistema desenvolvido para extrair, armazenar e analisar dados sobre partidos políticos e deputados federais do Brasil. Utilizando a API de Dados Abertos da Câmara dos Deputados, o projeto coleta informações relevantes e as armazena em um banco de dados MySQL, permitindo análises posteriores através de ferramentas de Data Mining, como o Orange.

## Funcionalidades

- **Extração de Dados**: O sistema realiza requisições à API da Câmara dos Deputados para obter informações sobre partidos e deputados, incluindo despesas.
- **Armazenamento em Banco de Dados**: Os dados extraídos são armazenados em um banco de dados MySQL, organizados em tabelas para fácil acesso e manipulação.
- **Validação de Dados**: O sistema identifica e separa dados "estranhos" (como despesas com valores negativos ou inválidos) em uma tabela específica.
- **Análise de Dados**: Os dados armazenados podem ser analisados utilizando o software Orange, facilitando a visualização e interpretação dos dados.

## Estrutura do Banco de Dados

O banco de dados contém as seguintes tabelas:

1. **partidos**: Armazena informações sobre os partidos políticos.
   - `sigla`: Sigla do partido (chave primária).
   - `nome`: Nome do partido.

2. **deputados**: Armazena informações sobre os deputados federais.
   - `id`: ID do deputado (chave primária).
   - `nome`: Nome do deputado.
   - `partido`: Sigla do partido (chave estrangeira referenciando `partidos`).

3. **gastos**: Armazena informações sobre as despesas dos deputados.
   - `id`: ID da despesa (chave primária).
   - `id_deputado`: ID do deputado (chave estrangeira referenciando `deputados`).
   - `data`: Data da despesa.
   - `valor`: Valor da despesa.
   - `tipoDespesa`: Tipo da despesa.
   - `codDocumento`: Código do documento da despesa.

4. **gastos_estranhos**: Armazena despesas que não atendem aos critérios de validade.
   - `id`: ID da despesa (chave primária).
   - `id_deputado`: ID do deputado (chave estrangeira referenciando `deputados`).
   - `data`: Data da despesa.
   - `valor`: Valor da despesa.
   - `tipoDespesa`: Tipo da despesa.
   - `codDocumento`: Código do documento da despesa.

## Requisitos

- Python 3.x
- Bibliotecas: `requests`, `mysql-connector-python`
- Banco de dados MySQL configurado com as credenciais corretas

## Como Usar

1. **Configurar o Banco de Dados**: Crie um banco de dados chamado "TFBD" e configure as credenciais de acesso (usuário e senha) no código.

2. **Executar o Código**: Execute o script Python para iniciar a extração e armazenamento dos dados.

```bash
python projeto_final_sbd2.py
```

3. **Analisar os Dados**: Após a execução do programa, utilize o software Orange para realizar análises de Data Mining nos dados coletados.

## Detalhes do Código

O código está dividido em várias seções, cada uma responsável por uma parte do processo:

1. **Extração de Dados dos Partidos**: Faz uma requisição à API para obter os partidos e armazena no banco de dados.

2. **Extração de Dados dos Deputados**: Faz uma requisição à API para obter os deputados e suas informações, armazenando-os no banco de dados.

3. **Extração de Despesas dos Deputados**: Para cada deputado, o sistema coleta suas despesas e as armazena na tabela `gastos`.

4. **Identificação de Gastos Estranhos**: O sistema verifica e separa gastos que não estão de acordo com os critérios definidos, armazenando-os na tabela `gastos_estranhos`.

5. **Análise de Dados**: Os dados podem ser analisados utilizando ferramentas de Data Mining, como o Orange.

---
