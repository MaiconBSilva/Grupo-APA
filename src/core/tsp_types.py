"""
Definições dos tipos de dados padrão e funções de validação para o TSP.
Todos os algoritmos desenvolvidos pelos 4 integrantes devem obrigatoriamente
respeitar as assinaturas e classes deste módulo.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TSPInstance:
    """
    Representa uma instância do Problema do Caixeiro Viajante.

    Atributos:
        name: Identificador único da instância (ex.: 'tiny_4', 'berlin52').
        dimension: Quantidade total de cidades / vértices (n).
        distance_matrix: Matriz quadrada de adjacência (n x n) com pesos não negativos.
        coordinates: Lista opcional de coordenadas euclidianas (x, y) de cada vértice.
    """
    name: str
    dimension: int
    distance_matrix: list[list[float]]
    coordinates: list[tuple[float, float]] | None = None

    def get_distance(self, u: int, v: int) -> float:
        """Retorna a distância/peso da aresta entre o vértice u e v."""
        return self.distance_matrix[u][v]


@dataclass
class TSPResult:
    """
    Representa o resultado consolidado da execução de qualquer algoritmo do TSP.

    Atributos:
        algorithm_name: Nome do algoritmo (ex: 'Forca_Bruta', 'Held_Karp', 'Vizinho_Mais_Proximo').
        instance_name: Nome da instância resolvida.
        dimension: Número de cidades (n).
        best_route: Lista de inteiros contendo o ciclo hamiltoniano com retorno (tamanho n + 1).
                    Exemplo para n=4: [0, 2, 3, 1, 0].
        best_cost: Custo total acumulado da rota.
        execution_time_seconds: Tempo decorrido de execução em segundos (via time.perf_counter).
        operations_count: Contagem determinística de operações fundamentais executadas.
        extra_metrics: Dicionário livre para métricas extras (ex.: nós podados, estados em cache).
    """
    algorithm_name: str
    instance_name: str
    dimension: int
    best_route: list[int]
    best_cost: float
    execution_time_seconds: float
    operations_count: int
    extra_metrics: dict[str, Any] = field(default_factory=dict)


def compute_tour_cost(route: list[int], distance_matrix: list[list[float]]) -> float:
    """
    Calcula a soma das arestas de um ciclo completo.
    Espera uma rota de tamanho n + 1 onde route[0] == route[-1].
    """
    if len(route) < 2:
        return 0.0
    total = 0.0
    for i in range(len(route) - 1):
        u, v = route[i], route[i + 1]
        total += distance_matrix[u][v]
    return round(total, 4)


def validate_tour(route: list[int], dimension: int) -> tuple[bool, str]:
    """
    Valida rigorosamente se uma rota é um ciclo hamiltoniano válido.

    Regras:
    1. A rota deve possuir exatamente dimension + 1 elementos.
    2. A rota deve começar e terminar na mesma cidade (por convenção, cidade 0).
    3. As cidades intermediárias route[0:dimension] devem conter cada vértice de 0 a dimension-1 exatamente uma vez.

    Retorna:
        tuple[bool, str]: (True, 'Rota válida') ou (False, 'Motivo da invalidade').
    """
    if len(route) != dimension + 1:
        return False, f"Tamanho incorreto: esperado {dimension + 1}, recebido {len(route)}."

    if route[0] != route[-1]:
        return False, f"A rota não fecha o ciclo: início={route[0]}, fim={route[-1]}."

    visited_vertices = route[:-1]
    unique_vertices = set(visited_vertices)

    if len(unique_vertices) != dimension:
        return False, f"Vértices repetidos ou faltando: visitados {len(unique_vertices)} de {dimension}."

    expected_set = set(range(dimension))
    if unique_vertices != expected_set:
        diff = expected_set - unique_vertices
        return False, f"Cidades não visitadas: {diff}."

    return True, "Rota válida"

