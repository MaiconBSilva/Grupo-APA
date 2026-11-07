"""
Módulo do Integrante 4: Algoritmos Gulosos e Aproximados para o TSP.
"""

from src.aproximados.nearest_neighbor_tsp import solve as solve_nearest_neighbor
from src.aproximados.mst_approximation_tsp import solve as solve_mst_approximation

__all__ = ["solve_nearest_neighbor", "solve_mst_approximation"]

