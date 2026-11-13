# 6. Estratégias 5 e 6: Algoritmos Gulosos, Aproximados e Heurísticas

**Responsável:** Integrante 4 — Victor Hugo Silva Ferreira (Matrícula: `202304809`)  
**Status:** Aguardando preenchimento

---

## 6.1. Algoritmo Guloso: Vizinho Mais Próximo (*Nearest Neighbor*)
*(Descrição do algoritmo, miopia de decisão local e complexidade O(n^2))*

### Código-Fonte do Vizinho Mais Próximo:
```python
# Inserir o código de src/aproximados/nearest_neighbor_tsp.py
```

---

## 6.2. Algoritmo 2-Aproximado com Árvore Geradora Mínima (MST)
*(Conceito de TSP Métrico, desigualdade triangular e algoritmo de aproximação via MST + DFS tour com atalhos)*

### Demonstração Teórica da Razão de Aproximação ($\alpha \le 2$):
*(Dedução de que w(MST) < C(OPT) e que o tour com atalhos custa no máximo 2 * w(MST) — Cormen et al. [1, Cap. 35])*

### Código-Fonte do 2-Aproximado e Refinamento 2-Opt:
```python
# Inserir o código de src/aproximados/mst_approximation_tsp.py
```

---

## 6.3. Resultados Experimentais: Trade-off Tempo vs. Qualidade da Solução
*(Comparação do desvio percentual em relação ao ótimo do Held-Karp e velocidade em instâncias grandes n=50 e n=100)*

