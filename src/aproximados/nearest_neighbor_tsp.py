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

