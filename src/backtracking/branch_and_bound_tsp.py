"""
Backtracking com Branch & Bound (Ramificação e Poda) para o TSP.
Responsável: Integrante 2 — Pedro Lucas Barbosa Guedes (Matrícula: 202305533)
Complexidade Teórica: O((n-1)!) nós no pior caso, ou seja, tempo O(n!) com a
cota simples e O(n^2 * n!) com a refinada; espaço O(n) de pilha de recursão.
"""

import time
from typing import Literal

from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost

INF = float("inf")
BoundKind = Literal["simples", "refinada"]


class _BranchAndBoundSearch:
    """Busca em profundidade com poda por cota inferior, origem na cidade 0.

    Cada nó da árvore é um caminho parcial que começa em 0. Um filho acrescenta
    uma cidade ainda não visitada ao fim do caminho. Antes de descer para um
    filho, a busca calcula uma cota inferior do custo de qualquer ciclo que
    complete aquele caminho; se a cota não for menor que o melhor ciclo já
    encontrado, a subárvore inteira é descartada (poda).

    Attributes:
        nodes_expanded: Nós em que a recursão entrou (raiz, internos e folhas).
        nodes_pruned: Filhos descartados pela cota antes de serem expandidos.
        solution_updates: Vezes em que um ciclo completo melhorou o melhor
            custo. Como a cota do último nível é exata, toda folha alcançada
            é uma melhora.
    """

    def __init__(self, instance: TSPInstance, bound: BoundKind) -> None:
        """Pré-calcula as estruturas usadas pela cota e pela ordem dos filhos.

        Args:
            instance: Instância com n >= 3 cidades.
            bound: "refinada" (padrão do solve) ou "simples" (a do guia).

        Complexity:
            Tempo O(n^2 log n) para ordenar os vizinhos de cada cidade.
        """
        self.dist = instance.distance_matrix
        self.n = instance.dimension
        self.bound = bound
        self.full_mask = (1 << self.n) - 1

        # Vizinhos de cada cidade em ordem crescente de distância. Visitar
        # primeiro o vizinho mais próximo encontra ciclos baratos cedo, o que
        # torna as podas seguintes mais agressivas.
        self.neighbors_by_distance: list[list[int]] = [
            sorted(
                (v for v in range(self.n) if v != u),
                key=lambda v, u=u: self.dist[u][v],
            )
            for u in range(self.n)
        ]
        # Menor aresta que sai de cada cidade, para qualquer destino.
        self.min_out_edge: list[float] = [
            self.dist[u][self.neighbors_by_distance[u][0]]
            for u in range(self.n)
        ]

        self.best_cost = INF
        self.best_route: list[int] = []
        self.route: list[int] = [0]
        self.nodes_expanded = 0
        self.nodes_pruned = 0
        self.solution_updates = 0

    def _cheapest_edge(self, u: int, allowed_mask: int) -> float:
        """Menor aresta que sai de u para alguma cidade em allowed_mask.

        Args:
            u: Cidade de origem da aresta.
            allowed_mask: Máscara de bits dos destinos permitidos.

        Returns:
            O custo da aresta mais barata, ou INF se não houver destino.

        Complexity:
            O(n) no pior caso; costuma parar nos primeiros vizinhos da lista.
        """
        row = self.dist[u]
        for w in self.neighbors_by_distance[u]:
            if allowed_mask >> w & 1:
                return row[w]
        return INF

    def _lower_bound(
        self,
        city: int,
        visited_mask: int,
        path_cost: float,
        unvisited_min_sum: float,
    ) -> float:
        """Cota inferior do custo de qualquer ciclo que estenda o caminho.

        O caminho vai de 0 até `city` e custa `path_cost`. Falta sair de
        `city`, passar por todas as cidades não visitadas R e voltar a 0.

        Cota simples (do guia):
            path_cost + soma, para u em R, da menor aresta que sai de u.
        Cota refinada:
            path_cost + menor aresta de `city` para R
                      + soma, para u em R, da menor aresta de u
                        para R - {u} ou para a origem 0.

        Ambas valem porque o restante do ciclo usa exatamente uma aresta
        saindo de `city` e de cada cidade de R, e cada aresta custa ao menos a
        mínima permitida para a sua origem.

        Args:
            city: Última cidade do caminho parcial.
            visited_mask: Máscara de bits das cidades já no caminho
                (inclui 0 e city).
            path_cost: Soma das arestas do caminho parcial.
            unvisited_min_sum: Soma de min_out_edge sobre R (usada só na
                cota simples).

        Returns:
            Valor que nunca excede o custo de um ciclo que complete o caminho.

        Complexity:
            Simples O(1); refinada O(|R| * n) no pior caso.
        """
        unvisited = self.full_mask ^ visited_mask
        if unvisited == 0:
            return path_cost + self.dist[city][0]
        if self.bound == "simples":
            return path_cost + unvisited_min_sum

        estimate = path_cost + self._cheapest_edge(city, unvisited)
        targets = unvisited | 1  # cidades em R e a origem 0
        remaining = unvisited
        while remaining and estimate < self.best_cost:
            low_bit = remaining & -remaining
            u = low_bit.bit_length() - 1
            remaining ^= low_bit
            estimate += self._cheapest_edge(u, targets ^ low_bit)
        # Se a soma parcial já alcançou o melhor custo, a poda é a mesma:
        # as parcelas que faltam são não negativas.
        return estimate

    def search(
        self,
        city: int,
        visited_mask: int,
        path_cost: float,
        unvisited_min_sum: float,
    ) -> None:
        """Expande o nó (city, visited_mask) e desce para os filhos viáveis.

        Args:
            city: Última cidade do caminho parcial.
            visited_mask: Máscara de bits das cidades já no caminho.
            path_cost: Soma das arestas do caminho parcial.
            unvisited_min_sum: Soma de min_out_edge das cidades fora do
                caminho.

        Complexity:
            O((n-1)!) nós no pior caso; profundidade da recursão n.
        """
        self.nodes_expanded += 1

        if visited_mask == self.full_mask:
            self.solution_updates += 1
            total = path_cost + self.dist[city][0]
            if total < self.best_cost:
                self.best_cost = total
                self.best_route = self.route + [0]
            return

        for nxt in self.neighbors_by_distance[city]:
            if visited_mask >> nxt & 1:
                continue
            child_mask = visited_mask | (1 << nxt)
            child_cost = path_cost + self.dist[city][nxt]
            child_min_sum = unvisited_min_sum - self.min_out_edge[nxt]

            if (
                self._lower_bound(nxt, child_mask, child_cost, child_min_sum)
                >= self.best_cost
            ):
                self.nodes_pruned += 1
                continue

            self.route.append(nxt)
            self.search(nxt, child_mask, child_cost, child_min_sum)
            self.route.pop()


def solve_with_bound(
    instance: TSPInstance, bound: BoundKind = "refinada"
) -> TSPResult:
    """Resolve o TSP por Branch & Bound usando a cota inferior escolhida.

    Existe para comparar a eficácia das duas cotas no Capítulo 3. O benchmark
    do grupo usa `solve`, que chama esta função com a cota refinada.

    Args:
        instance: Instância do TSP (matriz de custos não negativos).
        bound: "refinada" ou "simples".

    Returns:
        TSPResult com operations_count = nós expandidos e as podas em
        extra_metrics["nodes_pruned"].

    Complexity:
        O((n-1)!) nós no pior caso; espaço O(n) de pilha, mais O(n^2) das
        listas de vizinhos ordenadas (o mesmo tamanho da matriz de entrada).
    """
    start_time = time.perf_counter()
    n = instance.dimension
    dist = instance.distance_matrix

    if n <= 2:
        # Só existe um ciclo possível: [], [0, 0] ou [0, 1, 0].
        best_route = list(range(n)) + [0] if n else []
        best_cost = compute_tour_cost(best_route, dist) if n else 0.0
        expanded = n
        pruned = 0
        updates = 1 if n else 0
    else:
        searcher = _BranchAndBoundSearch(instance, bound)
        searcher.search(0, 1, 0.0, sum(searcher.min_out_edge[1:]))
        best_route = searcher.best_route
        best_cost = compute_tour_cost(best_route, dist)
        expanded = searcher.nodes_expanded
        pruned = searcher.nodes_pruned
        updates = searcher.solution_updates

    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="Branch_and_Bound",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=best_cost,
        execution_time_seconds=elapsed_time,
        operations_count=expanded,
        extra_metrics={
            "nodes_expanded": expanded,
            "nodes_pruned": pruned,
            "best_solution_updates": updates,
            "lower_bound": bound,
        },
    )


def solve(instance: TSPInstance) -> TSPResult:
    """Resolve o TSP por Backtracking com podas por cota inferior (B&B).

    Args:
        instance: Instância do TSP (matriz de custos não negativos).

    Returns:
        TSPResult: Rota ótima com retorno à cidade 0, custo, tempo, nós
        expandidos (operations_count) e nós podados
        (extra_metrics["nodes_pruned"]).

    Complexity:
        Tempo O(n^2 * n!) no pior caso; espaço O(n) de pilha.
    """
    return solve_with_bound(instance, "refinada")
