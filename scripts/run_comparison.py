"""
Runner unificado de benchmark para o Trabalho Final de APA — TSP.
Executa todos os algoritmos disponíveis contra as instâncias padrão em data/instances/
e gera uma tabela comparativa com tempos, custos e contagem de operações.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.instance_loader import load_instance_from_json
from src.core.tsp_types import TSPResult, validate_tour


def get_available_solvers():
    """Importa dinamicamente os algoritmos conforme forem sendo mergeados na main."""
    solvers = {}

    try:
        from src.forca_bruta.brute_force_tsp import solve as solve_fb
        solvers["Força Bruta"] = (solve_fb, 10)  # Limite máximo de n recomendado
    except ImportError:
        pass

    try:
        from src.backtracking.branch_and_bound_tsp import solve as solve_bb
        solvers["Branch & Bound"] = (solve_bb, 16)
    except ImportError:
        pass

    try:
        from src.dinamica.held_karp_tsp import solve as solve_hk
        solvers["Held-Karp (PD)"] = (solve_hk, 20)
    except ImportError:
        pass

    try:
        from src.aproximados.nearest_neighbor_tsp import solve as solve_nn
        solvers["Vizinho Próximo (Guloso)"] = (solve_nn, 1000)
    except ImportError:
        pass

    try:
        from src.aproximados.mst_approximation_tsp import solve as solve_mst
        solvers["2-Aproximado (MST)"] = (solve_mst, 1000)
    except ImportError:
        pass

    return solvers


def main():
    instances_dir = REPO_ROOT / "data" / "instances"
    instances_files = sorted(instances_dir.glob("*.json"), key=lambda p: int(p.stem.split("_")[1]) if "_" in p.stem else 0)

    solvers = get_available_solvers()
    print("=" * 80)
    print("BENCHMARK COMPARATIVO UNIFICADO — PROBLEMA DO CAIXEIRO VIAJANTE")
    print(f"Solvers ativos identificados: {list(solvers.keys()) or 'Nenhum solver implementado ainda'}")
    print("=" * 80)

    if not solvers:
        print("\nNenhum algoritmo encontrado ainda nas pastas src/.")
        print("Assim que cada integrante mergear sua branch com a implementação, este script executará os benchmarks automaticamente.")
        return

    for inst_path in instances_files:
        instance = load_instance_from_json(inst_path)
        print(f"\n--> Instância: {instance.name} (n = {instance.dimension})")

        for solver_name, (solve_fn, max_n) in solvers.items():
            if instance.dimension > max_n:
                print(f"  [{solver_name}] Pulado (n={instance.dimension} > limite prático {max_n})")
                continue

            try:
                res: TSPResult = solve_fn(instance)
                is_valid, msg = validate_tour(res.best_route, res.dimension)
                status = "OK" if is_valid else f"ERRO ({msg})"

                print(
                    f"  [{solver_name:25s}] Custo: {res.best_cost:8.2f} | "
                    f"Tempo: {res.execution_time_seconds:10.6f}s | "
                    f"Operações: {res.operations_count:10d} | "
                    f"Status: {status}"
                )
            except Exception as e:
                print(f"  [{solver_name}] Falha na execução: {e}")


if __name__ == "__main__":
    main()

