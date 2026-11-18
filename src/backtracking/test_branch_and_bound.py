"""
Testes e experimento local do Backtracking com Branch & Bound.
Responsável: Integrante 2 — Pedro Lucas Barbosa Guedes (Matrícula: 202305533)

Executar a partir da raiz do repositório:
    python -m src.backtracking.test_branch_and_bound
"""

import itertools
import math
import random
import sys
from pathlib import Path
from statistics import median

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Os imports abaixo dependem do sys.path ajustado acima.
from src.backtracking.branch_and_bound_tsp import (  # noqa: E402
    solve,
    solve_with_bound,
)
from src.core.instance_loader import load_instance_from_json  # noqa: E402
from src.core.tsp_types import (  # noqa: E402
    TSPInstance,
    TSPResult,
    compute_tour_cost,
    validate_tour,
)

INSTANCES_DIR = REPO_ROOT / "data" / "instances"

# Custos ótimos conferidos com a Força Bruta (n <= 10) e com o Held-Karp
# (n = 12 e 16).
CASES = (
    ("tiny_4", 4, 226.30),
    ("small_6", 6, 147.14),
    ("small_8", 8, 277.32),
    ("medium_10", 10, 312.11),
    ("medium_12", 12, 280.79),
    ("medium_16", 16, 368.30),
)
REPETITIONS = 3


def _brute_force_cost(instance: TSPInstance) -> float:
    """Custo ótimo enumerando as (n-1)! rotas (referência para n <= 9)."""
    n = instance.dimension
    best = math.inf
    for order in itertools.permutations(range(1, n)):
        best = min(
            best, compute_tour_cost([0, *order, 0], instance.distance_matrix)
        )
    return best


def _full_tree_nodes(n: int) -> int:
    """Nós da árvore sem poda: soma de (n-1)!/(n-1-k)!, k = 0..n-1."""
    return sum(math.perm(n - 1, k) for k in range(n))


def _check_result(
    result: TSPResult, instance: TSPInstance, expected_cost: float
) -> None:
    """Confere rota, custo e métricas contra o contrato do grupo."""
    name = instance.name
    valid, message = validate_tour(result.best_route, instance.dimension)
    assert valid, f"{name}: {message}"
    assert result.best_route[0] == result.best_route[-1] == 0, name
    assert result.dimension == instance.dimension, name
    assert result.instance_name == name, name
    assert math.isclose(
        result.best_cost, expected_cost, abs_tol=1e-6
    ), f"{name}: custo {result.best_cost} != {expected_cost}"
    assert math.isclose(
        result.best_cost,
        compute_tour_cost(result.best_route, instance.distance_matrix),
        abs_tol=1e-6,
    ), name
    assert (
        result.operations_count == result.extra_metrics["nodes_expanded"]
    ), name
    assert result.operations_count <= _full_tree_nodes(
        instance.dimension
    ), name


def test_edge_cases() -> None:
    """Instâncias com 0 a 3 cidades, incluindo uma assimétrica."""
    res_0 = solve(TSPInstance("edge_0", 0, []))
    assert res_0.best_route == [] and res_0.best_cost == 0.0

    res_1 = solve(TSPInstance("edge_1", 1, [[0.0]]))
    assert res_1.best_route == [0, 0] and res_1.best_cost == 0.0

    res_2 = solve(TSPInstance("edge_2", 2, [[0.0, 7.5], [7.5, 0.0]]))
    assert res_2.best_route == [0, 1, 0] and math.isclose(
        res_2.best_cost, 15.0
    )

    # Assimétrica: 0->1->2->0 custa 2+3+1 = 6; 0->2->1->0 custa 9+8+5 = 22.
    asym = TSPInstance(
        "edge_3_asym", 3, [[0.0, 2.0, 9.0], [5.0, 0.0, 3.0], [1.0, 8.0, 0.0]]
    )
    res_3 = solve(asym)
    assert res_3.best_route == [0, 1, 2, 0] and math.isclose(
        res_3.best_cost, 6.0
    )
    print("[OK] Casos de borda (n = 0, 1, 2, 3 assimétrica)")


def test_random_against_brute_force(seeds: int = 30) -> None:
    """Compara com a enumeração completa em matrizes aleatórias de n = 4 a 9.

    Usa matrizes simétricas e assimétricas, com custos inteiros pequenos para
    provocar empates, o caso em que uma poda mal feita perderia o ótimo.
    """
    for seed in range(seeds):
        rng = random.Random(seed)
        n = rng.randint(4, 9)
        symmetric = seed % 2 == 0
        matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j or (symmetric and j < i):
                    continue
                matrix[i][j] = float(rng.randint(1, 20))
                if symmetric:
                    matrix[j][i] = matrix[i][j]
        instance = TSPInstance(f"random_{seed}", n, matrix)
        expected = _brute_force_cost(instance)
        for bound in ("refinada", "simples"):
            _check_result(
                solve_with_bound(instance, bound), instance, expected
            )
    print(
        f"[OK] {seeds} matrizes aleatórias (simétricas e assimétricas) "
        "iguais à força bruta"
    )


def run_experiment() -> None:
    """Executa as instâncias do grupo e imprime a tabela do Capítulo 3."""
    print()
    print(
        "| Instância | n | Custo ótimo | Nós expandidos | Podas | (n-1)! | "
        "Nós da árvore sem poda | Expandidos / árvore | Tempo mediano (s) |"
    )
    print("| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")

    for name, dimension, expected_cost in CASES:
        instance = load_instance_from_json(INSTANCES_DIR / f"{name}.json")
        assert instance.dimension == dimension, name
        times: list[float] = []
        for _ in range(REPETITIONS):
            result = solve(instance)
            _check_result(result, instance, expected_cost)
            times.append(result.execution_time_seconds)

        expanded = result.operations_count
        tree = _full_tree_nodes(dimension)
        if dimension >= 8:
            # A poda precisa cortar a árvore de forma expressiva.
            assert expanded < math.factorial(dimension - 1) / 10, name
        pruned = result.extra_metrics["nodes_pruned"]
        permutations = math.factorial(dimension - 1)
        print(
            f"| {name} | {dimension} | {result.best_cost:.2f} | "
            f"{expanded:,} | {pruned:,} | {permutations:,} | {tree:,} | "
            f"{100 * expanded / tree:.2g}% | {median(times):.6f} |"
        )


def run_bound_comparison() -> None:
    """Compara a cota simples do guia com a refinada (eficácia das podas)."""
    print()
    print("| Instância | n | Cota | Nós expandidos | Podas | Tempo (s) |")
    print("| :--- | ---: | :--- | ---: | ---: | ---: |")
    for name, dimension, expected_cost in CASES:
        if dimension < 8:
            continue
        instance = load_instance_from_json(INSTANCES_DIR / f"{name}.json")
        for bound in ("simples", "refinada"):
            result = solve_with_bound(instance, bound)
            _check_result(result, instance, expected_cost)
            print(
                f"| {name} | {dimension} | {bound} | "
                f"{result.operations_count:,} | "
                f"{result.extra_metrics['nodes_pruned']:,} | "
                f"{result.execution_time_seconds:.6f} |"
            )


def main() -> None:
    """Roda os testes de correção e, em seguida, os experimentos."""
    test_edge_cases()
    test_random_against_brute_force()
    run_experiment()
    run_bound_comparison()


if __name__ == "__main__":
    main()
