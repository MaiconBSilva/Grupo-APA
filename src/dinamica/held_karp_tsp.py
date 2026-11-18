"""
Implementação do Algoritmo de Bellman-Held-Karp via Programação Dinâmica para o TSP.
Responsável: Integrante 3 — Maicon Brendo da Silva (Matrícula: 202204199)
Complexidade Teórica: Tempo Theta(n^2 * 2^n), Espaço Theta(n * 2^n).
"""

import math
import time
from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost


def _reconstruct_route(
    parent: list[int],
    full_submask: int,
    last_city: int,
    stride: int,
) -> list[int]:
    """
    Reconstrói o ciclo hamiltoniano ótimo a partir da tabela de predecessores.

    Args:
        parent: Tabela linearizada de predecessores indexada por (submask * stride + v_idx).
        full_submask: Máscara completa dos vértices {1, ..., n - 1}.
        last_city: Última cidade visitada antes do retorno à cidade 0.
        stride: Número de cidades excluindo a origem (n - 1).

    Returns:
        Lista de inteiros representando o ciclo completo [0, ..., 0] com n + 1 elementos.
    """
    reversed_route = [0]
    curr_submask = full_submask
    curr_city = last_city

    while curr_city != 0:
        reversed_route.append(curr_city)
        curr_idx = curr_city - 1
        prev_city = parent[curr_submask * stride + curr_idx]
        curr_submask ^= 1 << curr_idx
        curr_city = prev_city

    reversed_route.append(0)
    return reversed_route[::-1]


def solve(instance: TSPInstance) -> TSPResult:
    """
    Resolve o TSP utilizando o algoritmo exato de Bellman-Held-Karp com bitmask.

    A origem é fixada na cidade 0. Cada subconjunto S contendo 0 é representado
    por uma máscara `submask` de (n - 1) bits para os vértices {1, ..., n - 1},
    onde o bit j indica a presença da cidade (j + 1).

    Args:
        instance: Instância do TSP contendo dimensão e matriz de distâncias.

    Returns:
        TSPResult: Resultado padronizado com rota ótima, custo, tempo de execução
        e contagens determinísticas de estados memoizados e transições avaliadas.
    """
    start_time = time.perf_counter()
    n = instance.dimension
    dist = instance.distance_matrix

    if n == 0:
        elapsed_time = time.perf_counter() - start_time
        return TSPResult(
            algorithm_name="Held_Karp_PD",
            instance_name=instance.name,
            dimension=n,
            best_route=[],
            best_cost=0.0,
            execution_time_seconds=elapsed_time,
            operations_count=0,
            extra_metrics={"memoized_states": 0, "transitions_evaluated": 0},
        )

    if n == 1:
        elapsed_time = time.perf_counter() - start_time
        return TSPResult(
            algorithm_name="Held_Karp_PD",
            instance_name=instance.name,
            dimension=n,
            best_route=[0, 0],
            best_cost=0.0,
            execution_time_seconds=elapsed_time,
            operations_count=1,
            extra_metrics={"memoized_states": 1, "transitions_evaluated": 0},
        )

    if n == 2:
        best_route = [0, 1, 0]
        best_cost = compute_tour_cost(best_route, dist)
        elapsed_time = time.perf_counter() - start_time
        return TSPResult(
            algorithm_name="Held_Karp_PD",
            instance_name=instance.name,
            dimension=n,
            best_route=best_route,
            best_cost=best_cost,
            execution_time_seconds=elapsed_time,
            operations_count=1,
            extra_metrics={"memoized_states": 1, "transitions_evaluated": 0},
        )

    stride = n - 1
    num_submasks = 1 << stride
    inf = math.inf

    dp = [inf] * (num_submasks * stride)
    parent = [0] * (num_submasks * stride)

    masks_by_size: list[list[int]] = [[] for _ in range(stride + 1)]
    for submask in range(1, num_submasks):
        masks_by_size[submask.bit_count()].append(submask)

    states_computed = 0
    transitions_evaluated = 0

    # Caso base: |S| = 2 -> subconjuntos {0, v} com submask de tamanho 1
    for v_idx in range(stride):
        submask = 1 << v_idx
        idx = submask * stride + v_idx
        dp[idx] = dist[0][v_idx + 1]
        parent[idx] = 0
        states_computed += 1

    # Recorrência bottom-up por cardinalidade de S \ {0}
    for size in range(2, stride + 1):
        for submask in masks_by_size[size]:
            base_offset = submask * stride
            rem_v = submask
            while rem_v:
                lsb_v = rem_v & -rem_v
                v_idx = lsb_v.bit_length() - 1
                rem_v ^= lsb_v

                prev_submask = submask ^ lsb_v
                prev_offset = prev_submask * stride
                v_city = v_idx + 1

                best_val = inf
                best_u_city = 0

                rem_u = prev_submask
                while rem_u:
                    lsb_u = rem_u & -rem_u
                    u_idx = lsb_u.bit_length() - 1
                    rem_u ^= lsb_u

                    candidate = dp[prev_offset + u_idx] + dist[u_idx + 1][v_city]
                    transitions_evaluated += 1
                    if candidate < best_val:
                        best_val = candidate
                        best_u_city = u_idx + 1

                dp[base_offset + v_idx] = best_val
                parent[base_offset + v_idx] = best_u_city
                states_computed += 1

    # Fechamento do ciclo hamiltoniano retornando à cidade 0
    full_submask = num_submasks - 1
    full_offset = full_submask * stride
    best_tour_val = inf
    best_last_city = 1

    for v_idx in range(stride):
        v_city = v_idx + 1
        candidate = dp[full_offset + v_idx] + dist[v_city][0]
        if candidate < best_tour_val:
            best_tour_val = candidate
            best_last_city = v_city

    best_route = _reconstruct_route(parent, full_submask, best_last_city, stride)
    best_cost = compute_tour_cost(best_route, dist)
    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="Held_Karp_PD",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=best_cost,
        execution_time_seconds=elapsed_time,
        operations_count=states_computed,
        extra_metrics={
            "memoized_states": states_computed,
            "transitions_evaluated": transitions_evaluated,
        },
    )
