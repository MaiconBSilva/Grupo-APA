# 7. Análise de Resultados e Comparativo Global

**Responsáveis:** Todo o grupo (Consolidação com script unificado)  
**Status:** Aguardando execução do script `scripts/run_comparison.py` após o merge de todas as branches

---

## 7.1. Tabela Comparativa Consolidada

| Instância | $n$ | Força Bruta ($t$ / ops) | Backtracking B&B ($t$ / ops) | Held-Karp PD ($t$ / ops) | Guloso ($t$ / erro) | 2-Aproximado MST ($t$ / erro) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| tiny_4 | 4 | | | | | |
| small_8 | 8 | | | | | |
| medium_12 | 12 | Estourou | | | | |
| medium_16 | 16 | Estourou | | | | |
| medium_20 | 20 | Estourou | Estourou | | | |
| berlin52 | 52 | Estourou | Estourou | Estourou (RAM) | | |
| large_50 | 50 | Estourou | Estourou | Estourou (RAM) | | |
| large_100 | 100 | Estourou | Estourou | Estourou (RAM) | | |

> **Nota:** A instância `berlin52` é canônica da TSPLIB. Seu custo ótimo global publicado na literatura é de **7542**.

---

## 7.2. Gráficos de Desempenho e Discussão
*(Execute `python scripts/plot_results.py` para gerar as figuras automaticamente em `docs/images/`)*

![Comparativo de Tempo de Execução](images/comparativo_tempo_execucao.png)

![Comparativo de Qualidade da Rota](images/comparativo_custo_solucao.png)

