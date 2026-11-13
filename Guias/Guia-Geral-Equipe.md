# Guia Geral da Equipe e Governança do Projeto

**Disciplina:** Análise e Projeto de Algoritmos (APA)  
**Instituição:** Instituto de Informática — Universidade Federal de Goiás (UFG)  
**Professor:** André Luiz Moura  
**Tema Sorteado:** **Item 3 — Problema do Caixeiro Viajante (TSP - Traveling Salesperson Problem)**  
**Turma:** **Turma B**

---

## 1. Calendário e Prazos Críticos (Turma B)

* **23/11/2026 (Prazo Fatal):** Entrega da versão final do trabalho escrito (PDF único) e código-fonte compactado via **SIGAA**.
  * Formato do arquivo: `PRIMEIRO_ULTIMONOME.ZIP` (ex.: `MAICON_SILVA.ZIP`).
  * Penalidade do edital: **-0,1 ponto por hora de atraso**.
* **30/11/2026 e 07/12/2026:** Apresentações orais do grupo.
  * Tempo total: **20 minutos**.
  * Equipamento: notebook próprio do grupo.
  * Presença: **obrigatória para todos os 4 integrantes** (a ausência do grupo na data acarreta nota zero na apresentação).
  * Critério de maior peso da avaliação: profundidade da apresentação, análise de complexidade e discussão das aplicações práticas.

---

## 2. Quadro de Integrantes

| Papel no Projeto | Integrante Designado | Matrícula | Branch Pessoal de Trabalho |
| :--- | :--- | :--- | :--- |
| **Integrante 1** | Rodrigo Yuji Okida Tamoto | `201811626` | `feat/integrante-1-forca-bruta` |
| **Integrante 2** | Pedro Lucas Barbosa Guedes | `202305533` | `feat/integrante-2-backtracking` |
| **Integrante 3** | Maicon Brendo da Silva | `202204199` | `feat/integrante-3-prog-dinamica` |
| **Integrante 4** | Victor Hugo Silva Ferreira | `202304809` | `feat/integrante-4-aproximados` |

---

## 3. Matriz de Divisão de Responsabilidades

| Integrante | Implementação Prática (Código em Python) | Capítulo Teórico & Documentação | Escopo Experimental Individual |
| :--- | :--- | :--- | :--- |
| **Integrante 1** | **Força Bruta Exaustiva** ($O(n!)$) com gerador de permutações e contagem exata de rotas. | **Capítulo 1:** Introdução, Modelagem Matemática formal do TSP e **Demonstração Formal de NP-Completude** (Redução do Ciclo Hamiltoniano). | Benchmark individual em instâncias $n = 4 \dots 10$. Tabela de permutações vs. tempo. |
| **Integrante 2** | **Backtracking com Branch & Bound** (Poda por Cota Inferior / *Lower Bound* com arestas mínimas). | **Capítulo 2:** Fundamentação de Backtracking, Espaço de Estados e Análise de Eficácia das Podas. | Benchmark individual em $n = 4 \dots 16$. Métrica: nós gerados vs. nós podados. |
| **Integrante 3** | **Programação Dinâmica (Held-Karp)** ($O(n^2 2^n)$) com memoização e máscaras de bits (*bitmask*). | **Capítulo 3:** **Justificativa Formal da Inviabilidade de Divisão e Conquista** (item 33 do edital) + Análise teórica da PD. | Benchmark individual em $n = 4 \dots 20$. Métrica: subproblemas em cache e uso de memória. |
| **Integrante 4** | **Algoritmos Gulosos & Aproximados:** Vizinho Mais Próximo ($O(n^2)$) + 2-Aproximado com MST e refinamento 2-Opt. | **Capítulo 4:** Teoria de Heurísticas, TSP Métrico (desigualdade triangular) e Prova da Razão de Aproximação $\alpha \le 2$. | Benchmark individual em instâncias grandes ($n = 10 \dots 100+$). Métrica: erro relativo ao ótimo. |

---

## 4. Racionalidade e Critérios da Divisão de Trabalho

### O Desafio do Equilíbrio
O trabalho final exige a cobertura de **6 paradigmas algorítmicos** e duas demandas teóricas densas (Prova NP-Completo e Justificativa de Inviabilidade de D&C).
Se a divisão fosse feita meramente por "linhas de código", haveria um desbalanceamento prejudicial:
* Implementar **Programação Dinâmica (Held-Karp)** com manipulação de bits ou modelar um **Branch & Bound com poda por cota inferior** é computacionalmente e logicamente mais difícil do que implementar uma Força Bruta recursiva ou um Algoritmo Guloso.
* Paralelamente, redigir a **Demonstração Formal de NP-Completude** (redução a partir do Ciclo Hamiltoniano) requer rigor matemático e consulta bibliográfica (Cormen et al.) muito mais intensa do que descrever um algoritmo heurístico.

### A Lógica de Compensação Adotada
Adotou-se o princípio de **compensação cruzada** para garantir que cada um dos 4 membros assuma exatamente **25% de carga de esforço global**:

1. **Integrante 1 (Código Leve + Teoria de Alto Rigor):**
   * A Força Bruta é direta e serve de linha de base (*baseline*) para o grupo.
   * Em compensação, assume a redação da **Prova Formal de que o TSP é NP-Completo** e a estruturação introdutória da documentação formal.
2. **Integrante 2 (Código Intermediário-Avançado + Teoria Analítica de Árvore de Busca):**
   * O Branch & Bound requer cálculo de limites inferiores para evitar a explosão combinatória.
   * Assume a análise teórica e quantitativa da árvore de recursão, medindo a taxa de poda em relação à Força Bruta.
3. **Integrante 3 (Código de Alta Complexidade + Resposta a Requisito Formal do Edital):**
   * O Held-Karp é o algoritmo exato mais sofisticado do projeto, exigindo domínio de máscaras de bits e controle de consumo de memória.
   * Em compensação teórica, atende ao item 33 do edital do professor, elaborando a **Justificativa Formal da Inviabilidade de Divisão e Conquista Exata** para o TSP, fundamentada na literatura clássica.
4. **Integrante 4 (Dois Algoritmos Práticos + Teoria de Aproximação):**
   * Implementa duas abordagens práticas distintas: o Guloso (*Nearest Neighbor*) e o 2-Aproximado (*MST* com busca em profundidade e 2-Opt).
   * Documenta a teoria do TSP Métrico, desigualdade triangular e a dedução teórica da razão de aproximação $\alpha \le 2$.

---

## 5. Arquitetura do Repositório e Princípio de Isolamento

Para eliminar qualquer risco de conflitos de mesclagem (*merge conflicts*) no Git, o repositório é estritamente modular:

```text
Grupo-APA/
├── Guias/
│   ├── Trabalho-Final.md              # Especificação oficial do professor
│   ├── Guia-Geral-Equipe.md           # Este manual de governança
│   ├── Contrato-de-Regras.md          # Contrato de código, tipos e assinaturas
│   ├── Explicacao-Problema-TSP.md     # Dossiê teórico completo do TSP
│   ├── Guia-Integrante-1.md           # Roteiro e checklist do Integrante 1
│   ├── Guia-Integrante-2.md           # Roteiro e checklist do Integrante 2
│   ├── Guia-Integrante-3.md           # Roteiro e checklist do Integrante 3
│   └── Guia-Integrante-4.md           # Roteiro e checklist do Integrante 4
├── data/
│   └── instances/                     # Instâncias de teste compartilhadas (.json)
├── docs/                              # Capítulos modulares do relatório
│   ├── 01_introducao_e_prova_np.md    # Integrante 1
│   ├── 02_forca_bruta.md              # Integrante 1
│   ├── 03_backtracking.md             # Integrante 2
│   ├── 04_inviabilidade_dc.md         # Integrante 3
│   ├── 05_programacao_dinamica.md     # Integrante 3
│   ├── 06_algoritmos_aproximados.md   # Integrante 4
│   └── 07_analise_comparativa.md      # Síntese Conjunta
├── src/
│   ├── core/                          # CONTRATO BASE COMPARTILHADO (imutável)
│   │   ├── tsp_types.py               # TSPInstance, TSPResult
│   │   └── instance_loader.py         # Leitor e gerador de matrizes de adjacência
│   ├── forca_bruta/                   # Pasta exclusiva do Integrante 1
│   ├── backtracking/                  # Pasta exclusiva do Integrante 2
│   ├── dinamica/                      # Pasta exclusiva do Integrante 3
│   └── aproximados/                   # Pasta exclusiva do Integrante 4
├── scripts/
│   ├── generate_sample_instances.py   # Gerador de matrizes de teste
│   ├── run_comparison.py              # Script consolidado de benchmark
│   └── build_final_report.py          # Concatena docs/ em Trabalho-Final-Completo.md
└── README.md                          # Visão geral rápida do projeto
```

### Regra de Ouro de Isolamento
* Cada integrante cria e altera arquivos **apenas dentro de sua subpasta de código** (`src/<sua_pasta>/`) e no **seu arquivo em `docs/`**.
* Ninguém altera `src/core/` ou pastas de outros colegas sem debate e aprovação unânime do grupo.

---

## 6. Fluxo de Trabalho no Git e Regras de Pull Request (PR)

### 1. Branches Pessoais
A branch `main` é estritamente estável e protegida. Todo o trabalho deve ser desenvolvido em branches de feature:
```bash
# Integrante 1
git checkout -b feat/integrante-1-forca-bruta

# Integrante 2
git checkout -b feat/integrante-2-backtracking

# Integrante 3
git checkout -b feat/integrante-3-prog-dinamica

# Integrante 4
git checkout -b feat/integrante-4-aproximados
```

### 2. Padrão de Commits (Conventional Commits)
Mensagens de commit devem seguir o padrão:
* `feat: implementa algoritmo de força bruta com poda simétrica`
* `docs: redige prova formal de NP-completude do TSP`
* `test: adiciona testes unitários para instâncias com n=4 e n=8`
* `fix: corrige cálculo do ciclo de retorno à cidade inicial`
* `perf: otimiza máscara de bits no algoritmo de Held-Karp`

### 3. Política Obrigatória de Pull Requests (PR)
* Nenhum commit deve ser feito diretamente na `main`.
* **Obrigatoriedade de Aprovação:** Para que um PR seja integrado à `main`, ele **DEVE ser revisado e aprovado por pelo menos 1 outro integrante da equipe**.
* **Checklist de Validação do Revisor antes de aprovar:**
  1. O código executa sem erros em Python 3 (`python -m src.<pasta>.test_...`)?
  2. O retorno da função respeita estritamente o objeto `TSPResult` de `src.core.tsp_types`?
  3. A contagem de operações fundamentais foi implementada e é determinística?
  4. O capítulo correspondente em `docs/` está preenchido e inclui os códigos utilizados (conforme exige o item 49 do edital)?
  5. Nenhum arquivo de outra pasta foi alterado inadvertidamente?
* **Tipo de Merge:** Usar preferencialmente **Squash and Merge** no GitHub para manter a branch `main` com histórico limpo e rastreável.

### 4. Sincronização Periódica
Antes de abrir o PR ou sempre que houver novidade na `main`, atualize sua branch de trabalho:
```bash
git checkout main
git pull origin main
git checkout feat/<sua-branch>
git merge main
```

---

## 7. Critérios de Aceite e "Definition of Done" (DoD)

Uma entrega individual só é considerada **concluída (Done)** quando todos os itens abaixo forem cumpridos:

- [ ] **Código Funcional:** Algoritmo implementado na subpasta correspondente, validado e testado.
- [ ] **Ciclo Válido:** A rota retornada começa e termina na mesma cidade de origem e visita cada cidade intermediária exatamente uma vez.
- [ ] **Contagem de Operações:** O algoritmo incrementa e reporta operações fundamentais determinísticas (permutações, podas, subproblemas ou iterações).
- [ ] **Documentação Escrita:** Capítulo correspondente em `docs/` redigido em Markdown de alta qualidade técnica com o código-fonte embutido no texto (requisito obrigatório do professor).
- [ ] **PR Aprovado:** Código revisado e aprovado por ao menos um colega no GitHub.

---

## 8. Etapas Finais de Entrega e Apresentação Oral

1. **Benchmark Unificado:**
   * Com todos os PRs aprovados na `main`, uma máquina designada executará `python scripts/run_comparison.py`.
   * Isso gerará tabelas padronizadas de tempo e operações para o capítulo `docs/07_analise_comparativa.md`.
2. **Geração do Documento Final:**
   * Executar `python scripts/build_final_report.py`.
   * O script concatena os arquivos de `docs/` em `docs/Trabalho-Final-Completo.md`.
   * Exportar para PDF conferindo cabeçalhos com nomes completos em ordem alfabética e matrículas (requisito 43).
3. **Empacotamento ZIP:**
   * Compactar código-fonte e documentação PDF em `NOME_SOBRENOME.ZIP` para submissão no SIGAA até **23/11/2026**.
4. **Preparação dos Slides (20 minutos):**
   * Recomenda-se escolher **1 ou 2 apresentadores principais** com boa oratória (recomendação oficial do professor).
   * Enfatizar a análise de complexidade empírica vs. teórica e as aplicações práticas no mundo real.

