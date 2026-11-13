# Guia de Execução — Integrante 4

**Responsável:** Victor Hugo Silva Ferreira (Matrícula: `202304809`)  
**Papel:** Algoritmos Gulosos, Aproximados (2-Aproximação via MST) & Heurística 2-Opt  
**Branch de Trabalho:** `feat/integrante-4-aproximados`  
**Pasta de Código Exclusiva:** `src/aproximados/`  
**Arquivo de Documentação Exclusivo:**  
* `docs/06_algoritmos_aproximados.md`

---

## 1. Visão Geral das Suas Tarefas

Você é o responsável por desenvolver as soluções que tornam o TSP tratável para instâncias do mundo real com dezenas, centenas ou milhares de cidades, onde os algoritmos exatos tornam-se computacionalmente inviáveis.

### Suas Responsabilidades:
1. **Algoritmo Guloso:** Implementar o algoritmo do **Vizinho Mais Próximo (*Nearest Neighbor*)** ($O(n^2)$), contabilizando as comparações de distância realizadas.
2. **Algoritmo 2-Aproximado:** Implementar o clássico algoritmo baseado em **Árvore Geradora Mínima (MST)** com percurso em pré-ordem (DFS) e atalhos pela desigualdade triangular, garantindo $C(\pi) \le 2 \cdot C(\pi^*)$.
3. **Heurística de Busca Local (2-Opt):** Implementar o operador de melhoria 2-Opt para desatar arestas cruzadas e refinar as rotas gulosas/aproximadas.
4. **Testes Unitários:** Criar testes locais para instâncias pequenas ($n=10$) comparando com o ótimo, e instâncias médias/grandes ($n=50, 100$).
5. **Documentação de Aproximados (Capítulo 6):** Apresentar a teoria do TSP Métrico, a **demonstração matemática de por que a MST garante razão de aproximação $\alpha \le 2$** (Cormen et al. [1, Cap. 35]), colar os códigos no texto e analisar a qualidade da solução (percentual de desvio do ótimo vs. velocidade instantânea).

---

## 2. Passo a Passo de Execução

### Passo 1: Inicializar sua Branch de Trabalho
```bash
git checkout main
git pull origin main
git checkout -b feat/integrante-4-aproximados
```

---

### Passo 2: Implementar o Vizinho Mais Próximo (Guloso)
No arquivo `src/aproximados/nearest_neighbor_tsp.py`:
1. Importar `TSPInstance` e `TSPResult` de `src.core.tsp_types`.
2. Começar na cidade `0`.
3. Em cada passo, iterar sobre todas as cidades ainda não visitadas para eleger aquela com menor aresta incidente à cidade atual.
   * Incrementar `operations_count += 1` a cada aresta comparada.
4. Adicionar a cidade escolhida à rota e marcá-la como visitada.
5. Ao visitar todas as cidades, retornar à cidade de origem `0`.
6. Medir o tempo com `time.perf_counter()` e retornar `TSPResult`.

---

### Passo 3: Implementar o 2-Aproximado (MST) e Heurística 2-Opt
No arquivo `src/aproximados/mst_approximation_tsp.py`:
1. **Passo A — MST:** Construir a Árvore Geradora Mínima do grafo completo usando o algoritmo de **Prim** em $O(n^2)$.
2. **Passo B — Pré-ordem:** Executar uma Busca em Profundidade (DFS) a partir do nó `0` na MST.
3. **Passo C — Atalhos:** Gerar o ciclo visitando os nós na ordem de descoberta da DFS, pulando vértices já visitados (criando atalhos diretos garantidos pela desigualdade triangular) e retornando a `0`.
4. **Passo D — Refinamento 2-Opt (Opcional/Bônus):** Percorrer pares de arestas $(u, v)$ e $(x, y)$. Se inverter o segmento intermediário reduzir o custo, aplicar a troca até convergência local.
5. Contabilizar operações de relaxamento de arestas no Prim e swaps no 2-Opt.
6. Retornar `TSPResult`.

---

### Passo 4: Criar e Executar o Script de Teste Local
No arquivo `src/aproximados/test_aproximados.py`:
1. Carregar instâncias `small_8`, `medium_16` e instâncias maiores geradas em `data/instances/`.
2. Executar tanto o Vizinho Mais Próximo quanto o 2-Aproximado/2-Opt.
3. Validar:
   * As rotas são ciclos hamiltonianos válidos (visitam todas as cidades sem repetição e retornam a `0`)?
   * O custo do 2-Aproximado é de fato menor que o dobro do custo ótimo conhecido?
   * O tempo de execução é inferior a alguns milissegundos mesmo para instâncias de dezenas de cidades?
4. Rodar o teste no terminal:
   ```bash
   python -m src.aproximados.test_aproximados
   ```

---

### Passo 5: Redigir o Capítulo 6 — Algoritmos Gulosos e Aproximados
Edite o arquivo `docs/06_algoritmos_aproximados.md` contendo:
* Conceito de Heurísticas Construtivas vs. Algoritmos de Aproximação com garantia formal.
* Definição de TSP Métrico e desigualdade triangular.
* **Demonstração Matemática Formal do Fator $\alpha \le 2$:**
  * O custo da MST é menor que o ciclo ótimo ($w(MST) < C(\pi^*)$).
  * O passeio que percorre cada aresta da MST duas vezes tem custo $2 \cdot w(MST)$.
  * A introdução de atalhos diretos não aumenta o custo devido à desigualdade triangular, logo $C(\text{Tour}) \le 2 \cdot C(\pi^*)$.
* Códigos-fonte embutidos com destaque de sintaxe em Python (requisito 49).
* Tabela experimental comparando a qualidade da rota (Custo do Guloso vs. Custo do 2-Aproximado vs. Ótimo exato) e o ganho monumental de tempo de execução.

---

### Passo 6: Submissão do Pull Request (PR)
Suba seus commits e abra um PR para a `main`:
```bash
git push -u origin feat/integrante-4-aproximados
```
* Preencha o template de PR e solicite a revisão de um colega.
* Realize o **Squash and Merge** após a aprovação.

---

## 3. Checklist de Entregas e Commits

- [ ] **Entrega 4.1:** Implementação do Algoritmo Guloso (Vizinho Mais Próximo)
  * Arquivo: `src/aproximados/nearest_neighbor_tsp.py`
  * Commit: `feat: implementa algoritmo guloso do vizinho mais proximo com retorno TSPResult`
- [ ] **Entrega 4.2:** Implementação do 2-Aproximado com MST (Prim + DFS) e 2-Opt
  * Arquivo: `src/aproximados/mst_approximation_tsp.py`
  * Commit: `feat: implementa 2-aproximado com arvore geradora minima e busca local 2-opt`
- [ ] **Entrega 4.3:** Testes Locais e Avaliação de Desempenho
  * Arquivo: `src/aproximados/test_aproximados.py`
  * Commit: `test: adiciona testes comparativos para guloso e aproximado`
- [ ] **Entrega 4.4:** Capítulo Documental de Aproximados Completo
  * Arquivo: `docs/06_algoritmos_aproximados.md`
  * Commit: `docs: redige capitulo de aproximados com prova do fator 2 e analise de trade-off`
- [ ] **Entrega 4.5:** Pull Request Aprovado na `main`
  * Ação no GitHub: PR revisado e mergeado com sucesso.

