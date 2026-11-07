"""
Implementação de Backtracking com Branch & Bound (Ramificação e Poda) para o TSP.
Responsável: Integrante 2
Complexidade Teórica: Pior caso O(n!), Espaço O(n).
"""

import time
from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost


def solve(instance: TSPInstance) -> TSPResult:
    """
    Resolve o TSP utilizando Backtracking com podas por Cota Inferior (Branch & Bound).

    Retorna:
        TSPResult: Resultado padronizado com nós expandidos e nós podados.
    """
    start_time = time.perf_counter()
    n = instance.dimension

    # TODO: Integrante 2 implementará a busca em profundidade com poda aqui
    best_route = list(range(n)) + [0]
    best_cost = compute_tour_cost(best_route, instance.distance_matrix)
    expanded_nodes = 0
    pruned_nodes = 0

    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="Branch_and_Bound",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=best_cost,
        execution_time_seconds=elapsed_time,
        operations_count=expanded_nodes,
        extra_metrics={
            "nodes_expanded": expanded_nodes,
            "nodes_pruned": pruned_nodes
        }
    )

