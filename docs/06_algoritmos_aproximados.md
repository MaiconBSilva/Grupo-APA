# 6. Estratégias 5 e 6: Algoritmos Gulosos, Aproximados e Heurísticas

**Responsável:** Integrante 4 — Victor Hugo Silva Ferreira (Matrícula: `202304809`)  
**Status:** Concluído

Este capítulo apresenta duas estratégias para produzir ciclos hamiltonianos em tempo polinomial: a heurística construtiva do Vizinho Mais Próximo e a aproximação com garantia formal baseada em Árvore Geradora Mínima (MST). Também descreve o refinamento local 2-Opt e compara os resultados obtidos nas instâncias do projeto.

## 6.1. Algoritmo Guloso: Vizinho Mais Próximo (*Nearest Neighbor*)

Uma heurística construtiva monta uma solução passo a passo por decisões locais. No Vizinho Mais Próximo, a rota começa na cidade `0`; em cada etapa, o algoritmo escolhe a cidade ainda não visitada cuja distância até a cidade atual seja mínima. Depois de visitar todas as cidades, fecha o ciclo retornando à origem.

Essa escolha é gulosa porque otimiza apenas o próximo deslocamento, sem avaliar o efeito da decisão sobre o restante da rota. Por isso, o algoritmo é rápido, mas **não possui garantia de aproximação**: uma escolha localmente barata pode conduzir a uma rota globalmente cara. Empates são resolvidos de forma determinística pela ordem crescente dos índices das cidades.

Em uma instância com $n$ cidades, o algoritmo examina até $n-1$, $n-2$, ..., $1$ candidatos. Portanto, o número de comparações de distâncias é:

$$
\sum_{k=1}^{n-1} k = \frac{n(n-1)}{2},
$$

resultando em tempo $O(n^2)$ e espaço auxiliar $O(n)$.

### Código-fonte do Vizinho Mais Próximo

```python
"""
Implementação do Algoritmo Guloso do Vizinho Mais Próximo (Nearest Neighbor) para o TSP.
Responsável: Integrante 4
Complexidade Teórica: Tempo O(n^2), Espaço O(n).
"""

import time
from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost


def solve(instance: TSPInstance) -> TSPResult:
    """
    Resolve o TSP utilizando a heurística gulosa do Vizinho Mais Próximo.

    Inicia na cidade 0 e a cada passo escolhe a cidade ainda não visitada com menor distância à atual.

    Retorna:
        TSPResult: Resultado padronizado com contagem de arestas comparadas.
    """
    start_time = time.perf_counter()
    n = instance.dimension
    dist = instance.distance_matrix
    best_route = [0] if n > 0 else []
    visited = [False] * n
    if n > 0:
        visited[0] = True

    comparisons_count = 0
    current_city = 0

    while len(best_route) < n:
        nearest_city = None
        nearest_distance = None

        for candidate in range(n):
            if visited[candidate]:
                continue

            distance = dist[current_city][candidate]
            comparisons_count += 1
            if nearest_distance is None or distance < nearest_distance:
                nearest_city = candidate
                nearest_distance = distance

        if nearest_city is None:
            raise ValueError("Não foi possível encontrar uma cidade não visitada.")

        best_route.append(nearest_city)
        visited[nearest_city] = True
        current_city = nearest_city

    if n > 0:
        best_route.append(0)

    best_cost = compute_tour_cost(best_route, instance.distance_matrix)

    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="Vizinho_Mais_Proximo",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=best_cost,
        execution_time_seconds=elapsed_time,
        operations_count=comparisons_count,
        extra_metrics={"distance_comparisons": comparisons_count}
    )
```

## 6.2. Algoritmo 2-Aproximado com Árvore Geradora Mínima (MST)

### TSP métrico

A garantia de aproximação da MST requer um **TSP métrico**: o grafo é completo, as distâncias são não negativas e simétricas, e satisfazem a desigualdade triangular:

$$
d(u,w) \le d(u,v) + d(v,w)
\quad \text{para quaisquer cidades } u,v,w.
$$

As instâncias euclidianas do projeto obedecem a esse modelo. A garantia não deve ser assumida para matrizes não métricas ou assimétricas.

O algoritmo constrói uma MST com Prim, faz uma busca em profundidade (DFS) a partir da cidade `0` e percorre as cidades pela ordem de primeira visita. Ao pular as revisitas que ocorreriam no passeio da árvore, obtêm-se atalhos diretos; a rota é então fechada na origem. Como a matriz é simétrica, a heurística 2-Opt pode, em seguida, inverter segmentos para reduzir ainda mais o custo.

### Demonstração da razão de aproximação $\alpha \le 2$

O argumento clássico de MST seguido de atalhos métricos é apresentado por Cormen et al. [1, cap. 35]. Seja $C^*$ o custo de um ciclo hamiltoniano ótimo e seja $T$ uma árvore geradora mínima do grafo.

1. Removendo uma aresta do ciclo ótimo, obtém-se um caminho que ainda conecta todas as cidades. Esse caminho é uma árvore geradora, logo a MST não pode custar mais:

   $$
   w(T) \le C^*.
   $$

   Se todas as arestas do ciclo têm peso estritamente positivo, a remoção reduz estritamente o custo e vale $w(T) < C^*$.

2. Uma DFS percorre cada aresta da árvore uma vez para avançar e uma vez para retornar. O passeio fechado resultante tem custo:

   $$
   C_{\text{passeio}} = 2w(T).
   $$

3. Na conversão do passeio em ciclo hamiltoniano, as cidades já visitadas são puladas. Cada atalho substitui um caminho por uma aresta direta; pela desigualdade triangular, essa substituição não aumenta o custo. Assim:

   $$
   C_{\text{preordem}} \le 2w(T) \le 2C^*.
   $$

4. O 2-Opt da implementação só aceita uma troca quando ela reduz estritamente o custo. Portanto, seu resultado não é mais caro que o ciclo de pré-ordem:

   $$
   C_{\text{MST+2-Opt}} \le C_{\text{preordem}} \le 2C^*.
   $$

Logo, para o TSP métrico, a rota produzida tem razão de aproximação no máximo $2$. O 2-Opt pode melhorar a solução encontrada, mas não altera nem fortalece essa garantia teórica.

### Refinamento local 2-Opt

O 2-Opt considera pares de arestas não adjacentes $(a,b)$ e $(c,d)$. Ele testa substituí-las por $(a,c)$ e $(b,d)$ e inverte o segmento intermediário da rota. Como as distâncias são simétricas, as arestas internas ao segmento invertido mantêm o mesmo custo. A troca é aceita quando:

$$
d(a,c) + d(b,d) < d(a,b) + d(c,d).
$$

A implementação utiliza primeira melhoria: ao encontrar uma troca que reduz o custo, aplica-a e reinicia a busca. O processo termina quando uma varredura completa não encontra troca melhorante, atingindo um ótimo local em relação a movimentos 2-Opt. Cada varredura testa $O(n^2)$ pares; como podem ocorrer várias trocas, o tempo total depende da quantidade de melhorias aceitas e não é descrito apenas por $O(n^2)$.

Prim usa $O(n^2)$ de tempo e $O(n)$ de espaço neste grafo completo representado por matriz. A DFS percorre a árvore em $O(n)$. Para os contadores do projeto, `mst_edge_relaxations` registra candidatos examinados no Prim, `two_opt_checks` registra pares testados e `two_opt_swaps` registra as trocas aplicadas. `operations_count` soma os candidatos do Prim e os pares testados pelo 2-Opt.

### Código-fonte do 2-Aproximado e refinamento 2-Opt

```python
"""
Implementação do Algoritmo 2-Aproximado com Árvore Geradora Mínima (MST) e 2-Opt para o TSP.
Responsável: Integrante 4
Complexidade Teórica: Prim O(n^2); garantia de aproximação alpha <= 2 para TSP métrico.
"""

import time
from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost


def _build_mst(distance_matrix: list[list[float]]) -> tuple[list[list[int]], int]:
    """Constrói uma MST com Prim e conta cada aresta candidata examinada."""
    n = len(distance_matrix)
    in_mst = [False] * n
    min_edge = [float("inf")] * n
    parent = [-1] * n
    min_edge[0] = 0.0
    edge_relaxations = 0

    for _ in range(n):
        current = -1
        for city in range(n):
            if not in_mst[city] and (
                current == -1 or min_edge[city] < min_edge[current]
            ):
                current = city

        if current == -1:
            raise ValueError("Não foi possível conectar todas as cidades na MST.")

        in_mst[current] = True
        for neighbor in range(n):
            if in_mst[neighbor]:
                continue

            edge_relaxations += 1
            distance = distance_matrix[current][neighbor]
            if parent[neighbor] == -1 or distance < min_edge[neighbor]:
                min_edge[neighbor] = distance
                parent[neighbor] = current

    tree = [[] for _ in range(n)]
    for city in range(1, n):
        predecessor = parent[city]
        if predecessor == -1:
            raise ValueError(f"A cidade {city} não foi conectada à MST.")
        tree[city].append(predecessor)
        tree[predecessor].append(city)

    for neighbors in tree:
        neighbors.sort()

    return tree, edge_relaxations


def _preorder_tour(tree: list[list[int]]) -> list[int]:
    """Retorna a ordem de descoberta de uma DFS iterativa iniciada na cidade 0."""
    if not tree:
        return []

    preorder = []
    visited = [False] * len(tree)
    stack = [0]

    while stack:
        city = stack.pop()
        if visited[city]:
            continue

        visited[city] = True
        preorder.append(city)
        for neighbor in reversed(tree[city]):
            if not visited[neighbor]:
                stack.append(neighbor)

    return preorder


def _improve_with_two_opt(
    route: list[int],
    distance_matrix: list[list[float]],
) -> tuple[list[int], int, int]:
    """Aplica 2-opt por primeira melhoria em uma rota simétrica."""
    n = len(route) - 1
    pair_checks = 0
    swaps = 0

    while True:
        improved = False
        for first_edge in range(n - 1):
            for second_edge in range(first_edge + 2, n):
                if first_edge == 0 and second_edge == n - 1:
                    continue

                pair_checks += 1
                a = route[first_edge]
                b = route[first_edge + 1]
                c = route[second_edge]
                d = route[second_edge + 1]
                old_edges_cost = distance_matrix[a][b] + distance_matrix[c][d]
                new_edges_cost = distance_matrix[a][c] + distance_matrix[b][d]

                if new_edges_cost < old_edges_cost:
                    route[first_edge + 1 : second_edge + 1] = reversed(
                        route[first_edge + 1 : second_edge + 1]
                    )
                    swaps += 1
                    improved = True
                    break

            if improved:
                break

        if not improved:
            return route, pair_checks, swaps


def solve(instance: TSPInstance) -> TSPResult:
    """
    Resolve o TSP por MST (Prim + DFS), atalhos métricos e refinamento 2-opt.

    Retorna:
        TSPResult: Resultado padronizado. A garantia de fator 2 exige distâncias métricas.
    """
    start_time = time.perf_counter()
    n = instance.dimension
    distance_matrix = instance.distance_matrix

    if n == 0:
        best_route = []
        mst_edge_relaxations = 0
        two_opt_checks = 0
        two_opt_swaps = 0
    else:
        mst, mst_edge_relaxations = _build_mst(distance_matrix)
        best_route = _preorder_tour(mst) + [0]
        best_route, two_opt_checks, two_opt_swaps = _improve_with_two_opt(
            best_route,
            distance_matrix,
        )

    best_cost = compute_tour_cost(best_route, distance_matrix)
    operations_count = mst_edge_relaxations + two_opt_checks

    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="2_Aproximado_MST",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=best_cost,
        execution_time_seconds=elapsed_time,
        operations_count=operations_count,
        extra_metrics={
            "mst_edge_relaxations": mst_edge_relaxations,
            "two_opt_checks": two_opt_checks,
            "two_opt_swaps": two_opt_swaps,
        }
    )
```

## 6.3. Resultados Experimentais: Tempo e Qualidade da Solução

Os testes locais executaram `python -m src.aproximados.test_aproximados`, comparando Vizinho Mais Próximo e MST + 2-Opt nas instâncias pequenas, médias e grandes. Para $n \le 16$, o custo ótimo foi obtido pelo algoritmo exato de Held-Karp já implementado no projeto. Para $n=50$ e $n=100$, o ótimo não foi calculado; portanto, não se atribui desvio empírico nessas linhas.

As medições abaixo são de uma execução em Windows 11 com Python 3.15.2. Os tempos variam conforme o equipamento, a carga do sistema e a execução. O desvio relativo foi calculado por $(C_{\text{heurística}} - C^*)/C^* \times 100$.

| Instância | $n$ | Vizinho Mais Próximo (custo / tempo) | Desvio NN | MST + 2-Opt (custo / tempo) | Ótimo Held-Karp (custo / tempo) | Desvio MST |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `small_8` | 8 | 277.32 / 0.000017 s | 0.00% | 277.32 / 0.000026 s | 277.32 / 0.000141 s | 0.00% |
| `medium_10` | 10 | 343.95 / 0.000016 s | 10.20% | 312.11 / 0.000029 s | 312.11 / 0.000853 s | 0.00% |
| `medium_16` | 16 | 417.49 / 0.000013 s | 13.36% | 376.60 / 0.000044 s | 368.30 / 0.147528 s | 2.25% |
| `large_50` | 50 | 701.24 / 0.000059 s | n/d | 647.77 / 0.001002 s | n/d | n/d |
| `large_100` | 100 | 966.34 / 0.000209 s | n/d | 877.98 / 0.009722 s | n/d | n/d |

Nas instâncias pequenas, o Held-Karp permite verificar que a rota MST + 2-Opt respeitou o limite teórico de fator 2: o desvio observado foi de $0\%$ em `small_8` e `medium_10`, e de aproximadamente $2{,}25\%$ em `medium_16`. O Vizinho Mais Próximo encontrou o ótimo em `small_8`, mas ficou $10{,}20\%$ acima em `medium_10` e $13{,}36\%$ acima em `medium_16`, ilustrando que sua escolha local não garante otimalidade.

Nas instâncias maiores, ambas as heurísticas produziram rotas válidas rapidamente. Nesta execução, o MST + 2-Opt levou cerca de 1 ms em `large_50` e 9,7 ms em `large_100`; o Vizinho Mais Próximo levou menos de 0,3 ms em ambas. Como o ótimo não foi calculado para esses tamanhos, esses resultados demonstram custo e tempo observados, mas não constituem uma medição do desvio em relação ao ótimo.

## Referências

- **[1]** CORMEN, Thomas H.; LEISERSON, Charles E.; RIVEST, Ronald L.; STEIN, Clifford. *Introduction to Algorithms*. 3. ed. Cambridge: The MIT Press / McGraw-Hill, 2009. Cap. 35: *The Traveling-Salesperson Problem*.
