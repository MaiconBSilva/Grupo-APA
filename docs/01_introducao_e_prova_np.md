# 1. Identificação, Introdução e Prova Formal de NP-Completude

**Responsável:** Integrante 1 — Rodrigo Yuji Okida Tamoto (Matrícula: `201811626`)  
**Status:** Concluído

## 1.1. Identificação dos Autores

| Autor | Matrícula |
| :--- | :--- |
| Maicon Brendo da Silva | 202204199 |
| Pedro Lucas Barbosa Guedes | 202305533 |
| Rodrigo Yuji Okida Tamoto | 201811626 |
| Victor Hugo Silva Ferreira | 202304809 |

## 1.2. Introdução ao Problema do Caixeiro Viajante

O Problema do Caixeiro Viajante (*Traveling Salesperson Problem*, TSP) consiste em encontrar uma rota fechada de menor custo que visite cada cidade exatamente uma vez antes do retorno à origem. Ele permite estudar o crescimento combinatório do espaço de soluções e comparar estratégias exatas e aproximadas de projeto de algoritmos [1, 2].

### Modelagem matemática

Representamos as cidades por $V=\{0,\ldots,n-1\}$ e as ligações por um grafo completo não direcionado $K_n$, com $n\geq3$. Cada aresta tem um peso não negativo $w(u,v)=w(v,u)$ que representa distância, tempo ou outro custo. Uma permutação $\pi=(\pi_0,\ldots,\pi_{n-1})$ de $V$ determina um ciclo de custo

$$
C(\pi)=\sum_{i=0}^{n-1}w\bigl(\pi_i,\pi_{(i+1)\bmod n}\bigr).
$$

O termo com índice $n-1$ inclui o retorno à primeira cidade. Na implementação, fixamos $\pi_0=0$, pois qualquer ciclo pode ser escrito a partir dessa cidade.

Na **versão de otimização**, buscamos $\pi^*\in\operatorname{argmin}_{\pi}C(\pi)$. Na **versão de decisão**, recebemos também um limite $B$ e perguntamos se existe uma permutação com $C(\pi)\leq B$. A prova de NP-completude a seguir trata da versão de decisão [1, 4].

### Aplicações práticas

Na distribuição de mercadorias, um modelo básico considera um veículo que parte do depósito, atende os destinos e retorna ao depósito. Os pesos podem representar as distâncias entre os locais. Restrições como capacidade do veículo e janelas de atendimento exigem formulações adicionais.

Na fabricação de placas de circuito impresso, os vértices podem representar pontos de perfuração e o custo pode representar o deslocamento da ferramenta. O objetivo é reduzir o percurso necessário para visitar todos os pontos. Essas aplicações motivam a comparação entre o custo ótimo e soluções obtidas com menor esforço computacional [1, 4].

## 1.3. Demonstração Formal de Pertencimento à Classe NP e NP-Completude

Adotamos a formulação de decisão com pesos inteiros não negativos e limite $B$ codificados em binário. Pesos racionais representados por pares de inteiros também permitem verificação polinomial. Essa formulação explicita a representação finita usada na análise de complexidade [1, 4].

### 1.3.1. Certificado e verificador polinomial

Um certificado é uma sequência de $n$ identificadores de vértices. Cada identificador ocupa $O(\log n)$ bits, de modo que o certificado tem tamanho $O(n\log n)$.

O verificador realiza as seguintes etapas.

1. Verifica se a sequência tem exatamente $n$ elementos.
2. Confere se cada identificador está no intervalo $0,\ldots,n-1$ e aparece uma única vez, usando um vetor booleano de visitados.
3. Soma os pesos das $n$ arestas consecutivas do ciclo, incluindo o retorno à origem.
4. Aceita se, e somente se, a sequência for válida e a soma for menor ou igual a $B$.

Se o verificador aceita, o certificado representa uma rota válida que respeita o limite. Se existe uma rota que respeita o limite, sua sequência de vértices constitui um certificado aceito. Isso estabelece a correção do verificador.

Com acesso direto à matriz e operações aritméticas de custo unitário, o verificador executa $O(n)$ operações e usa $O(n)$ posições auxiliares. Considerando pesos de até $L$ bits, a soma ocupa $O(L+\log n)$ bits. O processamento das somas e da comparação com $B$ continua polinomial no tamanho da entrada. Portanto,

$$
\mathrm{TSP}_{\mathrm{dec}}\in\mathrm{NP}.
$$

A distinção entre encontrar uma solução e verificar um certificado fundamenta a definição de NP [1, 2, 4].

### 1.3.2. Redução polinomial de Ciclo Hamiltoniano

Usamos o problema de **Ciclo Hamiltoniano em grafos simples não direcionados**, que é NP-completo [1, 4]. Dado um grafo $G=(V,E)$ com $n\geq3$, construímos uma instância de TSP no grafo completo com o mesmo conjunto de vértices. Para vértices distintos, definimos

$$
w(u,v)=
\begin{cases}
1, & \text{se }\{u,v\}\in E,\\
2, & \text{se }\{u,v\}\notin E,
\end{cases}
\qquad B=n.
$$

A construção produz uma matriz simétrica. Depois de representar a adjacência do grafo, preenchemos a matriz em $O(n^2)$ tempo. Cada peso ocupa tamanho constante e $B$ ocupa $O(\log n)$ bits, portanto a transformação tem tamanho e tempo polinomiais [1, 4].

### 1.3.3. Equivalência das respostas

**Se $G$ possui um ciclo hamiltoniano, a instância construída de TSP possui uma rota com custo até $B$.**

O ciclo visita cada vértice uma vez e utiliza $n$ arestas de $E$. Cada uma recebe peso 1. Sua rota correspondente tem custo $n=B$.

**Se a instância construída de TSP possui uma rota com custo até $B$, o grafo $G$ possui um ciclo hamiltoniano.**

Uma rota contém $n$ arestas e cada uma tem peso pelo menos 1. Se alguma tivesse peso 2, o custo total seria pelo menos $(n-1)+2=n+1>B$. Logo, todas as arestas da rota têm peso 1 e pertencem a $E$. A mesma sequência forma um ciclo hamiltoniano no grafo original.

Assim,

$$
G\in\mathrm{HAM\text{-}CYCLE}
\iff
f(G)\in\mathrm{TSP}_{\mathrm{dec}},
$$

e a construção polinomial demonstra

$$
\mathrm{HAM\text{-}CYCLE}\leq_p\mathrm{TSP}_{\mathrm{dec}}.
$$

### 1.3.4. Classificação do problema

A redução prova que a versão de decisão do TSP é NP-difícil. Como essa versão também pertence a NP, concluímos que ela é **NP-completa** [1, 4].

A versão de otimização é **NP-difícil**. Um algoritmo que encontrasse seu custo ótimo em tempo polinomial também resolveria a decisão em tempo polinomial, bastando comparar o ótimo com $B$. A classificação de NP-completude fundamenta a discussão do esforço de busca. Ela preserva em aberto a existência de um algoritmo polinomial para o caso geral, questão relacionada a $P=NP$ [1, 4].

As referências [1], [2] e [4] correspondem às entradas da Seção 8.2 do relatório.
