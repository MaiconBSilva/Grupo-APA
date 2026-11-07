# Guia de Execução — Integrante 2

**Papel:** Backtracking com Branch & Bound & Análise de Árvore de Busca  
**Branch de Trabalho:** `feat/integrante-2-backtracking`  
**Pasta de Código Exclusiva:** `src/backtracking/`  
**Arquivo de Documentação Exclusivo:**  
* `docs/03_backtracking.md`

---

## 1. Visão Geral das Suas Tarefas

Você é o responsável por implementar o algoritmo exato baseado em **Backtracking e Branch & Bound (Ramificação e Poda)**. Seu algoritmo deve demonstrar como a poda inteligente do espaço de estados permite resolver instâncias substancialmente maiores do que a Força Bruta ingênua.

### Suas Responsabilidades:
1. **Implementação:** Desenvolver o algoritmo de **Backtracking com Branch & Bound** para o TSP em Python, obedecendo à interface `TSPResult` e incluindo contadores determinísticos de nós visitados e podas realizadas.
2. **Cálculo da Cota Inferior (Lower Bound):** Implementar uma função rápida de estimativa de custo mínimo para podar ramos inviáveis antes da expansão completa.
3. **Testes Unitários:** Criar o script de teste local testando instâncias de $n = 4 \dots 16$.
4. **Documentação do Algoritmo (Capítulo 3):** Redigir a explicação teórica do paradigma de Backtracking, detalhar o cálculo da cota inferior, colar o código no documento, apresentar a análise de complexidade e comparar a taxa de podas com o total de permutações da Força Bruta.

---

## 2. Passo a Passo de Execução

### Passo 1: Inicializar sua Branch de Trabalho
No terminal, certifique-se de estar com a `main` atualizada e crie sua branch:
```bash
git checkout main
git pull origin main
git checkout -b feat/integrante-2-backtracking
```

---

### Passo 2: Implementar o Branch & Bound com Poda
No arquivo `src/backtracking/branch_and_bound_tsp.py`:
1. Importar `TSPInstance` e `TSPResult` de `src.core.tsp_types`.
2. Modelar a recursão de busca em profundidade:
   * Estado: `(cidade_atual, cidades_visitadas_set, rota_atual, custo_acumulado)`.
3. **Cálculo da Cota Inferior (Lower Bound):**
   * Uma cota inferior simples e rápida: para cada cidade ainda não visitada, somar a menor aresta que sai dela.
   * `estimativa_total = custo_acumulado + cota_inferior_restante`.
4. **Regra de Poda:**
   * Se `estimativa_total >= melhor_custo_global`:
     * Incrementar contador de podas (`pruned_nodes += 1`).
     * Realizar `return` imediato (poda da subárvore).
5. A cada novo nó explorado, incrementar `expanded_nodes += 1`.
6. Ao atingir todas as cidades, adicionar o custo de retorno à cidade `0`. Se for menor que o melhor custo global, atualizar `melhor_rota` e `melhor_custo`.
7. Medir o tempo com `time.perf_counter()`.
8. Retornar `TSPResult` com `operations_count = expanded_nodes` e preencher `extra_metrics={"nodes_pruned": pruned_nodes}`.

---

### Passo 3: Criar e Executar o Script de Teste Local
No arquivo `src/backtracking/test_branch_and_bound.py`:
1. Carregar instâncias `tiny_4`, `small_8` e `medium_12` de `data/instances/`.
2. Executar `solve(instance)`.
3. Validar:
   * O custo ótimo encontrado coincide com a Força Bruta para $n=4$ e $n=8$?
   * A rota começa e termina em `0`?
   * O número de nós expandidos é dramaticamente menor do que $(n-1)!$?
4. Executar no terminal:
   ```bash
   python -m src.backtracking.test_branch_and_bound
   ```

---

### Passo 4: Redigir o Capítulo 3 — Backtracking e Branch & Bound
Edite o arquivo `docs/03_backtracking.md` contendo:
* Conceituação teórica de Backtracking e Branch & Bound.
* Formulação matemática da Cota Inferior utilizada e como ela garante que nenhuma solução ótima seja descartada erroneamente.
* Análise da complexidade assintótica teórica: Pior caso $O(n!)$ no tempo, $O(n)$ no espaço.
* O código-fonte embutido com realce de sintaxe em Python (conforme requisito 49 do edital).
* Tabela comparativa dos testes locais:
  * Colunas: Instância ($n$), Custo Ótimo, Nós Expandidos, Podas Realizadas, Tempo (s).
* Análise qualitativa: mostrar como o Branch & Bound consegue resolver $n=12$ ou $n=15$ em segundos, enquanto a Força Bruta levaria dias.

---

### Passo 5: Submissão do Pull Request (PR)
Suba seus commits para o GitHub e abra um PR para a branch `main`:
```bash
git push -u origin feat/integrante-2-backtracking
```
* Preencha a descrição do PR conforme `Guias/Contrato-de-Regras.md`.
* Solicite a revisão de pelo menos um colega de equipe.
* Realize o **Squash and Merge** após a aprovação.

---

## 3. Checklist de Entregas e Commits

- [ ] **Entrega 2.1:** Implementação da Cota Inferior e Estrutura de Busca
  * Arquivo: `src/backtracking/branch_and_bound_tsp.py`
  * Commit: `feat: cria estrutura recursiva de busca com calculo de cota inferior`
- [ ] **Entrega 2.2:** Lógica de Poda e Retorno `TSPResult`
  * Arquivo: `src/backtracking/branch_and_bound_tsp.py`
  * Commit: `feat: finaliza branch and bound com podas ativas e contagem de nos`
- [ ] **Entrega 2.3:** Testes Unitários e Validação Experimental
  * Arquivo: `src/backtracking/test_branch_and_bound.py`
  * Commit: `test: adiciona testes do branch and bound para n=4 ate n=12`
- [ ] **Entrega 2.4:** Capítulo Documental de Backtracking Completo
  * Arquivo: `docs/03_backtracking.md`
  * Commit: `docs: redige capitulo de backtracking com analise de podas e codigo`
- [ ] **Entrega 2.5:** Pull Request Aberto e Aprovado na `main`
  * Ação no GitHub: PR revisado e mergeado com sucesso.

