# Guia de Execução — Integrante 3

**Responsável:** Maicon Brendo da Silva (Matrícula: `202204199`)  
**Papel:** Programação Dinâmica (Held-Karp) & Inviabilidade de Divisão e Conquista  
**Branch de Trabalho:** `feat/integrante-3-prog-dinamica`  
**Pasta de Código Exclusiva:** `src/dinamica/`  
**Arquivos de Documentação Exclusivos:**  
* `docs/04_inviabilidade_dc.md`  
* `docs/05_programacao_dinamica.md`

---

## 1. Visão Geral das Suas Tarefas

Você é o responsável pelo algoritmo exato teoricamente mais elegante e eficiente em tempo assintótico: o **Algoritmo de Bellman-Held-Karp** via **Programação Dinâmica**. Além disso, você responderá formalmente à exigência do edital (item 33) documentando por que o paradigma de Divisão e Conquista não é viável para a solução ótima do TSP.

### Suas Responsabilidades:
1. **Justificativa Teórica de Divisão e Conquista (Capítulo 4):** Redigir a fundamentação matemática e bibliográfica provando a inviabilidade de Divisão e Conquista para a solução exata ótima do TSP (ausência de subproblemas disjuntos independentes e explosão na etapa de combinação).
2. **Implementação da Programação Dinâmica:** Codificar o algoritmo de Held-Karp utilizando representação de subconjuntos por **máscara de bits (*bitmask*)**, memoização e reconstrução do caminho ótimo, retornando o objeto padronizado `TSPResult`.
3. **Testes Unitários:** Validar seu algoritmo em instâncias de $n = 4 \dots 20$, monitorando a contagem de subproblemas em cache e tempo.
4. **Documentação de Programação Dinâmica (Capítulo 5):** Apresentar a relação de recorrência formal, a complexidade de tempo $O(n^2 2^n)$ e espaço $O(n 2^n)$, embutir o código no texto e discutir os limites de memória RAM para $n > 22$.

---

## 2. Passo a Passo de Execução

### Passo 1: Inicializar sua Branch de Trabalho
```bash
git checkout main
git pull origin main
git checkout -b feat/integrante-3-prog-dinamica
```

---

### Passo 2: Redigir a Inviabilidade de Divisão e Conquista
Edite o arquivo `docs/04_inviabilidade_dc.md`:
* Atender estritamente ao **item 33 do edital do professor**: *"Caso não seja tecnicamente viável resolver o problema utilizando qualquer uma das estratégias... deverão ser apresentadas justificativas fundamentadas, acompanhadas de referências bibliográficas pertinentes"*.
* Estruturar a argumentação:
  1. As premissas do paradigma D&C (Dividir em partes independentes, Conquistar e Combinar eficientemente — Cormen et al. [1]).
  2. A dependência global de conectividade do ciclo no TSP: a remoção de arestas de corte cria $O(|V_1|! \times |V_2|!)$ combinações para religar os subciclos.
  3. A inviabilidade de garantir a otimalidade global sem inspecionar todas as combinações de fronteira.
  4. Citações bibliográficas formais (Cormen [1], Kleinberg & Tardos).

---

### Passo 3: Implementar o Algoritmo de Held-Karp
No arquivo `src/dinamica/held_karp_tsp.py`:
1. Importar `TSPInstance` e `TSPResult` de `src.core.tsp_types`.
2. Utilizar representação inteira para o subconjunto de cidades visitadas (*bitmask*):
   * O bit `i` é `1` se a cidade `i` está no subconjunto $S$.
   * A cidade inicial `0` está sempre presente (`mask | 1`).
3. Tabela de memoização: `memo[(mask, u)] = (menor_custo, vertice_anterior)`.
4. Relação de recorrência:
   $$C(S, v) = \min_{u \in S \setminus \{v\}} \{ C(S \setminus \{v\}, u) + w(u, v) \}$$
5. Incrementar o contador de operações (`operations_count += 1`) a cada novo par `(mask, v)` calculado e inserido no cache.
6. Reconstruir a rota ótima percorrendo os ponteiros do vértice anterior a partir de `(mask_completa, ultimo_vertice)`.
7. Medir o tempo com `time.perf_counter()` e retornar `TSPResult`.

---

### Passo 4: Criar e Executar o Script de Teste Local
No arquivo `src/dinamica/test_held_karp.py`:
1. Carregar as instâncias `tiny_4`, `small_8`, `medium_12` e `medium_16` de `data/instances/`.
2. Executar `solve(instance)`.
3. Validar:
   * O custo ótimo coincide com a Força Bruta ($n=4, 8$) e com o Backtracking ($n=12, 16$)?
   * O número de estados únicos calculados é da ordem de $n 2^{n-1}$?
   * O tempo para $n=16$ é de fração de segundo?
4. Rodar o teste no terminal:
   ```bash
   python -m src.dinamica.test_held_karp
   ```

---

### Passo 5: Redigir o Capítulo 5 — Programação Dinâmica
Edite o arquivo `docs/05_programacao_dinamica.md` contendo:
* Conceito de Programação Dinâmica aplicado ao TSP e a técnica de bitmask.
* Dedução da complexidade teórica: Tempo $O(n^2 2^n)$ e Espaço $O(n 2^n)$.
* O código-fonte embutido com realce de sintaxe em Python (requisito 49).
* Tabela experimental local mostrando o crescimento do tempo e da memória até $n = 18$ ou $20$.
* Discussão sobre o gargalo de memória (*Memory Overhead*) para instâncias maiores.

---

### Passo 6: Submissão do Pull Request (PR)
Suba seus commits e abra um PR para a `main`:
```bash
git push -u origin feat/integrante-3-prog-dinamica
```
* Preencha o template de PR e solicite a revisão de um colega.
* Após a aprovação, realize o **Squash and Merge**.

---

## 3. Checklist de Entregas e Commits

- [ ] **Entrega 3.1:** Documentação da Inviabilidade de Divisão e Conquista
  * Arquivo: `docs/04_inviabilidade_dc.md`
  * Commit: `docs: formaliza justificativa bibliografica da inviabilidade de divisao e conquista no TSP`
- [ ] **Entrega 3.2:** Implementação do Algoritmo de Held-Karp com Bitmask
  * Arquivo: `src/dinamica/held_karp_tsp.py`
  * Commit: `feat: implementa held-karp com bitmask memoization e reconstrucao de rota`
- [ ] **Entrega 3.3:** Testes Locais e Validação de Otimização
  * Arquivo: `src/dinamica/test_held_karp.py`
  * Commit: `test: valida held-karp em instancias de n=4 ate n=16`
- [ ] **Entrega 3.4:** Capítulo Documental de Programação Dinâmica Completo
  * Arquivo: `docs/05_programacao_dinamica.md`
  * Commit: `docs: adiciona capitulo de programacao dinamica com analise assintotica e codigo`
- [ ] **Entrega 3.5:** Pull Request Aprovado na `main`
  * Ação no GitHub: PR revisado e mergeado.

