"""
Implementação do Algoritmo de Força Bruta para o Problema do Caixeiro Viajante (TSP).
Responsável: Integrante 1
Complexidade Teórica: Tempo O(n * n!), Espaço O(n).
"""

import time
from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost


def solve(instance: TSPInstance) -> TSPResult:
    """
    Resolve o TSP utilizando Força Bruta com geração exaustiva de permutações.

    Fixa a cidade 0 como origem/destino para evitar rotações cíclicas redundantes.
    Avalia (n-1)! permutações possíveis e identifica o ciclo de menor custo total.

    Retorna:
        TSPResult: Resultado padronizado contendo melhor rota, custo, tempo e operações.
    """
    start_time = time.perf_counter()
    n = instance.dimension

    # TODO: Integrante 1 implementará a lógica de permutações e contagem aqui
    # Este é um stub inicial que atende ao contrato de dados:
    best_route = list(range(n)) + [0]
    best_cost = compute_tour_cost(best_route, instance.distance_matrix)
    operations_count = 0

    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="Forca_Bruta",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=best_cost,
        execution_time_seconds=elapsed_time,
        operations_count=operations_count,
        extra_metrics={"permutations_evaluated": operations_count}
    )

