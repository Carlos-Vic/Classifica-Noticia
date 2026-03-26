# Classifica Notícia — To-Do

Projeto de coleta, rotulagem e classificação automática de notícias políticas brasileiras.

---

## Fase 1 — Setup e Coleta de Dados

- [ ] Criar ambiente virtual e instalar dependências (`requests`, `beautifulsoup4`, `feedparser`, `scikit-learn`, `pandas`, `joblib`)
- [ ] Criar o banco SQLite (`data/classifica.db`) com a tabela de artigos (`id`, `titulo`, `texto`, `url`, `portal`, `data_coleta`, `label`)
- [ ] Implementar `scraper/base_scraper.py` com a lógica base de request + parsing
- [ ] Implementar scraper do **Jornal de Brasília** (`scraper/portals/jornal_brasilia.py`)
- [ ] Implementar scraper do **Metrópoles** (`scraper/portals/metropoles.py`)
- [ ] Implementar scraper do **Correio Braziliense** (`scraper/portals/correio_braziliense.py`)
- [ ] Implementar scraper do **Brasil de Fato** (`scraper/portals/brasil_de_fato.py`)
- [ ] Implementar scraper do **G1** (`scraper/portals/g1.py`)
- [ ] Implementar scraper da **Folha de SP** (`scraper/portals/folha.py`)
- [ ] Adicionar outros portais conforme necessário
- [ ] Testar todos os scrapers e validar inserção no banco

---

## Fase 2 — Rotulagem do Dataset

- [ ] Implementar `labeling/label_tool.py` — CLI que exibe título + trecho e aguarda input (`e` = esquerda, `d` = direita, `s` = skip)
- [ ] Rotular lote inicial de artigos (meta mínima: **500 artigos**, idealmente 1000+)
- [ ] Garantir equilíbrio entre classes (aproximadamente 50% esquerda / 50% direita)
- [ ] Exportar dataset rotulado para `data/processed/dataset.csv`

---

## Fase 3 — EDA e Pré-processamento

- [ ] Exploração inicial no `notebooks/EDA.ipynb`:
  - Distribuição de classes
  - Portais mais frequentes por classe
  - Palavras mais frequentes por classe (WordCloud / frequência)
  - Comprimento médio dos textos
- [ ] Implementar `model/preprocess.py`:
  - Remoção de stopwords em português
  - Limpeza de HTML, URLs, pontuação
  - Normalização (lowercase, remoção de acentos opcional)

---

## Fase 4 — Treinamento do Modelo

- [ ] Implementar `model/train.py`:
  - Pipeline: `TfidfVectorizer` → `LogisticRegression` (ou SVM)
  - Split treino/teste (80/20)
  - Salvar modelo treinado em `model/modelo.pkl`
- [ ] Implementar `model/evaluate.py`:
  - Acurácia, precisão, recall, F1-score
  - Matriz de confusão
  - Análise de erros (quais artigos o modelo erra mais?)
- [ ] Iterar sobre o modelo se necessário (ajuste de hiperparâmetros, features)

---

## Fase 5 — Pipeline de Produção

- [ ] Implementar `scraper/rss_reader.py` — lê os feeds RSS dos portais e retorna lista de artigos novos
- [ ] Implementar `model/predict.py` — carrega `modelo.pkl` e classifica um artigo
- [ ] Implementar `report/generator.py` — formata a saída no padrão WhatsApp (`*DIREITA*` / `*ESQUERDA*`)
- [ ] Implementar `pipeline/run.py` — orquestra: RSS → predict → generator → salva/envia relatório
- [ ] Testar o pipeline completo de ponta a ponta
- [ ] Configurar agendamento (cron ou `schedule`) para rodar diariamente

---

## Fase 6 — Deploy (opcional)

- [ ] Subir o pipeline em um servidor (VPS, Render, Railway, etc.)
- [ ] Integrar envio automático via WhatsApp (Z-API, Twilio, Evolution API)
- [ ] Configurar logs e alertas de erro
- [ ] Monitorar desempenho do modelo ao longo do tempo (data drift)

---

## Backlog / Melhorias Futuras

- [ ] Migrar modelo para BERT em português (`neuralmind/bert-base-portuguese-cased`) quando o dataset for maior
- [ ] Adicionar categoria neutra (notícias sem viés político claro)
- [ ] Interface web simples para visualizar o relatório
- [ ] Versionamento do modelo (MLflow ou similar)
