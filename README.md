# Classifica Notícia

Projeto de coleta, rotulagem e classificação automática de notícias políticas brasileiras com geração de relatório diário formatado para WhatsApp.

---

## Visão Geral

O projeto tem como objetivo coletar notícias de grandes portais brasileiros, classificá-las automaticamente entre **esquerda** e **direita** com base no viés/perspectiva do conteúdo, e gerar um relatório diário no formato:

```
*PANORAMA POLÍTICO*
Panorama diário sobre a conjuntura política no Brasil.
*26/03/26*

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

O projeto é dividido em três grandes etapas:

### 1. Construção do Dataset
Notícias são coletadas manualmente dos portais via scraping (`requests` + `BeautifulSoup`), armazenadas em um banco SQLite e rotuladas uma a uma através de uma ferramenta CLI simples. O resultado é um dataset de artigos com seus respectivos rótulos (`esquerda` / `direita`).

### 2. Treinamento do Modelo
O dataset rotulado é usado para treinar um modelo de classificação de texto. O pipeline usa `TF-IDF` para vetorização e `Regressão Logística` (ou SVM) como classificador. O modelo treinado é salvo e reutilizado na etapa de produção.

### 3. Produção
Em produção, o sistema lê automaticamente os feeds RSS dos portais cadastrados, passa cada notícia pelo modelo treinado, e gera o relatório formatado para WhatsApp. O pipeline roda diariamente via agendamento.

---

## Portais Monitorados

| Portal | Scraping (dataset) | RSS (produção) |
|---|---|---|
| G1 | ✓ | ✓ |
| Folha de SP | ✓ | ✓ |
| Correio Braziliense | ✓ | ✓ |
| Jornal de Brasília | ✓ | ✓ |
| Metrópoles | ✓ | ✓ |
| Brasil de Fato | ✓ | ✓ |
| Outros | a definir | a definir |

---

## Estrutura do Projeto

```
classifica-noticia/
├── data/
│   ├── raw/              # HTML/JSON bruto coletado pelos scrapers
│   ├── processed/        # dataset limpo e pronto para treino (CSV)
│   └── classifica.db     # banco SQLite com artigos e labels
│
├── scraper/
│   ├── portals/          # um arquivo por portal (g1.py, folha.py, etc.)
│   ├── base_scraper.py   # classe base com lógica de request e parsing
│   └── rss_reader.py     # lê feeds RSS dos portais (usado em produção)
│
├── labeling/
│   └── label_tool.py     # CLI para rotulagem manual dos artigos
│
├── model/
│   ├── preprocess.py     # limpeza e normalização do texto
│   ├── train.py          # treinamento e salvamento do modelo
│   ├── evaluate.py       # métricas e análise de desempenho
│   └── predict.py        # carrega o modelo e classifica novos textos
│
├── report/
│   └── generator.py      # gera o relatório formatado para WhatsApp
│
├── pipeline/
│   └── run.py            # entry point de produção: RSS → modelo → relatório
│
└── notebooks/
    └── EDA.ipynb         # análise exploratória dos dados
```

---

## Stack Tecnológica

| Biblioteca | Uso |
|---|---|
| `requests` + `beautifulsoup4` | Scraping dos portais |
| `feedparser` | Leitura dos feeds RSS |
| `sqlite3` | Armazenamento dos artigos |
| `pandas` | Manipulação do dataset |
| `scikit-learn` | TF-IDF, treinamento e avaliação do modelo |
| `joblib` | Salvar e carregar o modelo treinado |
| `schedule` | Agendamento do pipeline em produção |

---

## Fluxo de Dados

```
[DATASET]
Portais → scraper → SQLite → label_tool (rotulagem manual) → dataset.csv

[TREINAMENTO]
dataset.csv → preprocess → TF-IDF + Classificador → modelo.pkl

[PRODUÇÃO]
RSS feeds → rss_reader → predict (modelo.pkl) → generator → relatório WhatsApp
```

---

## Critério de Classificação

A classificação é baseada no **viés e perspectiva** do conteúdo, não apenas nos personagens citados. Exemplos:

- Notícia do *Brasil de Fato* criticando Ibaneis → **esquerda**
- Coluna do *Jornal de Brasília* defendendo Bolsonaro → **direita**
- Notícia neutra sobre votação na CLDF → depende do enquadramento

O modelo aprende esse padrão a partir dos exemplos rotulados manualmente.

---

## Roadmap

- [x] Definição da arquitetura
- [ ] Implementação dos scrapers
- [ ] Rotulagem do dataset (meta: 1000 artigos)
- [ ] Treinamento e avaliação do modelo
- [ ] Pipeline de produção com RSS
- [ ] Deploy em servidor com envio automático via WhatsApp
- [ ] Migração para BERT em português (melhoria futura)
