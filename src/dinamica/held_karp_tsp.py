"""
Implementação do Algoritmo de Bellman-Held-Karp via Programação Dinâmica para o TSP.
Responsável: Integrante 3
Complexidade Teórica: Tempo O(n^2 * 2^n), Espaço O(n * 2^n).
"""

import time
from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost


def solve(instance: TSPInstance) -> TSPResult:
    """
    Resolve o TSP utilizando o Algoritmo exato de Bellman-Held-Karp com bitmask e memoização.

    Retorna:
        TSPResult: Resultado padronizado com contagem de subproblemas em cache.
    """
    start_time = time.perf_counter()
    n = instance.dimension

    # TODO: Integrante 3 implementará a recorrência de Bellman-Held-Karp com bitmask aqui
    best_route = list(range(n)) + [0]
    best_cost = compute_tour_cost(best_route, instance.distance_matrix)
    states_computed = 0

    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="Held_Karp_PD",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=best_cost,
        execution_time_seconds=elapsed_time,
        operations_count=states_computed,
        extra_metrics={"memoized_states": states_computed}
    )

