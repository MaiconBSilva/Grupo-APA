# 2. Estratégia exata de força bruta

A força bruta resolve o Problema do Caixeiro Viajante (TSP) avaliando todas as ordens de visita possíveis e escolhendo a rota de menor custo. Por encontrar o ótimo para as instâncias em que a enumeração é viável, essa estratégia serve de referência para avaliar a qualidade das soluções aproximadas.

## 2.1. Enumeração das rotas

A implementação fixa a cidade `0` como origem e destino. Essa escolha elimina as rotações de uma mesma sequência. Por exemplo, `0 → 1 → 2 → 3 → 0` e `2 → 3 → 0 → 1 → 2` descrevem o mesmo percurso, com pontos de partida diferentes.

Para cada permutação das cidades restantes, o algoritmo:

1. Acrescenta a cidade `0` no início e no fim da sequência.
2. Soma os custos das arestas consecutivas, incluindo a volta à origem.
3. Incrementa o contador de rotas avaliadas.
4. Atualiza a melhor rota quando encontra um custo estritamente menor.

Em caso de empate, mantém a primeira rota encontrada. Em instâncias simétricas, o algoritmo ainda avalia os dois sentidos de cada ciclo. Assim, a contagem de operações segue o padrão do grupo de uma avaliação para cada uma das $(n-1)!$ permutações.

## 2.2. Correção do algoritmo

Todo ciclo que visita as $n$ cidades pode ser representado a partir da cidade `0`. Ao fixar esse ponto de partida, a ordem das outras $n-1$ cidades corresponde a uma das permutações geradas. Portanto, a enumeração inclui uma representação de todo ciclo admissível.

Após avaliar a primeira rota, ela é a melhor entre as rotas examinadas. A cada avaliação seguinte, o algoritmo mantém a melhor rota anterior ou a substitui por uma de custo menor. Desse modo, após examinar todas as permutações, a rota armazenada tem custo mínimo entre todos os ciclos admissíveis.

## 2.3. Código-fonte

A função `solve` recebe uma `TSPInstance` e devolve um `TSPResult`, conforme o contrato compartilhado do projeto. Os custos são comparados durante a busca antes do arredondamento padrão aplicado ao valor retornado.

```python
"""Solução exata do TSP por enumeração de permutações."""

import time
from itertools import permutations

from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost


def solve(instance: TSPInstance) -> TSPResult:
    """Encontra um ciclo de custo mínimo com origem na cidade 0.

    Args:
        instance: Instância com pelo menos uma cidade e matriz de custos finitos.

    Returns:
        Rota ótima, custo no padrão do repositório, tempo e número de rotas.

    Raises:
        ValueError: Se a instância não tiver cidades.

    Complexity:
        Tempo Θ(n!) e espaço auxiliar Θ(n).
    """
    start_time = time.perf_counter()
    n = instance.dimension
    if n < 1:
        raise ValueError("A instância deve ter pelo menos uma cidade.")

    matrix = instance.distance_matrix
    best_route: list[int] = []
    best_cost = float("inf")
    operations_count = 0

    for order in permutations(range(1, n)):
        route = [0, *order, 0]
        cost = 0.0
        for index in range(n):
            cost += matrix[route[index]][route[index + 1]]
        operations_count += 1

        if cost < best_cost:
            best_cost = cost
            best_route = route

    reported_cost = compute_tour_cost(best_route, matrix)
    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="Forca_Bruta",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=reported_cost,
        execution_time_seconds=elapsed_time,
        operations_count=operations_count,
        extra_metrics={"permutations_evaluated": operations_count},
    )
```

## 2.4. Análise de complexidade

| Medida | Complexidade | Justificativa |
| :--- | :--- | :--- |
| Rotas avaliadas | $(n-1)!$ | Cada permutação das cidades restantes gera uma rota completa. |
| Acessos à matriz na enumeração | $n\cdot(n-1)!=n!$ | O cálculo do custo examina as $n$ arestas de cada rota. |
| Tempo de execução | $\Theta(n!)$ | Montar e avaliar uma candidata custa $\Theta(n)$, repetido para cada permutação. |
| Espaço auxiliar | $\Theta(n)$ | O gerador produz uma permutação por vez. A permutação atual, a rota candidata e a melhor rota têm tamanho linear. |
| Espaço da entrada | $\Theta(n^2)$ | A matriz armazena os custos entre todos os pares de cidades. |

A operação fundamental registrada em `operations_count` é **uma avaliação de rota completa**. Ao final da busca, o utilitário compartilhado recalcula o custo da rota escolhida em $\Theta(n)$ para reportá-lo no formato do projeto. Essa etapa preserva a complexidade total de $\Theta(n!)$.

## 2.5. Validação e resultados experimentais

O teste verifica se a rota começa e termina na cidade `0`, se contém todas as cidades exatamente uma vez antes do retorno, se seu custo coincide com o ótimo de referência e se o número de rotas avaliadas é igual a $(n-1)!$.

Para cada instância, o teste executa o algoritmo cinco vezes e registra a mediana dos tempos obtidos com `time.perf_counter()`. O carregamento dos arquivos JSON ocorre antes da medição.

| Instância | Cidades ($n$) | Custo ótimo de referência | Tempo mediano (s) | Rotas avaliadas |
| :--- | ---: | ---: | ---: | ---: |
| `tiny_4` | 4 | 226,30 | A medir | 6 |
| `small_6` | 6 | 147,14 | A medir | 120 |
| `small_8` | 8 | 277,32 | A medir | 5.040 |
| `medium_10` | 10 | 312,11 | A medir | 362.880 |

### Crescimento do espaço de busca

De 8 para 10 cidades, o número de rotas passa de 5.040 para 362.880, um aumento de **72 vezes**. Para 12 cidades, a enumeração exigiria $11! = 39.916.800$ rotas, **110 vezes** a contagem para 10 cidades. Além do aumento na quantidade de rotas, cada rota com 12 cidades exige somar mais arestas.

O benchmark comparativo do grupo limita a execução da força bruta a instâncias com até 10 cidades. Nesse intervalo, o custo ótimo calculado permite medir quanto as soluções aproximadas se afastam do ótimo na mesma instância.