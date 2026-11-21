# 8. Conclusão e Referências Bibliográficas

**Responsáveis:** Todo o grupo  
**Status:** Concluído

---

## 8.1. Conclusão e Principais Dificuldades Encontradas

O desenvolvimento deste trabalho permitiu investigar, sob as perspectivas teórica e experimental, o **Problema do Caixeiro Viajante (*Traveling Salesperson Problem* — TSP)** ao longo de seis paradigmas clássicos de Projeto e Análise de Algoritmos. Partindo da formalização matemática e da demonstração rigorosa de **NP-Completude** por redução polinomial a partir do Ciclo Hamiltoniano ($\mathrm{HAM\text{-}CYCLE} \le_p \mathrm{TSP}_{\mathrm{dec}}$) [1, 4], verificou-se empiricamente como a barreira de intratabilidade assintótica se manifesta na prática e como diferentes estratégias algorítmicas contornam — ou sucumbem a — essa explosão combinatória.

### Síntese das Conclusões Obtidas

1. **Limites dos Paradigmas Exatos:**
   - A **Força Bruta** ($\Theta(n!)$) comprovou-se indispensável como oráculo de validação (*ground truth*) para instâncias pequenas ($n \le 10$), mas seu crescimento fatorial inviabiliza qualquer aplicação direta já a partir de uma dezena de cidades.
   - O **Backtracking com Branch & Bound** demonstrou o poder da poda por cota inferior: ao ordenar as ramificações pela cidade mais próxima e estimar o custo residual mínimo de saída de cada vértice ativo, eliminou mais de $99{,}99999\%$ da árvore de busca em $n = 16$, mantendo consumo de memória estritamente linear $O(n)$ [2, 7, 8].
   - A análise formal de **Divisão e Conquista** evidenciou que nem todo paradigma clássico se adapta à resolução exata de problemas com acoplamento global: como um ciclo hamiltoniano ótimo pode cruzar a fronteira de qualquer bipartição de vértices múltiplas vezes, os subproblemas não são independentes e a etapa de combinação degenera para complexidade fatorial [1, 5, 9].
   - A **Programação Dinâmica (Bellman-Held-Karp)** superou essa limitação ao substituir partições disjuntas por subconjuntos sobrepostos memoizados via máscaras de bits (*bitmasks*), reduzindo a complexidade temporal de $\Theta(n!)$ para $\Theta(n^2 2^n)$ [3, 6]. Isso permitiu resolver $n = 20$ de forma exata em cerca de $10{,}6\text{ s}$ (frente a $19! \approx 1{,}21 \times 10^{17}$ permutações), mas revelou a troca direta de tempo por espaço: o crescimento exponencial da tabela $\Theta(n 2^n)$ torna a memória RAM o fator limitante absoluto para $n > 22$.

2. **Eficácia dos Paradigmas Polinomiais (Gulosos, Aproximados e Heurísticas):**
   - Para instâncias de escala realista ($n = 50, 52, 100$), os algoritmos polinomiais resolveram o problema em frações de milissegundo a poucos milissegundos.
   - Enquanto a escolha estritamente local do **Vizinho Mais Próximo** ($\Theta(n^2)$) apresentou desvios de até $19{,}08\%$ acima do ótimo, o algoritmo **2-Aproximado baseado em Árvore Geradora Mínima (MST)** apoiado pela desigualdade triangular garantiu formalmente soluções limitadas a duas vezes o ótimo ($\alpha \le 2$) [1]. Combinado ao refinamento de busca local **2-Opt**, alcançou o ótimo exato em todas as instâncias até $n = 12$ e manteve erro de apenas $12{,}30\%$ na instância clássica `berlin52` ($n = 52$) em $4{,}2\text{ ms}$.

### Principais Dificuldades Encontradas na Implementação

Durante o desenvolvimento modular e a integração dos algoritmos pelas quatro frentes da equipe, destacaram-se quatro desafios técnicos principais:

1. **Manipulação de Máscaras de Bits e Consumo de Memória no Held-Karp (Integrante 3):**
   - Uma implementação inicial utilizando dicionários Python (`dict[(mask, v), float]`) ou matrizes bidimensionais aninhadas sofria com elevado *overhead* de objetos e *hashing*, tornando $n = 20$ excessivamente lento e pesado em memória. Foi necessário reestruturar as tabelas `dp` e `parent` em vetores unidimensionais planos de tamanho $(n - 1)2^{n - 1}$ indexados por deslocamento aritmético (`submask * stride + v_idx`) e iterar apenas sobre bits ativos com a operação bitwise `lsb = rem & -rem`.
2. **Qualidade e Admissibilidade da Cota Inferior no Branch & Bound (Integrante 2):**
   - A cota inferior simples (soma da menor aresta global de cada cidade não visitada) deixava de considerar a aresta que sai da cidade atual e permitia arestas apontando para cidades já visitadas, resultando em podas fracas ($6{,}28$ milhões de nós expandidos em $n = 16$). O desenvolvimento da **cota refinada** com listas de vizinhos pré-ordenadas por distância e interrupção antecipada (*early exit*) quando a soma parcial atinge a incumbente $U$ reduziu os nós expandidos em **37,8 vezes** sem violar a admissibilidade matemática da poda.
3. **Prevenção de Laços e Índices de Borda no Refinamento 2-Opt (Integrante 4):**
   - Na implementação da busca local 2-Opt sobre ciclos fechados `[0, ..., 0]` de tamanho $n + 1$, foi preciso cuidado especial para evitar avaliar pares de arestas adjacentes (como a primeira aresta `first_edge == 0` simultaneamente à última aresta `second_edge == n - 1` que compartilham o vértice `0`) e para garantir critério de melhoria estrita (`new_edges_cost < old_edges_cost`), evitando ciclos infinitos de trocas degeneradas por erro de ponto flutuante.
4. **Padronização de Contratos e Determinismo das Métricas (Integração da Equipe):**
   - Garantir que quatro implementações independentes convergissem sem conflitos para o benchmark unificado exigiu a definição prévia de um contrato estrito em `src/core/tsp_types.py` (`TSPInstance`, `TSPResult`, arredondamento consistente em `compute_tour_cost` e verificação de ciclo hamiltoniano em `validate_tour`), assegurando que todas as contagens de operações fundamentais fossem determinísticas e reprodutíveis em qualquer sistema operacional.

---

## 8.2. Referências Bibliográficas

1. **[1]** CORMEN, Thomas H.; LEISERSON, Charles E.; RIVEST, Ronald L.; STEIN, Clifford. **Introduction to Algorithms**. 3. ed. Cambridge: The MIT Press / McGraw-Hill, 2009. (Cap. 2, Cap. 4: *Divide-and-Conquer*, Cap. 15: *Dynamic Programming*, Cap. 34: *NP-Completeness* e Cap. 35: *Approximation Algorithms / The Traveling-Salesperson Problem*).
2. **[2]** ZIVIANI, Nivio. **Projeto de Algoritmos com implementações em Java e C++**. 1. ed. São Paulo: Cengage Learning (Thomson/Pioneira), 2006.
3. **[3]** HELD, Michael; KARP, Richard M. **A Dynamic Programming Approach to Sequencing Problems**. *Journal of the Society for Industrial and Applied Mathematics (SIAM)*, v. 10, n. 1, p. 196–210, 1962.
4. **[4]** GAREY, Michael R.; JOHNSON, David S. **Computers and Intractability: A Guide to the Theory of NP-Completeness**. New York: W. H. Freeman & Co., 1979.
5. **[5]** KLEINBERG, Jon; TARDOS, Éva. **Algorithm Design**. Boston: Pearson / Addison-Wesley, 2006. (Cap. 5: *Divide and Conquer*, Cap. 6: *Dynamic Programming* e Cap. 8: *NP and Computational Intractability*).
6. **[6]** BELLMAN, Richard. **Dynamic Programming Treatment of the Travelling Salesman Problem**. *Journal of the ACM (JACM)*, v. 9, n. 1, p. 61–63, 1962.
7. **[7]** LAND, Ailsa H.; DOIG, Alison G. **An Automatic Method of Solving Discrete Programming Problems**. *Econometrica*, v. 28, n. 3, p. 497–520, 1960.
8. **[8]** LITTLE, John D. C.; MURTY, Katta G.; SWEENEY, Dura W.; KAREL, Caroline. **An Algorithm for the Traveling Salesman Problem**. *Operations Research*, v. 11, n. 6, p. 972–989, 1963.
9. **[9]** KARP, Richard M. **Probabilistic Analysis of Partitioning Algorithms for the Traveling-Salesman Problem in the Plane**. *Mathematics of Operations Research*, v. 2, n. 3, p. 209–224, 1977.
