"""
Suíte de testes unitários e benchmark local para o algoritmo de Held-Karp.
Responsável: Integrante 3 — Maicon Brendo da Silva (Matrícula: 202204199)
"""

import itertools
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.instance_loader import load_instance_from_json
from src.core.tsp_types import TSPInstance, compute_tour_cost, validate_tour
from src.dinamica.held_karp_tsp import solve

BENCHMARK_INSTANCES = [
    "tiny_4.json",
    "small_6.json",
    "small_8.json",
    "medium_10.json",
    "medium_12.json",
    "medium_16.json",
    "medium_20.json",
]


def _brute_force_reference_cost(instance: TSPInstance) -> float:
    """Calcula o custo ótimo exato por enumeração exaustiva para instâncias pequenas (n <= 10)."""
    n = instance.dimension
    if n <= 1:
        return 0.0
    dist = instance.distance_matrix
    best_cost = math.inf
    for perm in itertools.permutations(range(1, n)):
        route = [0, *perm, 0]
        cost = compute_tour_cost(route, dist)
        if cost < best_cost:
            best_cost = cost
    return best_cost


def test_edge_cases() -> None:
    """Valida casos de borda sintéticos em memória (n = 0, 1, 2, 3)."""
    inst_0 = TSPInstance(name="edge_0", dimension=0, distance_matrix=[])
    res_0 = solve(inst_0)
    assert res_0.best_route == []
    assert res_0.best_cost == 0.0
    assert res_0.operations_count == 0
    assert res_0.extra_metrics["transitions_evaluated"] == 0

    inst_1 = TSPInstance(name="edge_1", dimension=1, distance_matrix=[[0.0]])
    res_1 = solve(inst_1)
    assert res_1.best_route == [0, 0]
    assert res_1.best_cost == 0.0
    assert res_1.operations_count == 1
    assert res_1.extra_metrics["transitions_evaluated"] == 0

    inst_2 = TSPInstance(
        name="edge_2",
        dimension=2,
        distance_matrix=[[0.0, 7.5], [7.5, 0.0]],
    )
    res_2 = solve(inst_2)
    is_valid_2, msg_2 = validate_tour(res_2.best_route, 2)
    assert is_valid_2, msg_2
    assert math.isclose(res_2.best_cost, 15.0, abs_tol=1e-6)
    assert res_2.operations_count == 1
    assert res_2.extra_metrics["transitions_evaluated"] == 0

    # Instância assimétrica n=3 para validar direção e otimalidade
    inst_3 = TSPInstance(
        name="edge_3_asym",
        dimension=3,
        distance_matrix=[
            [0.0, 2.0, 9.0],
            [5.0, 0.0, 3.0],
            [1.0, 8.0, 0.0],
        ],
    )
    res_3 = solve(inst_3)
    is_valid_3, msg_3 = validate_tour(res_3.best_route, 3)
    assert is_valid_3, msg_3
    expected_3 = _brute_force_reference_cost(inst_3)
    assert math.isclose(res_3.best_cost, expected_3, abs_tol=1e-6)
    assert res_3.operations_count == (3 - 1) * (1 << (3 - 2))
    assert res_3.extra_metrics["transitions_evaluated"] == (3 - 1) * (3 - 2) * (1 << (3 - 3))
    print("[OK] Casos de borda sintéticos (n=0, 1, 2, 3) validados com sucesso.")


def run_benchmark_suite() -> None:
    """Executa validação de corretude, otimalidade e coleta métricas de n=4 até n=20."""
    instances_dir = REPO_ROOT / "data" / "instances"
    rows: list[tuple[str, int, float, float, int, int]] = []

    print("\nExecutando suíte Held-Karp (n=4 até n=20)...")
    for filename in BENCHMARK_INSTANCES:
        instance_path = instances_dir / filename
        assert instance_path.exists(), f"Instância não encontrada: {instance_path}"

        instance = load_instance_from_json(instance_path)
        n = instance.dimension
        result = solve(instance)

        is_valid, msg = validate_tour(result.best_route, n)
        assert is_valid, f"Rota inválida em {instance.name}: {msg}"

        recomputed_cost = compute_tour_cost(result.best_route, instance.distance_matrix)
        assert math.isclose(result.best_cost, recomputed_cost, rel_tol=1e-9, abs_tol=1e-6), (
            f"Divergência de custo em {instance.name}: {result.best_cost} vs {recomputed_cost}"
        )

        expected_states = (n - 1) * (1 << (n - 2))
        assert result.operations_count == expected_states, (
            f"Estados inesperados em {instance.name}: {result.operations_count} != {expected_states}"
        )
        assert result.extra_metrics["memoized_states"] == expected_states

        expected_transitions = (n - 1) * (n - 2) * (1 << (n - 3))
        transitions = result.extra_metrics["transitions_evaluated"]
        assert transitions == expected_transitions, (
            f"Transições inesperadas em {instance.name}: {transitions} != {expected_transitions}"
        )

        bf_note = ""
        if n <= 10:
            ref_cost = _brute_force_reference_cost(instance)
            assert math.isclose(result.best_cost, ref_cost, rel_tol=1e-9, abs_tol=1e-6), (
                f"Subotimalidade em {instance.name}: Held-Karp={result.best_cost} vs FB={ref_cost}"
            )
            bf_note = " | Ótimo==FB [OK]"

        print(
            f"[OK] {instance.name:10s} (n={n:2d}) | Custo: {result.best_cost:8.2f} | "
            f"Tempo: {result.execution_time_seconds:9.6f}s | "
            f"Estados: {result.operations_count:8d} | Transições: {transitions:9d}{bf_note}"
        )
        rows.append((
            instance.name,
            n,
            result.best_cost,
            result.execution_time_seconds,
            result.operations_count,
            transitions,
        ))

    print("\n### Tabela Markdown (Resultados Experimentais — Held-Karp)\n")
    print("| Instância | $n$ | Custo Ótimo | Tempo (s) | Estados Memoizados | Transições Avaliadas |")
    print("| :--- | :---: | :---: | :---: | :---: | :---: |")
    for name, n, cost, elapsed, states, transitions in rows:
        print(f"| `{name}` | {n} | {cost:.2f} | {elapsed:.6f} | {states:,} | {transitions:,} |".replace(",", "."))


def main() -> None:
    """Ponto de entrada da suíte de testes e benchmark do Held-Karp."""
    test_edge_cases()
    run_benchmark_suite()


if __name__ == "__main__":
    main()
