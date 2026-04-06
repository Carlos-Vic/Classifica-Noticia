# Classifica Notícia — To-Do

Projeto de coleta, rotulagem e classificação automática de notícias políticas brasileiras.

---

## Fase 1 — Setup e Coleta de Dados

- [x] Criar ambiente virtual e instalar dependências
- [x] Criar banco de dados (migrado de SQLite para PostgreSQL via Supabase)
- [x] Implementar `scraper/base_scraper.py` com lógica base de request + parsing
- [x] Implementar scraper do **G1**
- [x] Implementar scraper do **Jornal de Brasília**
- [x] Implementar scraper do **CNN Brasil**
- [x] Implementar scraper do **Metrópoles**
- [x] Implementar scraper do **Correio Braziliense**
- [x] Implementar scraper do **Brasil de Fato**
- [x] Implementar scraper do **Vero Notícias**
- [x] Implementar scraper do **blog CB Poder** (mesmo domínio do Correio Braziliense)

---

## Fase 2 — Interface Streamlit

- [x] Página de **Coleta Manual** — coleta por URL com detecção automática de portal e rotulagem
- [x] Página de **Coleta em Lote** — coleta via bloco de texto com múltiplas URLs e relatório de resultado
- [x] Página de **Artigos** — listagem com filtros por portal e viés, paginação
- [x] Página de **Dashboard** — gráficos de viés geral, viés por portal e portais sem scraper mais demandados
- [ ] Página de **Início** — apresentação do projeto e descrição das páginas
- [ ] Deploy no Streamlit Community Cloud com acesso restrito por e-mail

---

## Fase 3 — Rotulagem do Dataset

- [ ] Rotular lote inicial de artigos (meta mínima: **500 artigos**, idealmente 1000+)
- [ ] Garantir equilíbrio entre classes (~50% esquerda / ~50% direita)
- [ ] Exportar dataset rotulado para `data/processed/dataset.csv`

---

## Fase 4 — EDA e Pré-processamento

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

## Fase 5 — Treinamento do Modelo

- [ ] Implementar `model/train.py`:
  - Pipeline: `TfidfVectorizer` → `LogisticRegression` (ou SVM)
  - Split treino/teste (80/20)
  - Salvar modelo treinado em `model/modelo.pkl`
- [ ] Implementar `model/evaluate.py`:
  - Acurácia, precisão, recall, F1-score
  - Matriz de confusão
  - Análise de erros
- [ ] Iterar sobre o modelo se necessário (ajuste de hiperparâmetros, features)

---

## Fase 6 — Pipeline de Produção

- [ ] Implementar `scraper/rss_reader.py` — lê feeds RSS e retorna lista de artigos novos
- [ ] Implementar `model/predict.py` — carrega `modelo.pkl` e classifica um artigo
- [ ] Implementar `report/generator.py` — formata saída no padrão WhatsApp (`*DIREITA*` / `*ESQUERDA*`)
- [ ] Implementar `pipeline/run.py` — orquestra: RSS → predict → generator → salva/envia relatório
- [ ] Testar pipeline completo de ponta a ponta
- [ ] Configurar agendamento (cron ou `schedule`) para rodar diariamente

---

## Fase 7 — Deploy do Pipeline

- [ ] Subir o pipeline em um servidor (VPS, Render, Railway, etc.)
- [ ] Integrar envio automático via WhatsApp (Z-API, Twilio, Evolution API)
- [ ] Configurar logs e alertas de erro
- [ ] Monitorar desempenho do modelo ao longo do tempo (data drift)

---

## Backlog / Melhorias Futuras

- [ ] Migrar modelo para BERT em português (`neuralmind/bert-base-portuguese-cased`) quando o dataset for maior
- [ ] Adicionar categoria neutra (notícias sem viés político claro)
- [ ] Versionamento do modelo (MLflow ou similar)
