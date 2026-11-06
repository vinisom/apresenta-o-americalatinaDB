# América Latina DB — Análise de Futebol e Scouting

## Sobre o projeto

O **América Latina DB** é um projeto de análise de dados aplicado ao futebol sul-americano, desenvolvido para integrar informações de desempenho esportivo e valor de mercado dos jogadores.

O objetivo é transformar dados de diferentes fontes em informações úteis para análise de desempenho, comparação de atletas, identificação de talentos e apoio à tomada de decisão em possíveis contratações.

Esta versão apresenta análises do Campeonato Brasileiro de 2025 por meio de um dashboard interativo.

## Objetivos

- Analisar o desempenho individual dos jogadores.
- Comparar atletas por posição e indicadores estatísticos.
- Identificar destaques esportivos e oportunidades de mercado.
- Relacionar desempenho em campo e valor de mercado.
- Disponibilizar análises interativas para consulta e exploração dos dados.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Processamento de dados e desenvolvimento |
| SQL Server | Armazenamento e consultas no banco original |
| SQL | Tratamento, integração e criação de VIEWs analíticas |
| SQLite | Banco portátil para execução do dashboard |
| Pandas | Manipulação e análise dos dados |
| SQLAlchemy | Conexão com os bancos de dados |
| Streamlit | Desenvolvimento do dashboard |
| Plotly | Visualização interativa dos dados |
| Git e GitHub | Versionamento e publicação do projeto |
| Notion | Organização e documentação do projeto |

## Fontes de dados

**SofaScore:** estatísticas de desempenho dos jogadores, incluindo gols, assistências, minutos jogados, avaliações e indicadores técnicos.

**Transfermarkt:** informações de mercado, posições, clubes, nacionalidades, valores de mercado e contratos.

Os dados são integrados para permitir análises que relacionam desempenho esportivo e informações de mercado.

## Funcionalidades do dashboard

### Rankings de desempenho

Classificação dos jogadores por diferentes indicadores estatísticos, com filtros por clube e posição.

### Comparação entre jogadores

Comparação direta de dois atletas utilizando gráficos de barras e radar de percentis.

### Análise de mercado

Visualização dos valores de mercado e comparação com indicadores de desempenho esportivo.

### Exploração dos dados

Consulta às tabelas analíticas e possibilidade de exportação dos resultados em CSV.

## Arquitetura do projeto

O fluxo de dados segue as seguintes etapas:

1. Coleta de dados do SofaScore e Transfermarkt.
2. Organização e tratamento das informações.
3. Armazenamento e integração no SQL Server.
4. Criação de VIEWs analíticas utilizando SQL.
5. Exportação dos resultados para SQLite.
6. Desenvolvimento e visualização no Streamlit.

O SQLite permite executar a versão demonstrativa do dashboard sem depender de uma instalação local do SQL Server.

## Como executar

**1. Clone o repositório**

```bash
git clone https://github.com/vinisom/apresenta-o-americalatinaDB.git
```

**2. Entre na pasta do projeto**

```bash
cd apresenta-o-americalatinaDB
```

**3. Instale as dependências**

```bash
python -m pip install -r requirements.txt
```

**4. Execute o dashboard**

```bash
python -m streamlit run app.py
```

O Streamlit disponibilizará um endereço local para acessar o dashboard pelo navegador.

**Requisito:** o arquivo `americaLatinaDB.db` deve estar presente na pasta esperada pelo projeto.

## Escopo e limitações

Esta versão demonstrativa utiliza dados do Campeonato Brasileiro de 2025.

As métricas por 90 minutos devem ser interpretadas com cautela quando os jogadores possuem poucos minutos em campo.

Os valores de mercado são estimativas das fontes consultadas e não representam necessariamente o valor final de uma transferência.

## Evolução do projeto

O América Latina DB tem como proposta ampliar as análises para outras ligas sul-americanas, incluindo comparações entre países, clubes, posições e períodos de coleta.

## Finalidade

Projeto acadêmico e de portfólio voltado à aplicação prática de SQL, Python, bancos de dados, análise de dados e Business Intelligence no futebol.