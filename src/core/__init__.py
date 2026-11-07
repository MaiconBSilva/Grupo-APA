"""
Módulo Core para o Trabalho Final de APA — TSP.
Contém os tipos de dados e funções contratuais compartilhadas por todos os integrantes.
"""

from src.core.tsp_types import TSPInstance, TSPResult, validate_tour, compute_tour_cost

__all__ = ["TSPInstance", "TSPResult", "validate_tour", "compute_tour_cost"]

