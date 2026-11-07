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

    # TODO: Integrante 4 implementará a escolha gulosa do vizinho mais próximo aqui
    best_route = list(range(n)) + [0]
    best_cost = compute_tour_cost(best_route, instance.distance_matrix)
    comparisons_count = 0

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

