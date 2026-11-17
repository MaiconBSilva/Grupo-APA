"""Solução exata do TSP por enumeração de permutações."""

import time
from itertools import permutations

from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost


def solve(instance: TSPInstance) -> TSPResult:
    """Encontra um ciclo de custo mínimo com origem na cidade 0.

    Args:
        instance: Instância com pelo menos uma cidade e matriz de custos finitos.

    Returns:
        Rota ótima, custo no padrão do repositório, tempo e número de rotas.

    Raises:
        ValueError: Se a instância não tiver cidades.

    Complexity:
        Tempo Θ(n!) e espaço auxiliar Θ(n).
    """
    start_time = time.perf_counter()
    n = instance.dimension
    if n < 1:
        raise ValueError("A instância deve ter pelo menos uma cidade.")

    matrix = instance.distance_matrix
    best_route: list[int] = []
    best_cost = float("inf")
    operations_count = 0

    for order in permutations(range(1, n)):
        route = [0, *order, 0]
        cost = 0.0
        for index in range(n):
            cost += matrix[route[index]][route[index + 1]]
        operations_count += 1

        if cost < best_cost:
            best_cost = cost
            best_route = route

    reported_cost = compute_tour_cost(best_route, matrix)
    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="Forca_Bruta",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=reported_cost,
        execution_time_seconds=elapsed_time,
        operations_count=operations_count,
        extra_metrics={"permutations_evaluated": operations_count},
    )