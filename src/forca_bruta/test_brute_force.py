"""Valida a força bruta e imprime seus resultados experimentais."""

import os
import platform
import sys
from math import factorial, isclose
from pathlib import Path
from statistics import median

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.instance_loader import load_instance_from_json
from src.core.tsp_types import compute_tour_cost, validate_tour
from src.forca_bruta.brute_force_tsp import solve

INSTANCES_DIR = REPO_ROOT / "data" / "instances"
CASES = (
    ("tiny_4", 4, 226.30),
    ("small_6", 6, 147.14),
    ("small_8", 8, 277.32),
    ("medium_10", 10, 312.11),
)
REPETITIONS = 5


def main() -> None:
    """Verifica as quatro instâncias e imprime a mediana dos tempos."""
    print(f"Sistema operacional: {platform.platform()}")
    print(f"Python: {platform.python_version()} ({platform.python_implementation()})")
    processor = platform.processor() or os.environ.get(
        "PROCESSOR_IDENTIFIER", "Não identificado"
    )
    print(f"Processador: {processor}")
    print()
    print("| Instância | n | Custo ótimo | Tempo mediano (s) | Rotas |")
    print("|---|---:|---:|---:|---:|")

    for name, dimension, expected_cost in CASES:
        instance = load_instance_from_json(INSTANCES_DIR / f"{name}.json")
        assert instance.dimension == dimension, name
        expected_count = factorial(dimension - 1)
        times: list[float] = []

        for _ in range(REPETITIONS):
            result = solve(instance)
            route = result.best_route
            valid, message = validate_tour(route, dimension)
            assert valid, f"{name}: {message}"
            assert route[0] == route[-1] == 0, name
            assert result.dimension == dimension, name
            assert result.instance_name == instance.name, name
            assert result.operations_count == expected_count, name
            assert result.extra_metrics["permutations_evaluated"] == (
                expected_count
            ), name
            assert isclose(result.best_cost, expected_cost, abs_tol=1e-9), name
            assert isclose(
                result.best_cost,
                compute_tour_cost(route, instance.distance_matrix),
                abs_tol=1e-9,
            ), name
            times.append(result.execution_time_seconds)

        print(
            f"| {name} | {dimension} | {expected_cost:.2f} | "
            f"{median(times):.6f} | {expected_count} |"
        )


if __name__ == "__main__":
    main()