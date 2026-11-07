# Projeto Final de Análise e Projeto de Algoritmos (APA)

**Tema Sorteado:** **Item 3 — Problema do Caixeiro Viajante (TSP - Traveling Salesperson Problem)**  
**Instituição:** Instituto de Informática — Universidade Federal de Goiás (UFG)  
**Professor:** André Luiz Moura  
**Turma:** **Turma B**

---

## 📅 Datas Críticas e Entregas (Turma B)

* **23/11/2026 (Prazo Final):** Entrega do trabalho escrito (PDF único) e código-fonte compactado via **SIGAA** (`NOME_SOBRENOME.ZIP`).
* **30/11/2026 e 07/12/2026:** Apresentações orais (20 minutos com notebook próprio e presença obrigatória de todos).

---

## 👥 Integrantes do Grupo

1. Maicon Brendo da Silva
2. Pedro Lucas Barbosa Guedes
3. Rodrigo Yuji Okida Tamoto
4. Victor Hugo Silva Ferreira

---

## 🧭 Guias e Documentação Rápida

| Guia | Descrição | Link de Acesso |
| :--- | :--- | :--- |
| **Guia Geral da Equipe** | Playbook com regras de governança, GitFlow, aprovação obrigatória de PRs e justificativa detalhada da divisão de trabalho. | [Guia-Geral-Equipe.md](file:///Guias/Guia-Geral-Equipe.md) |
| **Contrato de Regras Técnicas** | Especificações de código em Python 3, assinaturas das funções, tipos de dados e padrões de contagem de operações. | [Contrato-de-Regras.md](file:///Guias/Contrato-de-Regras.md) |
| **Dossiê Teórico do TSP** | Formalização matemática, prova formal de que o TSP é NP-Completo, justificativa de inviabilidade de D&C e descrição dos 6 paradigmas. | [Explicacao-Problema-TSP.md](file:///Guias/Explicacao-Problema-TSP.md) |
| **Guia — Integrante 1** | Roteiro passo a passo e checklist de commits para **Força Bruta** e **Demonstração de NP-Completude**. | [Guia-Integrante-1.md](file:///Guias/Guia-Integrante-1.md) |
| **Guia — Integrante 2** | Roteiro passo a passo e checklist de commits para **Backtracking com Branch & Bound** e **Análise de Podas**. | [Guia-Integrante-2.md](file:///Guias/Guia-Integrante-2.md) |
| **Guia — Integrante 3** | Roteiro passo a passo e checklist de commits para **Programação Dinâmica (Held-Karp)** e **Inviabilidade de D&C**. | [Guia-Integrante-3.md](file:///Guias/Guia-Integrante-3.md) |
| **Guia — Integrante 4** | Roteiro passo a passo e checklist de commits para **Gulosos**, **2-Aproximado (MST)** e **Heurística 2-Opt**. | [Guia-Integrante-4.md](file:///Guias/Guia-Integrante-4.md) |
| **Edital Oficial** | Requisitos oficiais, critérios de avaliação e ementa completa fornecida pelo professor. | [Trabalho-Final.md](file:///Guias/Trabalho-Final.md) |

---

## ⚖️ Matriz de Divisão de Responsabilidades

| Integrante | Código Prático (Python 3) | Parte Teórica e Relatório | Branch Pessoal |
| :--- | :--- | :--- | :--- |
| **Integrante 1** | Força Bruta ($O(n!)$) | Introdução e Prova Formal NP-Completo | `feat/integrante-1-forca-bruta` |
| **Integrante 2** | Backtracking com Branch & Bound | Fundamentação de Busca e Eficácia das Podas | `feat/integrante-2-backtracking` |
| **Integrante 3** | Programação Dinâmica (Held-Karp com bitmask) | Justificativa Formal da Inviabilidade de D&C | `feat/integrante-3-prog-dinamica` |
| **Integrante 4** | Vizinho Mais Próximo e 2-Aproximado (MST) + 2-Opt | Teoria de Heurísticas e Prova do Fator $\alpha \le 2$ | `feat/integrante-4-aproximados` |

> *A fundamentação completa do equilíbrio de carga e compensação entre esforço algorítmico e densidade teórica está detalhada na Seção 4 do [Guia Geral da Equipe](file:///Guias/Guia-Geral-Equipe.md).*

---

## 🗂️ Estrutura do Repositório

```text
Grupo-APA/
├── data/
│   └── instances/             # Instâncias padrão de teste (.json) de n=4 até n=100
├── docs/                      # Capítulos modulares em Markdown
│   ├── 01_introducao_e_prova_np.md
│   ├── 02_forca_bruta.md
│   ├── 03_backtracking.md
│   ├── 04_inviabilidade_dc.md
│   ├── 05_programacao_dinamica.md
│   ├── 06_algoritmos_aproximados.md
│   ├── 07_analise_comparativa.md
│   └── 08_conclusao_e_referencias.md
├── Guias/                     # Guias de execução, contratos e dossiê teórico
├── scripts/
│   ├── generate_sample_instances.py  # Gera instâncias de teste euclidianas
│   ├── run_comparison.py             # Executa o benchmark comparativo unificado
│   ├── plot_results.py               # Gera os gráficos comparativos em docs/images/
│   └── build_final_report.py         # Concatena docs/ em Trabalho-Final-Completo.md
├── src/
│   ├── core/                  # Contrato base compartilhado (tipos e loaders)
│   ├── forca_bruta/           # Módulo exclusivo do Integrante 1
│   ├── backtracking/          # Módulo exclusivo do Integrante 2
│   ├── dinamica/              # Módulo exclusivo do Integrante 3
│   └── aproximados/           # Módulo exclusivo do Integrante 4
└── README.md
```

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar e Acessar o Repositório
```bash
git clone https://github.com/MaiconBSilva/Grupo-APA.git
cd Grupo-APA
```

### 2. Gerar Instâncias de Teste (se necessário)
```bash
python scripts/generate_sample_instances.py
```

### 3. Executar o Benchmark Comparativo Unificado
```bash
python scripts/run_comparison.py
```

### 4. Gerar Gráficos para o Relatório e Slides (Opcional)
```bash
pip install -r requirements.txt
python scripts/plot_results.py
```

### 5. Compilar o Relatório Final para PDF
```bash
python scripts/build_final_report.py
```
O script gera o arquivo unificado `docs/Trabalho-Final-Completo.md`, que pode ser exportado para PDF utilizando Pandoc ou a extensão *Markdown PDF* do VSCode.

---

## 🛡️ Regras de Git e Governança
1. **Nenhum commit direto na `main`:** todo trabalho é feito na sua respectiva branch de feature.
2. **Revisão Obrigatória:** Nenhum Pull Request é mergeado sem a validação e aprovação de pelo menos um outro colega de grupo.
3. **Isolamento de Pastas:** Cada integrante altera apenas seus arquivos de código em `src/` e seus capítulos em `docs/`.
