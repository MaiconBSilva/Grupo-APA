"""
Implementação do Algoritmo 2-Aproximado com Árvore Geradora Mínima (MST) e 2-Opt para o TSP.
Responsável: Integrante 4
Complexidade Teórica: Tempo O(n^2), Razão de aproximação alpha <= 2 para TSP métrico.
"""

import time
from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost


def solve(instance: TSPInstance) -> TSPResult:
    """
    Resolve o TSP utilizando o Algoritmo 2-Aproximado baseado em MST (Prim + DFS) e refinamento 2-Opt.

    Retorna:
        TSPResult: Resultado padronizado com garantia matemática de custo <= 2 * Ótimo.
    """
    start_time = time.perf_counter()
    n = instance.dimension

    # TODO: Integrante 4 implementará o Prim + percurso em pré-ordem DFS + 2-opt aqui
    best_route = list(range(n)) + [0]
    best_cost = compute_tour_cost(best_route, instance.distance_matrix)
    operations_count = 0

    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="2_Aproximado_MST",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=best_cost,
        execution_time_seconds=elapsed_time,
        operations_count=operations_count,
        extra_metrics={"two_opt_swaps": 0}
    )

