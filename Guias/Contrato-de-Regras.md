# Contrato de Regras e Padrões Técnicos do Repositório

Este documento estabelece as **especificações técnicas, contratos de código, padrões de medição e diretrizes de formatação** que todos os integrantes devem seguir impreterivelmente. O objetivo é assegurar total interoperabilidade entre as implementações e consistência máxima no relatório final.

---

## 1. Padrões de Código (Python 3)

1. **Versão:** Python 3.10 ou superior.
2. **Estilo e Formatação:** Seguir rigorosamente a **PEP 8**:
   * Nomes de funções e variáveis: `snake_case` (ex.: `calculate_cost`, `lower_bound`).
   * Nomes de classes: `PascalCase` (ex.: `TSPInstance`, `TSPResult`).
   * Constantes: `UPPER_SNAKE_CASE` (ex.: `INF = float('inf')`).
3. **Tipagem Estrita (Type Annotations):** Todas as funções e métodos devem utilizar *type hints* para parâmetros e retornos:
   ```python
   def solve_tsp(instance: TSPInstance) -> TSPResult: ...
   ```
4. **Documentação de Código (Docstrings):** Todas as funções devem conter docstrings no formato Google Style ou NumPy explicando parâmetros, retorno e complexidade teórica esperada.
5. **Proibição de Efeitos Colaterais:**
   * Nenhuma função algorítmica deve realizar `print()`, entrada de teclado (`input()`) ou plotagem gráfica interna.
   * O algoritmo deve apenas receber a instância, processar e retornar o objeto `TSPResult`. Toda impressão e visualização ocorre nos scripts de teste ou runners de benchmark.

---

## 2. Contrato de Dados Compartilhado (`src/core/`)

Para garantir que o script de testes e o benchmark unificado consigam executar os algoritmos de todos os 4 integrantes sem nenhuma modificação, todos devem obedecer às seguintes estruturas de dados definidas em `src/core/tsp_types.py`:

### Objeto de Entrada: `TSPInstance`
Representa uma instância do problema:
```python
@dataclass
class TSPInstance:
    name: str                           # Nome da instância (ex: "instancia_8_cidades")
    dimension: int                      # Quantidade de vértices / cidades (n)
    distance_matrix: list[list[float]]  # Matriz de distâncias simétrica (n x n)
    coordinates: list[tuple[float, float]] | None = None  # Coordenadas (x, y) se disponíveis
```

### Objeto de Retorno: `TSPResult`
Representa o resultado gerado por qualquer algoritmo:
```python
@dataclass
class TSPResult:
    algorithm_name: str         # Nome do algoritmo (ex: "Forca_Bruta", "Held_Karp")
    instance_name: str          # Nome da instância avaliada
    dimension: int              # Número de cidades (n)
    best_route: list[int]       # Ciclo completo com retorno (ex: [0, 2, 1, 3, 0])
    best_cost: float            # Custo total do ciclo
    execution_time_seconds: float # Tempo real medido em segundos
    operations_count: int       # Contagem de operações fundamentais determinísticas
    extra_metrics: dict         # Métricas adicionais (nós podados, subproblemas em cache, etc.)
```

### Assinatura Padrão Obrigatória
Cada módulo deve exportar uma função principal com a seguinte assinatura exata:
```python
def solve(instance: TSPInstance) -> TSPResult:
    """
    Resolve o TSP para a instância dada utilizando a estratégia do módulo.
    """
```

---

## 3. Diretrizes para Medição de Tempo e Contagem de Operações

O edital exige duas análises fundamentais:
1. **Análise de Desempenho (Tempo de Execução):** Medição do tempo de CPU / relógio.
2. **Análise de Complexidade Computacional (Contagem de Instruções):** Contagem de operações fundamentais determinísticas.

### 3.1. Medição de Tempo de Execução
* Utilizar estritamente `time.perf_counter()` para obter precisão de nanossegundos.
* Medir exclusivamente o tempo do algoritmo, excluindo carga de arquivos do disco ou formatação de strings:
```python
import time

start_time = time.perf_counter()
# ... execução do algoritmo ...
elapsed_time = time.perf_counter() - start_time
```

### 3.2. Contagem de Operações Fundamentais por Paradigma
A contagem de operações deve ser determinística (o mesmo número em qualquer computador):

| Paradigma / Algoritmo | Operação Fundamental a ser Contabilizada |
| :--- | :--- |
| **Força Bruta** | Número de permutações / rotas completas geradas e avaliadas. |
| **Backtracking (Branch & Bound)** | Número de nós expandidos na árvore de busca recursiva e número de podas realizadas. |
| **Programação Dinâmica (Held-Karp)** | Número de estados únicos $(S, v)$ calculados / inseridos na tabela de memoização. |
| **Guloso (Nearest Neighbor)** | Número de arestas ou distâncias comparadas para eleger o próximo vértice. |
| **2-Aproximado (MST) & 2-Opt** | Número de arestas relaxadas no Prim/Kruskal + número de trocas de arestas (*edge swaps*) testadas no 2-opt. |

---

## 4. Regras de Validação da Solução (Ciclo Válido)

Para que a rota retornada por qualquer algoritmo seja considerada válida, ela deve cumprir rigorosamente as seguintes propriedades:
1. **Tamanho:** Conter exatamente $n + 1$ elementos (para $n$ cidades).
2. **Origem e Destino:** O primeiro e o último elemento devem ser idênticos (cidade de partida, por convenção a cidade `0`).
3. **Visita Única:** O conjunto das cidades intermediárias `route[0:n]` deve ser exatamente uma permutação de `{0, 1, ..., n - 1}` (sem cidades repetidas ou faltantes).
4. **Custo:** O custo calculado deve coincidir com a soma exata das arestas correspondentes:
   $$\text{cost} = \sum_{i=0}^{n-1} \text{matrix}[\text{route}[i]][\text{route}[i+1]]$$

---

## 5. Padrão dos Documentos em Markdown (`docs/*.md`)

Cada capítulo do trabalho escrito deve ser mantido em formato Markdown com alta qualidade tipográfica, seguindo o padrão que facilitará a conversão para PDF:

1. **Equações Matemáticas:** Utilizar sintaxe LaTeX:
   * Inline: `$O(n^2 2^n)$` ou `$\sum_{i=1}^n c_i$`.
   * Bloco:
     $$c(\pi) = d(\pi(n), \pi(1)) + \sum_{i=1}^{n-1} d(\pi(i), \pi(i+1))$$
2. **Códigos-Fonte Inseridos:** O edital exige (item 49) que os códigos utilizados nas implementações sejam inseridos na documentação. Eles devem estar em blocos com identificador de linguagem:
   ````markdown
   ```python
   def branch_and_bound_tsp(instance: TSPInstance) -> TSPResult:
       # Código limpo, comentado e bem formatado
   ```
   ````
3. **Tabelas de Resultados:** Utilizar tabelas em Markdown no seguinte padrão:
   ```markdown
   | Instância | Vértices ($n$) | Custo Obtido | Tempo (s) | Operações Contadas |
   | :--- | :--- | :--- | :--- | :--- |
   | tiny_4 | 4 | 35.00 | 0.000045 | 6 |
   ```
4. **Citações Bibliográficas:** Utilizar os identificadores conforme o edital:
   * `[1]` Cormen et al. (*Introduction to Algorithms*).
   * `[2]` Ziviani (*Projeto de Algoritmos com implementações em Java e C++*).

---

## 6. Template de Pull Request (PR)

Ao abrir um PR no GitHub para a `main`, utilize o seguinte modelo:

```markdown
### Descrição do PR
Implementação do algoritmo [Nome do Algoritmo] e capítulo correspondente em docs/.

### Mudanças Realizadas
- [x] Implementado algoritmo em `src/<pasta>/...py`
- [x] Testes unitários com instâncias em `src/<pasta>/test_...py`
- [x] Capítulo redigido em `docs/<capitulo>.md` com código embutido
- [x] Contagem de operações fundamentais validada

### Resultados dos Testes Locais
- Instâncias testadas: [ex: tiny_4, small_8, medium_12]
- Solução ótima encontrada conferida com baseline: [Sim/Não]
- Tempo médio de execução: [ex: 0.12s para n=10]

### Revisor Solicitado
@[Nome_Colega] - Favor validar conformidade com o Contrato de Regras.
```

