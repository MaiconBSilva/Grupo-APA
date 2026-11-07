"""
Script para geração automática das instâncias de teste padronizadas do TSP.
Gera arquivos em formato JSON no diretório data/instances/.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz do repositório ao sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.instance_loader import generate_random_euclidean_instance, save_instance_to_json


def main():
    base_dir = Path(__file__).resolve().parent.parent / "data" / "instances"
    base_dir.mkdir(parents=True, exist_ok=True)

    instances_to_generate = [
        ("tiny_4", 4, 101),
        ("small_6", 6, 102),
        ("small_8", 8, 103),
        ("medium_10", 10, 104),
        ("medium_12", 12, 105),
        ("medium_16", 16, 106),
        ("medium_20", 20, 107),
        ("large_50", 50, 108),
        ("large_100", 100, 109),
    ]

    print("Gerando instâncias padrão de teste do TSP...")
    for name, n, seed in instances_to_generate:
        inst = generate_random_euclidean_instance(name=name, n=n, seed=seed)
        filepath = base_dir / f"{name}.json"
        save_instance_to_json(inst, filepath)
        print(f" -> Criada instância {name} (n={n}) em {filepath.name}")

    print("Todas as instâncias foram geradas com sucesso!")


if __name__ == "__main__":
    main()
