# 5. Estratégia 4: Programação Dinâmica (Algoritmo de Bellman-Held-Karp)

**Responsável:** Integrante 3 — Maicon Brendo da Silva (Matrícula: `202204199`)  
**Status:** Concluído

---

## 5.1. Descrição do Paradigma, Subestrutura Ótima e Relação de Recorrência

A **Programação Dinâmica (PD)** resolve problemas de otimização combinatória explorando duas propriedades estruturais fundamentais [1, Cap. 15; 2, 5]:

1. **Subestrutura ótima:** qualquer subcaminho de um ciclo hamiltoniano ótimo no Problema do Caixeiro Viajante (TSP) é, por si só, um caminho simples de custo mínimo entre suas extremidades sobre o mesmo conjunto intermediário de vértices.
2. **Sobreposição de subproblemas:** diversas permutações distintas compartilham exatamente o mesmo conjunto de cidades já visitadas e a mesma cidade final. Ao memoizar o menor custo para cada par `(subconjunto, último vértice)`, evita-se recomputar exponencialmente os mesmos prefixos.

### Formulação Matemática (Bellman-Held-Karp)

Proposta independentemente por Bellman [6] e por Held e Karp [3] em 1962, a formulação fixa sem perda de generalidade a cidade `0` como origem do ciclo e define o estado $C(S, v)$ como o **menor custo de um caminho simples** que:
- inicia na cidade `0`;
- visita exatamente o subconjunto de cidades $S \subseteq \{0, 1, \dots, n - 1\}$, com $0 \in S$ e $v \in S$;
- termina na cidade $v \neq 0$.

A recorrência é composta por três etapas:

1. **Caso base ($|S| = 2$, isto é, $S = \{0, v\}$):**
   $$C(\{0, v\}, v) = w(0, v) \quad \forall v \in \{1, \dots, n - 1\}$$
2. **Transição (*bottom-up* para $|S| = 3, \dots, n$):**
   $$C(S, v) = \min_{u \in S \setminus \{0, v\}} \Big( C(S \setminus \{v\}, u) + w(u, v) \Big)$$
3. **Fechamento do ciclo hamiltoniano ($S = V = \{0, 1, \dots, n - 1\}$):**
   $$C^* = \min_{v \in \{1, \dots, n - 1\}} \Big( C(V, v) + w(v, 0) \Big)$$

### Codificação por Máscara de Bits (*Bitmask*)

Como a cidade `0` pertence obrigatoriamente a todos os estados $S$, o subconjunto $S \setminus \{0\} \subseteq \{1, \dots, n - 1\}$ é codificado por um inteiro `submask` de $(n - 1)$ bits, em que o bit $j$ ($0 \le j < n - 1$) vale `1` se e somente se a cidade $j + 1$ pertence a $S$. Para $n = 4$, por exemplo, `submask = 0b101` (decimal `5`) representa $S = \{0, 1, 3\}$.

| Operação Bitwise | Expressão em Python | Significado no Algoritmo |
| :--- | :--- | :--- |
| Inserir cidade `v` | `submask \| (1 << (v - 1))` | Forma o conjunto $S \cup \{v\}$ |
| Remover cidade `v` | `submask ^ lsb_v` | Obtém o subconjunto anterior $S \setminus \{v\}$ |
| Extrair bit menos significativo | `lsb = rem & -rem` | Itera apenas sobre cidades ativas em $S \setminus \{0\}$ |
| Converter bit em índice | `lsb.bit_length() - 1` | Mapeia o bit ativo para o índice `v_idx = v - 1` |
| Conjunto completo $V \setminus \{0\}$ | `(1 << (n - 1)) - 1` | Máscara final para fechamento do ciclo na cidade `0` |

---

## 5.2. Implementação do Código-Fonte

Em conformidade com o Requisito 49 do edital, apresenta-se abaixo o código-fonte integral de `src/dinamica/held_karp_tsp.py`:

```python
"""
Implementação do Algoritmo de Bellman-Held-Karp via Programação Dinâmica para o TSP.
Responsável: Integrante 3 — Maicon Brendo da Silva (Matrícula: 202204199)
Complexidade Teórica: Tempo Theta(n^2 * 2^n), Espaço Theta(n * 2^n).
"""

import math
import time
from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost


def _reconstruct_route(
    parent: list[int],
    full_submask: int,
    last_city: int,
    stride: int,
) -> list[int]:
    """
    Reconstrói o ciclo hamiltoniano ótimo a partir da tabela de predecessores.

    Args:
        parent: Tabela linearizada de predecessores indexada por (submask * stride + v_idx).
        full_submask: Máscara completa dos vértices {1, ..., n - 1}.
        last_city: Última cidade visitada antes do retorno à cidade 0.
        stride: Número de cidades excluindo a origem (n - 1).

    Returns:
        Lista de inteiros representando o ciclo completo [0, ..., 0] com n + 1 elementos.
    """
    reversed_route = [0]
    curr_submask = full_submask
    curr_city = last_city

    while curr_city != 0:
        reversed_route.append(curr_city)
        curr_idx = curr_city - 1
        prev_city = parent[curr_submask * stride + curr_idx]
        curr_submask ^= 1 << curr_idx
        curr_city = prev_city

    reversed_route.append(0)
    return reversed_route[::-1]


def solve(instance: TSPInstance) -> TSPResult:
    """
    Resolve o TSP utilizando o algoritmo exato de Bellman-Held-Karp com bitmask.

    A origem é fixada na cidade 0. Cada subconjunto S contendo 0 é representado
    por uma máscara `submask` de (n - 1) bits para os vértices {1, ..., n - 1},
    onde o bit j indica a presença da cidade (j + 1).

    Args:
        instance: Instância do TSP contendo dimensão e matriz de distâncias.

    Returns:
        TSPResult: Resultado padronizado com rota ótima, custo, tempo de execução
        e contagens determinísticas de estados memoizados e transições avaliadas.
    """
    start_time = time.perf_counter()
    n = instance.dimension
    dist = instance.distance_matrix

    if n == 0:
        elapsed_time = time.perf_counter() - start_time
        return TSPResult(
            algorithm_name="Held_Karp_PD",
            instance_name=instance.name,
            dimension=n,
            best_route=[],
            best_cost=0.0,
            execution_time_seconds=elapsed_time,
            operations_count=0,
            extra_metrics={"memoized_states": 0, "transitions_evaluated": 0},
        )

    if n == 1:
        elapsed_time = time.perf_counter() - start_time
        return TSPResult(
            algorithm_name="Held_Karp_PD",
            instance_name=instance.name,
            dimension=n,
            best_route=[0, 0],
            best_cost=0.0,
            execution_time_seconds=elapsed_time,
            operations_count=1,
            extra_metrics={"memoized_states": 1, "transitions_evaluated": 0},
        )

    if n == 2:
        best_route = [0, 1, 0]
        best_cost = compute_tour_cost(best_route, dist)
        elapsed_time = time.perf_counter() - start_time
        return TSPResult(
            algorithm_name="Held_Karp_PD",
            instance_name=instance.name,
            dimension=n,
            best_route=best_route,
            best_cost=best_cost,
            execution_time_seconds=elapsed_time,
            operations_count=1,
            extra_metrics={"memoized_states": 1, "transitions_evaluated": 0},
        )

    stride = n - 1
    num_submasks = 1 << stride
    inf = math.inf

    dp = [inf] * (num_submasks * stride)
    parent = [0] * (num_submasks * stride)

    masks_by_size: list[list[int]] = [[] for _ in range(stride + 1)]
    for submask in range(1, num_submasks):
        masks_by_size[submask.bit_count()].append(submask)

    states_computed = 0
    transitions_evaluated = 0

    # Caso base: |S| = 2 -> subconjuntos {0, v} com submask de tamanho 1
    for v_idx in range(stride):
        submask = 1 << v_idx
        idx = submask * stride + v_idx
        dp[idx] = dist[0][v_idx + 1]
        parent[idx] = 0
        states_computed += 1

    # Recorrência bottom-up por cardinalidade de S \ {0}
    for size in range(2, stride + 1):
        for submask in masks_by_size[size]:
            base_offset = submask * stride
            rem_v = submask
            while rem_v:
                lsb_v = rem_v & -rem_v
                v_idx = lsb_v.bit_length() - 1
                rem_v ^= lsb_v

                prev_submask = submask ^ lsb_v
                prev_offset = prev_submask * stride
                v_city = v_idx + 1

                best_val = inf
                best_u_city = 0

                rem_u = prev_submask
                while rem_u:
                    lsb_u = rem_u & -rem_u
                    u_idx = lsb_u.bit_length() - 1
                    rem_u ^= lsb_u

                    candidate = dp[prev_offset + u_idx] + dist[u_idx + 1][v_city]
                    transitions_evaluated += 1
                    if candidate < best_val:
                        best_val = candidate
                        best_u_city = u_idx + 1

                dp[base_offset + v_idx] = best_val
                parent[base_offset + v_idx] = best_u_city
                states_computed += 1

    # Fechamento do ciclo hamiltoniano retornando à cidade 0
    full_submask = num_submasks - 1
    full_offset = full_submask * stride
    best_tour_val = inf
    best_last_city = 1

    for v_idx in range(stride):
        v_city = v_idx + 1
        candidate = dp[full_offset + v_idx] + dist[v_city][0]
        if candidate < best_tour_val:
            best_tour_val = candidate
            best_last_city = v_city

    best_route = _reconstruct_route(parent, full_submask, best_last_city, stride)
    best_cost = compute_tour_cost(best_route, dist)
    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="Held_Karp_PD",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=best_cost,
        execution_time_seconds=elapsed_time,
        operations_count=states_computed,
        extra_metrics={
            "memoized_states": states_computed,
            "transitions_evaluated": transitions_evaluated,
        },
    )
```

### Estrutura Lógica da Implementação

- **Casos de borda ($n \in \{0, 1, 2\}$):** retornam imediatamente o ciclo trivial e contagens exatas sem alocar tabelas de programação dinâmica.
- **Tabelas linearizadas (`dp` e `parent`):** em vez de dicionários com chaves em tupla `(mask, v)`, os estados são armazenados em vetores unidimensionais de tamanho $(n - 1) \cdot 2^{n - 1}$, reduzindo o custo de *hashing* e o consumo de memória em Python.
- **Agrupamento por cardinalidade (`masks_by_size`):** garante que todos os subproblemas de tamanho $|S| - 1$ já estejam resolvidos antes do cálculo dos estados de tamanho $|S|$ (*bottom-up*).
- **Extração de bits ativos (`rem & -rem`):** percorre exclusivamente os vértices pertencentes ao subconjunto atual, evitando iterações ociosas sobre cidades ausentes.
- **Reconstrução via `parent`:** a função auxiliar `_reconstruct_route` retrocede de `full_submask` até a cidade `0`, produzindo a rota `[0, ..., 0]` com $n + 1$ elementos.

---

## 5.3. Análise da Complexidade Computacional (Tempo e Espaço)

### Complexidade de Espaço: $\Theta(n \cdot 2^n)$

Para cada cardinalidade $k = |S|$ com $2 \le k \le n$, existem $\binom{n - 1}{k - 1}$ escolhas para os $(k - 1)$ vértices distintos de `0` em $S$, e para cada subconjunto há $(k - 1)$ escolhas possíveis para o último vértice $v \in S \setminus \{0\}$. Utilizando a identidade binomial $m \binom{n - 1}{m} = (n - 1) \binom{n - 2}{m - 1}$ com $m = k - 1$, o número exato de estados únicos calculados para $n \ge 2$ é:

$$\text{Estados}(n) = \sum_{k=2}^{n} \binom{n - 1}{k - 1} (k - 1) = (n - 1) \sum_{m=1}^{n - 1} \binom{n - 2}{m - 1} = (n - 1) \cdot 2^{n - 2} = \Theta(n \cdot 2^n)$$

As tabelas linearizadas `dp` e `parent` alocam $(n - 1) \cdot 2^{n - 1}$ posições, mantendo a ordem assintótica espacial de $\Theta(n \cdot 2^n)$ [3, 5].

### Complexidade de Tempo: $\Theta(n^2 \cdot 2^n)$

Nos estados de cardinalidade $k \ge 3$, para cada par $(S, v)$ há exatamente $(k - 2)$ predecessores candidatos $u \in S \setminus \{0, v\}$. Aplicando a identidade $m(m - 1)\binom{n - 1}{m} = (n - 1)(n - 2)\binom{n - 3}{m - 2}$ para $m = k - 1$, o total exato de transições avaliadas na recorrência para $n \ge 3$ é:

$$\text{Transições}(n) = \sum_{k=3}^{n} \binom{n - 1}{k - 1} (k - 1)(k - 2) = (n - 1)(n - 2) \sum_{m=2}^{n - 1} \binom{n - 3}{m - 2} = (n - 1)(n - 2) \cdot 2^{n - 3} = \Theta(n^2 \cdot 2^n)$$

Somando os $(n - 1)$ casos base, as $(n - 1)$ verificações de fechamento do ciclo e os $O(n)$ passos de reconstrução da rota, a complexidade temporal assintótica do algoritmo de Bellman-Held-Karp é estritamente $\Theta(n^2 \cdot 2^n)$ [3, 6].

### Comparação Numérica com a Força Bruta

Embora ainda exponencial, $\Theta(n^2 \cdot 2^n)$ representa uma redução drástica em relação ao crescimento fatorial $\Theta(n!)$ — ou $(n - 1)!$ permutações fixando a origem — da Força Bruta [1, 2]:

- Para **$n = 12$**: $11! = 39.916.800$ rotas na Força Bruta contra apenas **$11.264$ estados** no Held-Karp (redução de $3.543\times$).
- Para **$n = 16$**: $15! \approx 1{,}307 \times 10^{12}$ rotas contra **$245.760$ estados** (redução superior a $5{,}3 \times 10^6$ vezes).
- Para **$n = 20$**: $19! \approx 1{,}216 \times 10^{17}$ rotas contra **$4.980.736$ estados** — redução superior a **10 ordens de grandeza**, tornando viável encontrar o ótimo exato em poucos segundos.

---

## 5.4. Resultados Experimentais Locais e Limites de Memória RAM

### Ambiente de Execução

Todos os experimentos locais desta seção foram executados na seguinte configuração de hardware e software:

- **Processador (CPU):** AMD Ryzen 5 7600 6-Core Processor (12 threads lógicos, clock base ~3,79 GHz)
- **Memória RAM:** 30,96 GiB utilizáveis (~32 GB instalados)
- **Sistema Operacional:** Windows 11 (`Windows-11-10.0.26200-SP0`, arquitetura `AMD64`)
- **Interpretador:** Python 3.14.7 (64-bit)

### Tabela de Resultados Experimentais ($n = 4$ até $n = 20$)

Os valores abaixo foram obtidos diretamente pela execução da suíte `py -m src.dinamica.test_held_karp`, com validação de otimalidade exata contra Força Bruta para $n \le 10$ e verificação exata das fórmulas de estados e transições para todas as instâncias:

| Instância | $n$ | Custo Ótimo | Tempo (s) | Estados Memoizados | Transições Avaliadas |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `tiny_4` | 4 | 226,30 | 0,000024 | 12 | 12 |
| `small_6` | 6 | 147,14 | 0,000058 | 80 | 160 |
| `small_8` | 8 | 277,32 | 0,000269 | 448 | 1.344 |
| `medium_10` | 10 | 312,11 | 0,002123 | 2.304 | 9.216 |
| `medium_12` | 12 | 280,79 | 0,009166 | 11.264 | 56.320 |
| `medium_16` | 16 | 368,30 | 0,302392 | 245.760 | 1.720.320 |
| `medium_20` | 20 | 379,34 | 6,572496 | 4.980.736 | 44.826.624 |

### Análise da Curva Empírica e Gargalo de Memória (*Memory Overhead*)

Observa-se na tabela que até $n = 12$ o algoritmo executa em menos de **10 milissegundos**, e mesmo para $n = 16$ (onde a Força Bruta já é computacionalmente proibitiva) o ótimo exato é encontrado em **0,302 s**. Ao saltar de $n = 16$ para $n = 20$, o número de estados cresce de $245.760$ para $4.980.736$ ($\approx 20{,}27\times$), enquanto as transições saltam de $1{,}72 \times 10^6$ para $44{,}83 \times 10^6$ ($\approx 26{,}06\times$), elevando o tempo para **6,572 s**.

Diferentemente da Força Bruta e do Backtracking — que utilizam apenas $O(n)$ de memória para a pilha de recursão e são limitados exclusivamente por **tempo de CPU** —, o principal gargalo prático do algoritmo de Bellman-Held-Karp para $n > 22$ passa a ser a **memória RAM** ($\Theta(n \cdot 2^n)$):

- **$n = 25$:** $(24) \cdot 2^{23} = 201.326.592$ estados únicos ($402{,}65 \times 10^6$ posições nas tabelas `dp` e `parent`), consumindo cerca de **11–12 GB de RAM** em Python (~24 GB+ já em $n = 26$, aproximando-se do limite físico de 30,96 GiB da máquina de testes).
- **`large_50` ($n = 50$):** $(49) \cdot 2^{48} \approx 1{,}38 \times 10^{16}$ estados. Mesmo se cada estado ocupasse apenas 1 byte, seriam necessários aproximadamente **13,8 Petabytes de RAM**.
- **`berlin52` ($n = 52$):** $(51) \cdot 2^{50} \approx 5{,}74 \times 10^{16}$ estados (**~57,4 Petabytes**).
- **`large_100` ($n = 100$):** $(99) \cdot 2^{98} \approx 3{,}14 \times 10^{31}$ estados — escala fisicamente impossível de armazenar em qualquer arquitetura computacional existente.

Esses cálculos demonstram por que o limite prático `max_n = 20` adotado no *runner* comparativo do projeto é tecnicamente adequado e fundamentam os registros classificados como `"Estourou (RAM)"` para instâncias de médio/grande porte no Capítulo 7.

As referências [1], [2], [3], [5] e [6] citadas neste capítulo encontram-se consolidadas na Seção 8.2 do relatório.
