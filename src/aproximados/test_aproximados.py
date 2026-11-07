"""
Script de teste unitário local para os algoritmos Gulosos e Aproximados.
Responsável: Integrante 4
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.instance_loader import load_instance_from_json
from src.core.tsp_types import validate_tour
from src.aproximados.nearest_neighbor_tsp import solve as solve_nn
from src.aproximados.mst_approximation_tsp import solve as solve_mst


def main():
    instance_path = REPO_ROOT / "data" / "instances" / "large_50.json"
    if not instance_path.exists():
        print(f"Erro: Instância não encontrada em {instance_path}")
        return

    instance = load_instance_from_json(instance_path)
    print(f"Executando testes locais em instância de grande porte: {instance.name} (n={instance.dimension})...")

    # Teste 1: Vizinho Mais Próximo
    res_nn = solve_nn(instance)
    valid_nn, msg_nn = validate_tour(res_nn.best_route, res_nn.dimension)
    print(f" -> [Vizinho Mais Próximo] Custo: {res_nn.best_cost} | Tempo: {res_nn.execution_time_seconds:.6f}s | Status: {'[OK]' if valid_nn else f'[FALHA: {msg_nn}]'}")

    # Teste 2: 2-Aproximado MST
    res_mst = solve_mst(instance)
    valid_mst, msg_mst = validate_tour(res_mst.best_route, res_mst.dimension)
    print(f" -> [2-Aproximado MST]   Custo: {res_mst.best_cost} | Tempo: {res_mst.execution_time_seconds:.6f}s | Status: {'[OK]' if valid_mst else f'[FALHA: {msg_mst}]'}")


if __name__ == "__main__":
    main()

