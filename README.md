# Classifica Notícia

Projeto de coleta, rotulagem e classificação automática de notícias políticas brasileiras com geração de relatório diário formatado para WhatsApp.

---

## Visão Geral

O projeto tem como objetivo coletar notícias de grandes portais brasileiros, classificá-las automaticamente entre **esquerda** e **direita** com base no viés/perspectiva do conteúdo, e gerar um relatório diário no formato:

```
*PANORAMA POLÍTICO*
Panorama diário sobre a conjuntura política no Brasil.
*06/04/26*

*DIREITA*
*Título da notícia.*
PORTAL
https://link.com.br

*ESQUERDA*
*Título da notícia.*
PORTAL
https://link.com.br
```

A classificação não é baseada apenas em quem é citado na notícia, mas no **viés e perspectiva** do conteúdo — uma notícia do Brasil de Fato criticando um político de direita é classificada como esquerda, não como direita.

---

## Como Funciona

### 1. Construção do Dataset
Notícias são coletadas dos portais via scraping (`requests` + `BeautifulSoup`) e rotuladas manualmente através de uma interface Streamlit. O resultado é um dataset de artigos com seus respectivos rótulos (`Esquerda` / `Direita`), armazenado em um banco PostgreSQL no Supabase.

### 2. Treinamento do Modelo
O dataset rotulado é usado para treinar um modelo de classificação de texto. O pipeline usa `TF-IDF` para vetorização e `Regressão Logística` (ou SVM) como classificador. O modelo treinado é salvo e reutilizado na etapa de produção.

### 3. Produção
Em produção, o sistema lê automaticamente os feeds RSS dos portais cadastrados, passa cada notícia pelo modelo treinado e gera o relatório formatado para WhatsApp. O pipeline roda diariamente via agendamento.

---

## Portais Monitorados

| Portal | Scraper |
|---|---|
| G1 | ✓ |
| CNN Brasil | ✓ |
| Correio Braziliense | ✓ |
| Jornal de Brasília | ✓ |
| Metrópoles | ✓ |
| Brasil de Fato | ✓ |
| Vero Notícias | ✓ |

---

## Estrutura do Projeto

```
classifica_noticia/
├── src/
│   ├── app/
│   │   ├── pages/            # páginas da interface Streamlit
│   │   ├── inicio.py         # página inicial
│   │   └── utils.py          # dicionário de portais e funções compartilhadas
│   │
│   ├── database/
│   │   ├── queries/          # arquivos .sql separados por operação
│   │   ├── db.py             # conexão e funções de acesso ao banco
│   │   └── schema.sql        # definição das tabelas
│   │
│   ├── scraper/
│   │   ├── portals/          # um arquivo por portal
│   │   └── base_scraper.py   # lógica base de request e parsing
│   │
│   └── model/                # pré-processamento, treino, avaliação e predição
│
├── notebooks/
│   └── EDA.ipynb             # análise exploratória dos dados
│
├── .env.example              # variáveis de ambiente necessárias
├── pyproject.toml
└── TODO.md
```

---

## Stack Tecnológica

| Biblioteca | Uso |
|---|---|
| `requests` + `beautifulsoup4` | Scraping dos portais |
| `psycopg2` | Conexão com o banco PostgreSQL |
| `python-dotenv` | Gerenciamento de variáveis de ambiente |
| `streamlit` | Interface de coleta, rotulagem e visualização |
| `plotly` | Gráficos no dashboard |
| `pandas` | Manipulação do dataset |
| `scikit-learn` | TF-IDF, treinamento e avaliação do modelo |
| `joblib` | Salvar e carregar o modelo treinado |

---

## Fluxo de Dados

```
[DATASET]
Portais → scraper → PostgreSQL (Supabase) → interface Streamlit (rotulagem) → dataset.csv

[TREINAMENTO]
dataset.csv → preprocess → TF-IDF + Classificador → modelo.pkl

[PRODUÇÃO]
RSS feeds → rss_reader → predict (modelo.pkl) → generator → relatório WhatsApp
```

---

## Critério de Classificação

A classificação é baseada no **viés e perspectiva** do conteúdo, não apenas nos personagens citados. Exemplos:

- Notícia do *Brasil de Fato* criticando Ibaneis → **Esquerda**
- Coluna do *Jornal de Brasília* defendendo Bolsonaro → **Direita**
- Notícia neutra sobre votação → depende do enquadramento

O modelo aprende esse padrão a partir dos exemplos rotulados manualmente.

---

## Roadmap

- [x] Definição da arquitetura
- [x] Implementação dos scrapers
- [x] Interface Streamlit de coleta e rotulagem
- [x] Dashboard de acompanhamento
- [ ] Rotulagem do dataset (meta: 1000 artigos)
- [ ] Treinamento e avaliação do modelo
- [ ] Pipeline de produção com RSS
- [ ] Deploy em servidor com envio automático via WhatsApp
- [ ] Migração para BERT em português (melhoria futura)
