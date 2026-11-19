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

