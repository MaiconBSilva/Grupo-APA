"""
Módulo utilitário para carregamento, salvamento e geração de instâncias do TSP.
"""

import json
import math
import os
import random
from pathlib import Path
from src.core.tsp_types import TSPInstance


def calculate_euclidean_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Calcula a distância euclidiana 2D entre dois pontos arredondada para 2 casas."""
    return round(math.hypot(p1[0] - p2[0], p1[1] - p2[1]), 2)


def calculate_euclidean_matrix(coords: list[tuple[float, float]]) -> list[list[float]]:
    """Gera matriz de adjacência simétrica a partir de uma lista de coordenadas 2D."""
    n = len(coords)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dist = calculate_euclidean_distance(coords[i], coords[j])
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix


def generate_random_euclidean_instance(
    name: str,
    n: int,
    seed: int = 42,
    max_coord: float = 100.0
) -> TSPInstance:
    """
    Gera uma instância euclidiana reproduzível com coordenadas pseudoaleatórias.
    Garante a propriedade do TSP Métrico (desigualdade triangular).
    """
    rng = random.Random(seed)
    coordinates = [
        (round(rng.uniform(0.0, max_coord), 2), round(rng.uniform(0.0, max_coord), 2))
        for _ in range(n)
    ]
    matrix = calculate_euclidean_matrix(coordinates)
    return TSPInstance(
        name=name,
        dimension=n,
        distance_matrix=matrix,
        coordinates=coordinates
    )


def save_instance_to_json(instance: TSPInstance, filepath: str | Path) -> None:
    """Salva a instância em um arquivo JSON padronizado."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    payload = {
        "name": instance.name,
        "dimension": instance.dimension,
        "coordinates": instance.coordinates,
        "distance_matrix": instance.distance_matrix
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def load_instance_from_json(filepath: str | Path) -> TSPInstance:
    """Carrega uma instância a partir de um arquivo JSON."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    coords = None
    if data.get("coordinates") is not None:
        coords = [tuple(c) for c in data["coordinates"]]

    return TSPInstance(
        name=data["name"],
        dimension=data["dimension"],
        distance_matrix=data["distance_matrix"],
        coordinates=coords
    )

