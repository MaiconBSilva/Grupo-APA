# Estrutura, Regras e Requisitos do Trabalho Final de APA

Implementação e Análise de Estratégias de Algoritmos para Solução de Problema NP

Tema Sorteado: **PROBLEMA DO CAIXEIRO VIAJANTE** (Traveling Salesperson Problem — TSP)

Integrantes:
- Maicon Brendo da Silva
- Pedro Lucas Barbosa Guedes
- Rodrigo Yuji Okida Tamoto
- Victor Hugo Silva Ferreira

## Descrição

O trabalho prático consiste em implementar e analisar algoritmos de diferentes paradigmas, realizando a análise da complexidade computacional por contagem de instruções e a análise do desempenho pela medição dos tempos de execução.

Na documentação do trabalho, deverá ser demonstrado formalmente que o problema sorteado ou selecionado pertence à classe NP [1, 2], com fundamentação teórica e referências bibliográficas.

Deverá ser implementada a solução do problema, usando diferentes estratégias:

- Força Bruta

- Backtracking

- Divisão e Conquista

- Programação Dinâmica

- Algoritmos Gulosos

- Algoritmos Aproximados ou Heurísticas

Caso não seja tecnicamente viável resolver o problema utilizando qualquer uma das estratégias de projeto e análise de algoritmos mencionadas anteriormente, deverão ser apresentadas justificativas fundamentadas, acompanhadas de referências bibliográficas pertinentes.

## O que deve ser entregue

- Códigos-fonte dos programas em Java, Python, C ou C++ (bem identado e comentado).

- Documentação do trabalho.

Entre outras coisas, a documentação deve conter:

1. Identificação dos autores do trabalho (nomes completos em ordem alfabética seguidos do núm. de matrícula).

2. Introdução: Descrição do problema a ser resolvido pelo grupo de trabalho.

3. Prova: Provar que o problema pertence à classe NP.

4. Implementação: Descrição sobre as implementações. Muito importante: os códigos utilizados nas implementações devem ser inseridos na documentação.

5. Análise de Complexidade: Estudo da complexidade de tempo e espaço das funções implementadas.

6. Análise de Resultados: Comparar os dados obtidos e discorrer sobre eles.

7. Conclusão: Comentários gerais sobre o trabalho e as principais dificuldades encontradas em sua implementação.

8. Bibliografia: Bibliografia utilizada para o desenvolvimento do trabalho, incluindo sítio da Internet se for o caso. Uma referência bibliográfica deve ser citada no texto onde é utilizada.

9. Formato final: PDF.

## Referências

- [1] T.H. Cormen, C.E. Leiserson, R.L. Rivest, and C. Stein. Introduction to Algorithms. The MIT Press/McGraw- Hill, 3rd edition, 2009.

- [2] N. Ziviani. Projeto de Algoritmos com implementações em Java e C++. Cengage Learning (Thomson/Pioneira), São Paulo, 1st edition, 2006.


## Temas a serem sorteados

#### 1. CLIQUE EM GRAFOS (Clique)  
- Dado um grafo G=(V,E) e um inteiro k, existe um subconjunto de, pelo menos, k vértices tal que todos os pares de vértices desse subconjunto são conectados por uma aresta?

#### 2. COLORAÇÃO EM GRAFOS (Graph Coloring)
- Dado um grafo G=(V,E) e um inteiro k, é possível atribuir, no máximo, k cores aos vértices, de modo que quaisquer dois vértices adjacentes tenham cores diferentes?

#### 3. PROBLEMA DO CAIXEIRO VIAJANTE (Traveling Salesperson Problem — TSP)

- Dado um conjunto de cidades, as distâncias entre elas e um limite B, existe uma rota que visita cada cidade exatamente uma vez, retorna à cidade de origem e possui custo total menor ou igual a B?

#### 4. MOCHILA BINÁRIA (0–1 Knapsack)

- Dados n itens, cada um com peso pi e valor vi, uma capacidade máxima C e um valor-alvo V, existe uma seleção de itens, respeitando a capacidade da mochila, cujo valor total seja maior ou igual a V? Cada item pode ser selecionado, no máximo, uma vez.

#### 5. CAMINHO HAMILTONIANO (Hamiltonian Path)

- Dado um grafo G=(V,E), existe um caminho que visita cada vértice exatamente uma vez?

#### 6. CAMPO MINADO (Minesweeper Consistency)

- Dado um tabuleiro parcialmente revelado de Campo Minado, com os números já revelados e as posições conhecidas de células seguras, existe uma distribuição de minas nas células ainda não reveladas que sejaconsistente com todos os números apresentados?

#### 7. PARTIÇÃO DE NÚMEROS (Partition Problem)

- Dado um conjunto de inteiros positivos, é possível dividi-lo em dois subconjuntos disjuntos cuja soma dos elementos seja igual?

#### 8. TIME TABLING (PROBLEMA DE ELABORAÇÃO DE HORÁRIOS)

- Dadas atividades, horários disponíveis, recursos e restrições de incompatibilidade, existe uma grade de horários que atribua um horário a cada atividade, respeitando todas as restrições especificadas?

#### 9. PROBLEMA DO EMPACOTAMENTO (Bin Packing)

- Dados n itens com tamanhos conhecidos, recipientes de capacidade C e um inteiro k, é possível distribuir todos os itens em, no máximo, k recipientes, sem exceder a capacidade de nenhum deles?

#### 10. CONJUNTO INDEPENDENTE (Independent Set)

- Dado um grafo G=(V,E) e um inteiro k, existe um subconjunto de, pelo menos, k vértices tal que não exista nenhuma aresta conectando dois vértices desse subconjunto?

#### 11. ÁRVORE DE STEINER (Steiner Tree)

- Dado um grafo ponderado, um conjunto de vértices terminais que precisam ser conectados e um limite de custo B, existe uma árvore que conecta todos os vértices terminais e cujo custo total é menor ou igual a B?

#### 12. MAIOR SUBSEQUÊNCIA COMUM ENTRE DUAS STRINGS (Longest Common Subsequence — LCS)

- Dadas duas strings S1 e S2 e um inteiro positivo k, existe uma subsequência comum às duas strings cujo comprimento seja maior ou igual a k?

#### 13. COBERTURA DE VÉRTICES (Vertex Cover)

- Existe um conjunto de, no máximo, k vértices que cobre todas as arestas do grafo?

#### 14. COBERTURA DE CONJUNTOS (Set Cover)

- Dado um universo de elementos e uma coleção de subconjuntos, é possível cobrir todo o universo utilizando, no máximo, k subconjuntos?

#### 15. SOMA DE SUBCONJUNTOS (Subset Sum)

- Existe um subconjunto de números inteiros cuja soma é exatamente um valor-alvo T?

#### 16. EMPACOTAMENTO DE CONJUNTOS (Set Packing)

- É possível selecionar pelo menos k subconjuntos dois a dois disjuntos?

#### 17. CONJUNTO INTERCEPTADOR (Hitting Set)

- Existe um conjunto de, no máximo, k elementos que intersecta todos os subconjuntos de uma coleção?

#### 18. COBERTURA EXATA (Exact Cover)

- Existe uma seleção de subconjuntos que cobre cada elemento do universo exatamente uma vez?

#### 19. EMPARELHAMENTO TRIDIMENSIONAL (3-Dimensional Matching)

- Dadas triplas de três conjuntos distintos, existe uma coleção de triplas disjuntas que utiliza todos os elementos?

#### 20. CONJUNTO DE VÉRTICES DE REALIMENTAÇÃO (Feedback Vertex Set)

- É possível remover, no máximo, k vértices de um grafo para eliminar todos os ciclos?

#### 21. CICLO HAMILTONIANO DIRECIONADO

- Existe um ciclo direcionado que visita cada vértice exatamente uma vez e retorna ao vértice inicial?

#### 22. COBERTURA POR CLIQUES (Clique Cover)

- Os vértices podem ser cobertos por, no máximo, k cliques?

#### 23. DIVISÃO DE CONJUNTOS (Set Splitting)

- É possível dividir um universo em duas partes de modo que cada conjunto de uma coleção tenha elementos nas duas partes?

#### 24. CORTE MÁXIMO (Max-Cut)

- Existe uma partição dos vértices que corta pelo menos k arestas?

#### 25. ESCALONAMENTO DE TAREFAS (Job Scheduling)

- Em uma formulação clássica com restrições de precedência e prazo, é possível programar todas as tarefas para concluir dentro do prazo especificado?

#### 26. CONJUNTO DOMINANTE (Dominating Set)

- Existe um conjunto de, no máximo, k vértices tal que todo vértice do grafo pertence ao conjunto ou é adjacente a algum vértice dele?


## Observações adicionais

- Nota máxima: 10,0 (dez vírgula zero) pontos.

- Forma de Entrega

  - A entrega DEVERÁ ser realizada exclusivamente pela plataforma SIGAA, mediante o envio de um único arquivo compactado no formato ZIP, contendo o código-fonte, os arquivos complementares necessários e a documentação do trabalho. Não serão aceitas entregas por e-mail.

  - O arquivo ZIP deverá ser nomeado com o primeiro e o último nome de um dos integrantes do grupo, separados por sublinhado, conforme o seguinte exemplo: ADELIA_COSTA.ZIP.

- Datas/prazos importantes

  - Turma A:

    - Entregas do trabalho escrito: 11/11/2026

    - Apresentações orais: 17 e 24/11/2026

  - Turma B:

    - Entregas do trabalho escrito: 23/11/2026

    - Apresentações orais: 30/11 e 07/12/2026

  - Tempo de cada apresentação: 20 minutos

- Cada grupo deverá ser composto por 4 (quatro) integrantes. Não serão aceitos trabalhos realizados individualmente.

- Recomenda-se que a elaboração do trabalho seja iniciada o quanto antes, evitando-se deixar sua execução para os últimos dias do prazo estabelecido.

- O critério de maior peso na avaliação será a profundidade da apresentação, especialmente no que se refere à análise e à discussão das aplicações práticas do problema estudado.

- Cada grupo deverá apresentar o Trabalho Final utilizando notebook próprio e o equipamento de projeção disponibilizado pela Universidade.

- A presença de todos os integrantes do grupo será obrigatória durante as apresentações orais dos trabalhos.

- Trabalhos e códigos-fonte copiados de outros grupos serão avaliados com nota 0,0 (zero vírgula zero). Da mesma forma, em caso de plágio comprovado, os trabalhos originais dos quais houve cópia também receberão nota zero, em razão da impossibilidade de assegurar a originalidade e a autoria efetiva do material apresentado.

- Cálculo da nota: (Nota Trabalho Escrito + Nota Apresentação Oral) / 2.

- Os trabalhos escritos entregues fora do prazo estabelecido sofrerão desconto de 0,1 (zero vírgula um) ponto por hora de atraso.

- O grupo que não realizar a apresentação do trabalho na data e no horário estabelecidos receberá nota 0,0 (zero vírgula zero) nesse quesito da avaliação.

- Recomenda-se que apenas um ou dois integrantes do grupo realizem a apresentação, devendo ser escolhidos aqueles que demonstrarem maior aptidão para essa atividade.

- Solicita-se que sejam evitadas discussões improdutivas com o professor com o intuito de postergar a data de entrega do trabalho, uma vez que não há disponibilidade no calendário acadêmico para adiamentos.


