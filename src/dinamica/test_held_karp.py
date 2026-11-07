"""
Script de teste unitário local para o algoritmo de Held-Karp.
Responsável: Integrante 3
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.instance_loader import load_instance_from_json
from src.core.tsp_types import validate_tour
from src.dinamica.held_karp_tsp import solve


def main():
    instance_path = REPO_ROOT / "data" / "instances" / "medium_12.json"
    if not instance_path.exists():
        print(f"Erro: Instância não encontrada em {instance_path}")
        return

    instance = load_instance_from_json(instance_path)
    print(f"Executando teste local de Held-Karp na instância {instance.name} (n={instance.dimension})...")

    result = solve(instance)
    is_valid, msg = validate_tour(result.best_route, result.dimension)

    print(f" -> Rota retornada: {result.best_route}")
    print(f" -> Custo total: {result.best_cost}")
    print(f" -> Tempo: {result.execution_time_seconds:.6f}s")
    print(f" -> Estados calculados: {result.operations_count}")
    print(f" -> Validação da rota: {'[OK]' if is_valid else f'[FALHA: {msg}]'}")


if __name__ == "__main__":
    main()

