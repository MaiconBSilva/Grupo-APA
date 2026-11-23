# 3. Estratégia 2: Backtracking com Branch & Bound

**Responsável:** Integrante 2 — Pedro Lucas Barbosa Guedes (Matrícula: `202305533`)  
**Status:** Concluído

---

O Backtracking com Branch & Bound encontra a rota ótima do Problema do Caixeiro Viajante (TSP) sem examinar todas as rotas. Ele constrói a rota cidade a cidade e descarta um caminho parcial assim que uma cota inferior mostra que nenhuma rota que o complete pode superar a melhor já encontrada. Na instância `medium_16`, o algoritmo expande 166.139 nós de uma árvore com cerca de $3{,}55 \times 10^{12}$ nós e termina em menos de 2 s. Pela estimativa da Seção 3.5, a Força Bruta levaria cerca de 12 dias na mesma máquina.

---

## 3.1. Descrição do Paradigma e Espaço de Estados

O **backtracking** é uma busca em profundidade que constrói uma solução por etapas. A cada etapa, escolhe uma opção, avança e, ao esgotar as possibilidades daquele ramo, desfaz a escolha e tenta a próxima [2]. As escolhas possíveis formam uma **árvore de estados**:

- A **raiz** é o caminho que contém só a cidade `0`, a origem fixa (a mesma convenção da Força Bruta).
- Um **nó de profundidade $k$** é um caminho $0 \to c_1 \to \dots \to c_k$ com $k$ cidades distintas além da origem.
- Os **filhos** de um nó acrescentam ao fim do caminho uma cidade ainda não visitada.
- As **folhas**, na profundidade $n-1$, são as $(n-1)!$ rotas completas. O custo de cada uma inclui a volta à cidade `0`.

Sem poda, o backtracking percorre a árvore inteira e examina as mesmas $(n-1)!$ rotas da Força Bruta. O **Branch & Bound** (ramificação e poda) acrescenta dois elementos à busca [7, 8]:

1. **Incumbente:** o custo $U$ da melhor rota completa encontrada até o momento. No início, $U = +\infty$.
2. **Cota inferior** $LB(P)$: um valor que nunca excede o custo de qualquer rota que complete o caminho parcial $P$.

Antes de descer para um filho $P$, o algoritmo calcula $LB(P)$. Se $LB(P) \ge U$, nenhuma rota daquela subárvore pode ser melhor que a incumbente, e a subárvore inteira é descartada sem ser visitada. Essa é a **poda**.

A ordem dos filhos também importa. A implementação visita primeiro a cidade mais próxima da cidade atual. Assim, a primeira descida até uma folha equivale à heurística do vizinho mais próximo e produz cedo uma incumbente de custo baixo. Quanto menor $U$, mais filhos satisfazem $LB(P) \ge U$, e mais cedo as podas começam.

---

## 3.2. Formulação da Cota Inferior e Regras de Poda

### Notação

Seja $P = (0, c_1, \dots, c_k)$ um caminho parcial que termina na cidade $c = c_k$, com custo $g(P) = \sum_{i=0}^{k-1} d(c_i, c_{i+1})$, em que $c_0 = 0$. Seja $R$ o conjunto das cidades ainda não visitadas. Os custos $d(u, v)$ são não negativos, e a matriz pode ser assimétrica.

Qualquer rota que complete $P$ sai de $c$, passa por todas as cidades de $R$ em alguma ordem e volta a `0`. Esse trecho final usa exatamente $|R| + 1$ arestas, **uma saindo de cada cidade** de $\{c\} \cup R$:

- a aresta que sai de $c$ chega a alguma cidade de $R$;
- a aresta que sai de cada $u \in R$ chega a outra cidade de $R$ ou à origem `0`.

### Cota simples (a do guia da equipe)

Para cada cidade não visitada, soma-se a menor aresta que sai dela, para qualquer destino:

$$LB_s(P) = g(P) + \sum_{u \in R} \min_{v \ne u} d(u, v)$$

### Cota refinada (usada na função `solve`)

A cota refinada aproveita as duas observações acima. Conta também a aresta que sai de $c$ e restringe os destinos de cada aresta aos que ainda são possíveis:

$$LB_r(P) = g(P) + \min_{v \in R} d(c, v) + \sum_{u \in R} \; \min_{v \in (R \setminus \{u\}) \cup \{0\}} d(u, v)$$

Quando $R = \varnothing$, as duas cotas valem $g(P) + d(c, 0)$, que é o custo exato da rota completa.

### Por que nenhuma solução ótima é descartada

**Lema (admissibilidade).** Para toda rota $T$ que completa $P$, vale $LB_s(P) \le LB_r(P) \le c(T)$.

*Demonstração.* Seja $s(x)$ a cidade que vem logo depois de $x$ em $T$. Então

$$c(T) = g(P) + d(c, s(c)) + \sum_{u \in R} d(u, s(u)).$$

Como $s(c) \in R$, a parcela $d(c, s(c))$ é pelo menos $\min_{v \in R} d(c, v)$. Como $s(u) \in (R \setminus \{u\}) \cup \{0\}$, cada $d(u, s(u))$ é pelo menos o mínimo sobre esse conjunto. Somando termo a termo, $LB_r(P) \le c(T)$. Além disso, o mínimo sobre um conjunto maior nunca é maior, e $\min_{v \in R} d(c, v) \ge 0$; logo $LB_s(P) \le LB_r(P)$. $\square$

**Regra de poda.** Um filho $P$ é descartado quando $LB(P) \ge U$.

**Teorema (correção).** Ao final da busca, $U$ é o custo ótimo $OPT$, e a rota guardada tem esse custo.

*Demonstração.* $U$ só diminui, e cada valor que assume é o custo de uma rota completa; portanto $U \ge OPT$ sempre. Seja $T^*$ uma rota ótima. Se nenhum prefixo de $T^*$ for podado, a busca chega à folha $T^*$ e faz $U \le OPT$. Se algum prefixo $P$ de $T^*$ for podado, no momento da poda valia $U \le LB(P) \le c(T^*) = OPT$, pelo lema. Nos dois casos, $U \le OPT$ em algum momento e, como $U$ não aumenta, termina igual a $OPT$. $\square$

A poda com $\ge$ (e não $>$) descarta também os ramos que só empatariam com a incumbente. Isso não perde o ótimo, porque uma rota com aquele custo já foi guardada. Uma consequência é que a busca só entra em uma folha quando ela melhora $U$ estritamente, pois no último nível a cota é exata. A métrica `best_solution_updates` conta essas melhoras.

### Detalhes da implementação da cota

- As cidades visitadas ficam em uma **máscara de bits**, como no Held-Karp do Capítulo 5. Testar se uma cidade foi visitada custa $O(1)$.
- Cada cidade guarda a lista dos seus vizinhos em ordem crescente de distância. Para achar a menor aresta de $u$ para um conjunto permitido, basta percorrer essa lista até o primeiro vizinho permitido, o que costuma terminar nos primeiros elementos.
- A soma da cota refinada é interrompida assim que a soma parcial alcança $U$. As parcelas restantes são não negativas, então a decisão de podar é a mesma e o cálculo fica mais curto.
- Os mínimos usam as arestas que **saem** de cada cidade. Por isso, a cota também vale para matrizes assimétricas, o que os testes conferem.

---

## 3.3. Implementação do Código-Fonte

O módulo segue o contrato do grupo. A função `solve` recebe uma `TSPInstance`, devolve um `TSPResult` e não imprime nada. O campo `operations_count` traz os nós expandidos, e `extra_metrics` traz as podas. A função `solve_with_bound` existe só para comparar as duas cotas na Seção 3.5.

Duas contagens definem as operações fundamentais:

- **Nó expandido:** um nó em que a recursão entra (a raiz, os nós internos e as folhas).
- **Poda:** um filho descartado pela cota antes de ser expandido.

```python
"""
Backtracking com Branch & Bound (Ramificação e Poda) para o TSP.
Responsável: Integrante 2 — Pedro Lucas Barbosa Guedes (Matrícula: 202305533)
Complexidade Teórica: O((n-1)!) nós no pior caso, ou seja, tempo O(n!) com a
cota simples e O(n^2 * n!) com a refinada; espaço O(n) de pilha de recursão.
"""

import time
from typing import Literal

from src.core.tsp_types import TSPInstance, TSPResult, compute_tour_cost

INF = float("inf")
BoundKind = Literal["simples", "refinada"]


class _BranchAndBoundSearch:
    """Busca em profundidade com poda por cota inferior, origem na cidade 0.

    Cada nó da árvore é um caminho parcial que começa em 0. Um filho acrescenta
    uma cidade ainda não visitada ao fim do caminho. Antes de descer para um
    filho, a busca calcula uma cota inferior do custo de qualquer ciclo que
    complete aquele caminho; se a cota não for menor que o melhor ciclo já
    encontrado, a subárvore inteira é descartada (poda).

    Attributes:
        nodes_expanded: Nós em que a recursão entrou (raiz, internos e folhas).
        nodes_pruned: Filhos descartados pela cota antes de serem expandidos.
        solution_updates: Vezes em que um ciclo completo melhorou o melhor
            custo. Como a cota do último nível é exata, toda folha alcançada
            é uma melhora.
    """

    def __init__(self, instance: TSPInstance, bound: BoundKind) -> None:
        """Pré-calcula as estruturas usadas pela cota e pela ordem dos filhos.

        Args:
            instance: Instância com n >= 3 cidades.
            bound: "refinada" (padrão do solve) ou "simples" (a do guia).

        Complexity:
            Tempo O(n^2 log n) para ordenar os vizinhos de cada cidade.
        """
        self.dist = instance.distance_matrix
        self.n = instance.dimension
        self.bound = bound
        self.full_mask = (1 << self.n) - 1

        # Vizinhos de cada cidade em ordem crescente de distância. Visitar
        # primeiro o vizinho mais próximo encontra ciclos baratos cedo, o que
        # torna as podas seguintes mais agressivas.
        self.neighbors_by_distance: list[list[int]] = [
            sorted(
                (v for v in range(self.n) if v != u),
                key=lambda v, u=u: self.dist[u][v],
            )
            for u in range(self.n)
        ]
        # Menor aresta que sai de cada cidade, para qualquer destino.
        self.min_out_edge: list[float] = [
            self.dist[u][self.neighbors_by_distance[u][0]]
            for u in range(self.n)
        ]

        self.best_cost = INF
        self.best_route: list[int] = []
        self.route: list[int] = [0]
        self.nodes_expanded = 0
        self.nodes_pruned = 0
        self.solution_updates = 0

    def _cheapest_edge(self, u: int, allowed_mask: int) -> float:
        """Menor aresta que sai de u para alguma cidade em allowed_mask.

        Args:
            u: Cidade de origem da aresta.
            allowed_mask: Máscara de bits dos destinos permitidos.

        Returns:
            O custo da aresta mais barata, ou INF se não houver destino.

        Complexity:
            O(n) no pior caso; costuma parar nos primeiros vizinhos da lista.
        """
        row = self.dist[u]
        for w in self.neighbors_by_distance[u]:
            if allowed_mask >> w & 1:
                return row[w]
        return INF

    def _lower_bound(
        self,
        city: int,
        visited_mask: int,
        path_cost: float,
        unvisited_min_sum: float,
    ) -> float:
        """Cota inferior do custo de qualquer ciclo que estenda o caminho.

        O caminho vai de 0 até `city` e custa `path_cost`. Falta sair de
        `city`, passar por todas as cidades não visitadas R e voltar a 0.

        Cota simples (do guia):
            path_cost + soma, para u em R, da menor aresta que sai de u.
        Cota refinada:
            path_cost + menor aresta de `city` para R
                      + soma, para u em R, da menor aresta de u
                        para R - {u} ou para a origem 0.

        Ambas valem porque o restante do ciclo usa exatamente uma aresta
        saindo de `city` e de cada cidade de R, e cada aresta custa ao menos a
        mínima permitida para a sua origem.

        Args:
            city: Última cidade do caminho parcial.
            visited_mask: Máscara de bits das cidades já no caminho
                (inclui 0 e city).
            path_cost: Soma das arestas do caminho parcial.
            unvisited_min_sum: Soma de min_out_edge sobre R (usada só na
                cota simples).

        Returns:
            Valor que nunca excede o custo de um ciclo que complete o caminho.

        Complexity:
            Simples O(1); refinada O(|R| * n) no pior caso.
        """
        unvisited = self.full_mask ^ visited_mask
        if unvisited == 0:
            return path_cost + self.dist[city][0]
        if self.bound == "simples":
            return path_cost + unvisited_min_sum

        estimate = path_cost + self._cheapest_edge(city, unvisited)
        targets = unvisited | 1  # cidades em R e a origem 0
        remaining = unvisited
        while remaining and estimate < self.best_cost:
            low_bit = remaining & -remaining
            u = low_bit.bit_length() - 1
            remaining ^= low_bit
            estimate += self._cheapest_edge(u, targets ^ low_bit)
        # Se a soma parcial já alcançou o melhor custo, a poda é a mesma:
        # as parcelas que faltam são não negativas.
        return estimate

    def search(
        self,
        city: int,
        visited_mask: int,
        path_cost: float,
        unvisited_min_sum: float,
    ) -> None:
        """Expande o nó (city, visited_mask) e desce para os filhos viáveis.

        Args:
            city: Última cidade do caminho parcial.
            visited_mask: Máscara de bits das cidades já no caminho.
            path_cost: Soma das arestas do caminho parcial.
            unvisited_min_sum: Soma de min_out_edge das cidades fora do
                caminho.

        Complexity:
            O((n-1)!) nós no pior caso; profundidade da recursão n.
        """
        self.nodes_expanded += 1

        if visited_mask == self.full_mask:
            self.solution_updates += 1
            total = path_cost + self.dist[city][0]
            if total < self.best_cost:
                self.best_cost = total
                self.best_route = self.route + [0]
            return

        for nxt in self.neighbors_by_distance[city]:
            if visited_mask >> nxt & 1:
                continue
            child_mask = visited_mask | (1 << nxt)
            child_cost = path_cost + self.dist[city][nxt]
            child_min_sum = unvisited_min_sum - self.min_out_edge[nxt]

            if (
                self._lower_bound(nxt, child_mask, child_cost, child_min_sum)
                >= self.best_cost
            ):
                self.nodes_pruned += 1
                continue

            self.route.append(nxt)
            self.search(nxt, child_mask, child_cost, child_min_sum)
            self.route.pop()


def solve_with_bound(
    instance: TSPInstance, bound: BoundKind = "refinada"
) -> TSPResult:
    """Resolve o TSP por Branch & Bound usando a cota inferior escolhida.

    Existe para comparar a eficácia das duas cotas no Capítulo 3. O benchmark
    do grupo usa `solve`, que chama esta função com a cota refinada.

    Args:
        instance: Instância do TSP (matriz de custos não negativos).
        bound: "refinada" ou "simples".

    Returns:
        TSPResult com operations_count = nós expandidos e as podas em
        extra_metrics["nodes_pruned"].

    Complexity:
        O((n-1)!) nós no pior caso; espaço O(n) de pilha, mais O(n^2) das
        listas de vizinhos ordenadas (o mesmo tamanho da matriz de entrada).
    """
    start_time = time.perf_counter()
    n = instance.dimension
    dist = instance.distance_matrix

    if n <= 2:
        # Só existe um ciclo possível: [], [0, 0] ou [0, 1, 0].
        best_route = list(range(n)) + [0] if n else []
        best_cost = compute_tour_cost(best_route, dist) if n else 0.0
        expanded = n
        pruned = 0
        updates = 1 if n else 0
    else:
        searcher = _BranchAndBoundSearch(instance, bound)
        searcher.search(0, 1, 0.0, sum(searcher.min_out_edge[1:]))
        best_route = searcher.best_route
        best_cost = compute_tour_cost(best_route, dist)
        expanded = searcher.nodes_expanded
        pruned = searcher.nodes_pruned
        updates = searcher.solution_updates

    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        algorithm_name="Branch_and_Bound",
        instance_name=instance.name,
        dimension=n,
        best_route=best_route,
        best_cost=best_cost,
        execution_time_seconds=elapsed_time,
        operations_count=expanded,
        extra_metrics={
            "nodes_expanded": expanded,
            "nodes_pruned": pruned,
            "best_solution_updates": updates,
            "lower_bound": bound,
        },
    )


def solve(instance: TSPInstance) -> TSPResult:
    """Resolve o TSP por Backtracking com podas por cota inferior (B&B).

    Args:
        instance: Instância do TSP (matriz de custos não negativos).

    Returns:
        TSPResult: Rota ótima com retorno à cidade 0, custo, tempo, nós
        expandidos (operations_count) e nós podados
        (extra_metrics["nodes_pruned"]).

    Complexity:
        Tempo O(n^2 * n!) no pior caso; espaço O(n) de pilha.
    """
    return solve_with_bound(instance, "refinada")
```

Os testes ficam em `src/backtracking/test_branch_and_bound.py` e rodam, a partir da raiz do repositório, com:

```bash
python -m src.backtracking.test_branch_and_bound
```

---

## 3.4. Análise da Complexidade Computacional (Tempo e Espaço)

### Tamanho da árvore de busca

A profundidade $k$ tem $\frac{(n-1)!}{(n-1-k)!}$ nós, que são os arranjos de $k$ cidades entre as $n-1$ que não são a origem. O total de nós da árvore sem poda é

$$N(n) = \sum_{k=0}^{n-1} \frac{(n-1)!}{(n-1-k)!} = (n-1)! \sum_{j=0}^{n-1} \frac{1}{j!} < e \cdot (n-1)!.$$

A árvore tem, portanto, $\Theta((n-1)!)$ nós, menos de $e \approx 2{,}718$ vezes o número de folhas. Para $n = 16$, são $3.554.627.472.076$ nós e $15! = 1.307.674.368.000$ folhas.

### Pior caso: tempo $O(n!)$ com a cota simples e $O(n^2 \cdot n!)$ com a refinada

No pior caso, as podas quase não agem e o número de nós expandidos chega a $\Theta((n-1)!)$. O exemplo de custos iguais com a cota simples, mais abaixo, expande 63% da árvore. Toda busca expande pelo menos os $n$ nós da primeira descida. Em cada nó, o laço percorre os $n-1$ vizinhos e calcula a cota de cada filho:

- **Cota simples:** a soma $\sum_{u \in R} \min d(u, \cdot)$ é atualizada em $O(1)$ ao passar de um nó para o filho. Cada nó custa $O(n)$, e o total é $O(n \cdot (n-1)!) = O(n!)$.
- **Cota refinada:** cada filho exige até $|R| + 1$ buscas de menor aresta, cada uma $O(n)$, ou $O(n^2)$ por filho e $O(n^3)$ por nó. O total é $O(n^3 \cdot (n-1)!) = O(n^2 \cdot n!)$.

A cota refinada é mais cara por nó, mas poda muito mais. Na prática, ela expande de 13 a 38 vezes menos nós e termina antes (Seção 3.5).

### Melhor caso: $\Theta(n)$ nós expandidos

Se todas as arestas têm o mesmo custo $w$, a primeira descida chega a uma rota de custo $U = n w$. A partir daí, todo filho tem $LB_r = g(P) + (|R| + 1) w = n w = U$ e é podado. A busca expande só os $n$ nós dessa descida. Com a cota simples, que ignora a aresta que sai da cidade atual, vale $LB_s = U - w < U$, e só o último nível, em que a cota é exata, é podado. Em um teste com $n = 12$ e custos iguais, a cota refinada expandiu 12 nós e a simples, 68.588.313, ou 63% da árvore. O exemplo mostra que a qualidade da cota decide a eficácia das podas.

### Espaço: $O(n)$

A recursão tem profundidade $n$, e cada chamada guarda um número constante de variáveis. A rota corrente e a melhor rota têm $n + 1$ posições. O espaço auxiliar da busca é $O(n)$. As listas de vizinhos ordenadas somam $O(n^2)$, o mesmo tamanho da matriz de distâncias recebida como entrada. É essa a diferença em relação ao Held-Karp, que guarda $\Theta(n \cdot 2^n)$ estados (Capítulo 5).

---

## 3.5. Resultados Experimentais Locais: Nós Expandidos vs. Nós Podados

### Ambiente de execução

- **Processador:** Intel Xeon @ 2,10 GHz (2 núcleos virtuais)
- **Sistema operacional:** Linux (64 bits)
- **Interpretador:** Python 3.13
- **Comando:** `python -m src.backtracking.test_branch_and_bound`

Os tempos são a mediana de 3 execuções, medidos com `time.perf_counter()` apenas em torno do algoritmo.

### Validação

Antes dos experimentos, o script confere a correção do algoritmo:

- **Casos de borda:** instâncias com 0, 1, 2 e 3 cidades, incluindo uma matriz assimétrica.
- **30 matrizes aleatórias** com $n$ de 4 a 9, metade simétricas e metade assimétricas, com custos inteiros de 1 a 20 para provocar empates. As duas cotas dão sempre o mesmo custo da enumeração completa.
- **Instâncias do grupo:** o custo ótimo coincide com o da Força Bruta para $n \le 10$ e com o do Held-Karp para $n = 12$ e $n = 16$. Toda rota é validada por `validate_tour` e começa e termina na cidade `0`.

### Tabela 3.1 — Branch & Bound com a cota refinada

| Instância | $n$ | Custo Ótimo | Nós Expandidos | Podas Realizadas | $(n-1)!$ | Nós da árvore sem poda | Tempo (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `tiny_4` | 4 | 226,30 | 8 | 4 | 6 | 16 | 0,000015 |
| `small_6` | 6 | 147,14 | 36 | 53 | 120 | 326 | 0,000078 |
| `small_8` | 8 | 277,32 | 49 | 162 | 5.040 | 13.700 | 0,000234 |
| `medium_10` | 10 | 312,11 | 1.186 | 3.619 | 362.880 | 986.410 | 0,006137 |
| `medium_12` | 12 | 280,79 | 1.827 | 8.873 | 39.916.800 | 108.505.112 | 0,013359 |
| `medium_16` | 16 | 368,30 | 166.139 | 982.818 | $1{,}31 \times 10^{12}$ | $3{,}55 \times 10^{12}$ | 1,732759 |

A fração da árvore que precisa ser expandida cai rapidamente com $n$: metade da árvore em `tiny_4`, 0,12% em `medium_10` e cerca de 1 nó em cada 21 milhões em `medium_16`. Em instâncias pequenas, a árvore é rasa e sobra pouco para podar. Conforme $n$ cresce, cada poda perto da raiz elimina uma subárvore de tamanho fatorial.

### Tabela 3.2 — Eficácia das podas: cota simples vs. cota refinada

| Instância | $n$ | Cota | Nós Expandidos | Podas Realizadas | Tempo (s) |
| :--- | :---: | :--- | :---: | :---: | :---: |
| `small_8` | 8 | simples | 619 | 1.114 | 0,000483 |
| `small_8` | 8 | refinada | 49 | 162 | 0,000201 |
| `medium_10` | 10 | simples | 21.220 | 35.684 | 0,017726 |
| `medium_10` | 10 | refinada | 1.186 | 3.619 | 0,005849 |
| `medium_12` | 12 | simples | 26.324 | 91.933 | 0,032797 |
| `medium_12` | 12 | refinada | 1.827 | 8.873 | 0,013395 |
| `medium_16` | 16 | simples | 6.284.091 | 26.349.458 | 9,686351 |
| `medium_16` | 16 | refinada | 166.139 | 982.818 | 1,817531 |

As duas cotas encontram o mesmo ótimo. A refinada expande 12,6, 17,9, 14,4 e 37,8 vezes menos nós em `small_8`, `medium_10`, `medium_12` e `medium_16`. Como ela custa mais por nó, o ganho de tempo é menor que o de nós, mas ainda chega a 5,3 vezes em `medium_16`. A diferença vem das duas informações que a cota simples ignora: a aresta que ainda sai da cidade atual e o fato de que as arestas restantes não podem voltar a cidades já visitadas.

### Comparação com a Força Bruta

Na mesma máquina, a Força Bruta do Capítulo 2 avaliou as $9! = 362.880$ rotas de `medium_10` em 0,175 s, cerca de $4{,}8 \times 10^{-7}$ s por rota. Corrigindo pelo número de arestas somadas em cada rota, a extrapolação dá:

| $n$ | Rotas da Força Bruta | Tempo estimado da Força Bruta | Tempo medido do Branch & Bound |
| :---: | :---: | :---: | :---: |
| 12 | $11! \approx 4{,}0 \times 10^{7}$ | $\approx$ 23 s | 0,013 s |
| 16 | $15! \approx 1{,}3 \times 10^{12}$ | $\approx$ 12 dias | 1,7 s |
| 20 | $19! \approx 1{,}2 \times 10^{17}$ | $\approx$ 3.700 anos | $\approx$ 27 s |

Em `medium_20`, fora da tabela principal, o Branch & Bound expandiu 1.437.257 nós, fez 12.552.793 podas e encontrou o custo 379,34, o mesmo do Held-Karp, em cerca de 27 s. O script comparativo do grupo (`scripts/run_comparison.py`) limita o Branch & Bound a $n \le 16$ para manter o tempo total baixo.

### Análise qualitativa

O Branch & Bound continua exponencial no pior caso, mas o pior caso depende da instância. Nas instâncias euclidianas do projeto, a combinação de três fatores mantém a árvore pequena: a ordem dos filhos produz cedo uma boa incumbente, a cota refinada fica próxima do custo real e cada poda perto da raiz elimina uma subárvore inteira. Com isso, $n = 16$ é resolvido em segundos, enquanto a Força Bruta levaria dias.

Em relação ao Held-Karp, o Branch & Bound foi mais lento em `medium_16` (cerca de 1,7 s contra 0,3 s na mesma máquina), porque o número de nós depende da qualidade das podas e não tem garantia além de $O((n-1)!)$. Em troca, ele usa memória $O(n)$, enquanto o Held-Karp precisa de $\Theta(n \cdot 2^n)$ estados. Em instâncias em que a cota é justa, isso pode permitir resolver tamanhos em que o Held-Karp já esgota a memória. Em instâncias em que a cota é fraca, como no exemplo de custos iguais com a cota simples, o algoritmo se aproxima da Força Bruta.

As referências [2], [7] e [8] citadas neste capítulo encontram-se consolidadas na Seção 8.2 do relatório.
