"""
Script de teste unitário local para os algoritmos Gulosos e Aproximados.
Responsável: Integrante 4
"""

import itertools
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.instance_loader import load_instance_from_json
from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost, validate_tour
from src.aproximados.nearest_neighbor_tsp import solve as solve_nn
from src.aproximados.mst_approximation_tsp import solve as solve_mst
from src.dinamica.held_karp_tsp import solve as solve_exact

BENCHMARK_INSTANCES = (
    "small_8.json",
    "medium_10.json",
    "medium_16.json",
    "large_50.json",
    "large_100.json",
)


def _brute_force_cost(instance: TSPInstance) -> float:
    """Calcula o ótimo exato para as pequenas instâncias usadas nos testes."""
    n = instance.dimension
    if n <= 1:
        return 0.0

    return min(
        compute_tour_cost([0, *permutation, 0], instance.distance_matrix)
        for permutation in itertools.permutations(range(1, n))
    )


def test_nearest_neighbor_edge_cases():
    empty_instance = TSPInstance(name="empty", dimension=0, distance_matrix=[])
    empty_result = solve_nn(empty_instance)
    assert empty_result.best_route == []
    assert empty_result.best_cost == 0.0
    assert empty_result.operations_count == 0

    single_city = TSPInstance(name="single", dimension=1, distance_matrix=[[0.0]])
    single_result = solve_nn(single_city)
    assert single_result.best_route == [0, 0]
    assert single_result.best_cost == 0.0
    assert single_result.operations_count == 0
    assert validate_tour(single_result.best_route, 1)[0]


def test_nearest_neighbor_tie_break_and_metrics():
    instance = TSPInstance(
        name="tie_break",
        dimension=3,
        distance_matrix=[
            [0.0, 1.0, 1.0],
            [1.0, 0.0, 2.0],
            [1.0, 2.0, 0.0],
        ],
    )
    result = solve_nn(instance)

    assert result.best_route == [0, 1, 2, 0]
    assert result.best_cost == 4.0
    assert validate_tour(result.best_route, instance.dimension)[0]
    assert result.operations_count == 3
    assert result.extra_metrics["distance_comparisons"] == 3


def test_mst_approximation_edge_cases():
    empty_instance = TSPInstance(name="empty", dimension=0, distance_matrix=[])
    empty_result = solve_mst(empty_instance)
    assert empty_result.best_route == []
    assert empty_result.best_cost == 0.0
    assert empty_result.operations_count == 0

    single_city = TSPInstance(name="single", dimension=1, distance_matrix=[[0.0]])
    single_result = solve_mst(single_city)
    assert single_result.best_route == [0, 0]
    assert single_result.best_cost == 0.0
    assert single_result.operations_count == 0
    assert validate_tour(single_result.best_route, 1)[0]


def test_mst_approximation_quality_and_two_opt():
    instance = TSPInstance(
        name="metric_two_opt",
        dimension=5,
        distance_matrix=[
            [0.0, 11.12, 13.31, 8.99, 6.19],
            [11.12, 0.0, 13.93, 5.77, 6.22],
            [13.31, 13.93, 0.0, 17.30, 15.18],
            [8.99, 5.77, 17.30, 0.0, 2.87],
            [6.19, 6.22, 15.18, 2.87, 0.0],
        ],
    )
    result = solve_mst(instance)

    is_valid, message = validate_tour(result.best_route, instance.dimension)
    assert is_valid, message
    assert math.isclose(
        result.best_cost,
        compute_tour_cost(result.best_route, instance.distance_matrix),
        abs_tol=1e-6,
    )
    assert result.best_cost <= 2 * _brute_force_cost(instance)
    assert result.extra_metrics["mst_edge_relaxations"] == 10
    assert result.extra_metrics["two_opt_swaps"] > 0
    assert result.operations_count == (
        result.extra_metrics["mst_edge_relaxations"]
        + result.extra_metrics["two_opt_checks"]
    )


def _assert_valid_result(result: TSPResult, instance: TSPInstance) -> None:
    is_valid, message = validate_tour(result.best_route, instance.dimension)
    assert is_valid, f"Rota inválida em {instance.name}: {message}"
    assert result.dimension == instance.dimension
    expected_cost = compute_tour_cost(result.best_route, instance.distance_matrix)
    assert math.isclose(result.best_cost, expected_cost, rel_tol=1e-9, abs_tol=1e-6), (
        f"Custo divergente em {instance.name}: {result.best_cost} != {expected_cost}"
    )


def run_benchmark_suite() -> None:
    instances_dir = REPO_ROOT / "data" / "instances"
    print("\nBenchmark local — Vizinho Mais Próximo e MST + 2-Opt")
    print(
        "| Instância | n | NN custo / tempo | MST+2-Opt custo / tempo | "
        "Ótimo | Razão MST/ótimo |"
    )
    print("| :--- | ---: | ---: | ---: | ---: | ---: |")

    for filename in BENCHMARK_INSTANCES:
        instance_path = instances_dir / filename
        if not instance_path.exists():
            raise FileNotFoundError(f"Instância não encontrada: {instance_path}")

        instance = load_instance_from_json(instance_path)
        nn_result = solve_nn(instance)
        mst_result = solve_mst(instance)
        _assert_valid_result(nn_result, instance)
        _assert_valid_result(mst_result, instance)

        n = instance.dimension
        expected_edge_checks = n * (n - 1) // 2
        assert nn_result.operations_count == expected_edge_checks

        mst_relaxations = mst_result.extra_metrics["mst_edge_relaxations"]
        two_opt_checks = mst_result.extra_metrics["two_opt_checks"]
        assert mst_relaxations == expected_edge_checks
        assert mst_result.operations_count == mst_relaxations + two_opt_checks

        optimal_cost = None
        approximation_ratio = None
        if n <= 16:
            exact_result = solve_exact(instance)
            _assert_valid_result(exact_result, instance)
            optimal_cost = exact_result.best_cost
            assert mst_result.best_cost <= 2 * optimal_cost + 1e-4, (
                f"Violação do fator 2 em {instance.name}: "
                f"MST={mst_result.best_cost}, ótimo={optimal_cost}"
            )
            approximation_ratio = mst_result.best_cost / optimal_cost

        optimal_text = f"{optimal_cost:.2f}" if optimal_cost is not None else "n/d"
        ratio_text = f"{approximation_ratio:.3f}" if approximation_ratio is not None else "n/d"
        print(
            f"| {instance.name} | {n} | "
            f"{nn_result.best_cost:.2f} / {nn_result.execution_time_seconds:.6f}s | "
            f"{mst_result.best_cost:.2f} / {mst_result.execution_time_seconds:.6f}s | "
            f"{optimal_text} | {ratio_text} |"
        )


def main() -> None:
    test_nearest_neighbor_edge_cases()
    test_nearest_neighbor_tie_break_and_metrics()
    test_mst_approximation_edge_cases()
    test_mst_approximation_quality_and_two_opt()
    run_benchmark_suite()


if __name__ == "__main__":
    main()

