# Guia de Execução — Integrante 1

**Papel:** Força Bruta & Demonstração Formal de NP-Completude  
**Branch de Trabalho:** `feat/integrante-1-forca-bruta`  
**Pasta de Código Exclusiva:** `src/forca_bruta/`  
**Arquivos de Documentação Exclusivos:**  
* `docs/01_introducao_e_prova_np.md`  
* `docs/02_forca_bruta.md`

---

## 1. Visão Geral das Suas Tarefas

Você é o responsável por estabelecer o alicerce teórico do trabalho e o primeiro algoritmo exato (Força Bruta), que servirá como linha de base (*baseline*) para comparar todos os outros.

### Suas Responsabilidades:
1. **Implementação:** Desenvolver o algoritmo de **Força Bruta Exaustiva** para o TSP em Python, obedecendo rigorosamente à interface `TSPResult` e incluindo a contagem de permutações avaliadas.
2. **Testes Unitários:** Criar o script de teste local testando instâncias pequenas ($n = 4 \dots 10$).
3. **Fundamentação Teórica (Capítulo 1):** Redigir a Introdução do trabalho, a modelagem matemática formal do TSP e a **Demonstração Formal de que o TSP pertence à classe NP e é NP-Completo** (via redução de Ciclo Hamiltoniano, baseando-se no Cormen et al. [1]).
4. **Documentação do Algoritmo (Capítulo 2):** Redigir a explicação do seu algoritmo, complexidade de tempo/espaço ($O(n!)$), colar o código-fonte no texto e apresentar a tabela de resultados locais.

---

## 2. Passo a Passo de Execução

### Passo 1: Inicializar sua Branch de Trabalho
No terminal, certifique-se de estar com a `main` atualizada e crie sua branch:
```bash
git checkout main
git pull origin main
git checkout -b feat/integrante-1-forca-bruta
```

---

### Passo 2: Redigir o Capítulo 1 — Introdução e Prova NP
Edite o arquivo `docs/01_introducao_e_prova_np.md` contendo:
* **Identificação:** Seção de autores em ordem alfabética com matrículas (requisito 43).
* **Introdução:** Descrição formal do TSP, grafos valorados, ciclo hamiltoniano de menor custo e aplicações reais no mundo moderno (PCB, logística, DNA).
* **Prova Formal de NP-Completude:**
  * Prova de pertinência em NP (algoritmo verificador polinomial de certificado em $O(n)$).
  * Redução polinomial de Ciclo Hamiltoniano ($HAM-CYCLE \le_P TSP$).
  * Demonstração bidirecional ($\Rightarrow$ e $\Leftarrow$) conforme o guia `Guias/Explicacao-Problema-TSP.md`.

---

### Passo 3: Implementar a Força Bruta
No arquivo `src/forca_bruta/brute_force_tsp.py`:
1. Importar `TSPInstance` e `TSPResult` de `src.core.tsp_types`.
2. Fixar a cidade inicial como `0` para evitar rotações cíclicas redundantes.
3. Para cada permutação dos vértices restantes $\{1, 2, \dots, n-1\}$:
   * Incrementar o contador de operações (`operations_count += 1`).
   * Somar o custo das arestas consecutivas mais o retorno à cidade `0`.
   * Se o custo for menor que o melhor encontrado até agora, atualizar a melhor rota.
4. Medir o tempo de execução usando `time.perf_counter()`.
5. Retornar o objeto `TSPResult` devidamente preenchido.

---

### Passo 4: Criar e Executar o Script de Teste Local
No arquivo `src/forca_bruta/test_brute_force.py`:
1. Carregar as instâncias de teste `tiny_4` e `small_8` de `data/instances/` usando `src.core.instance_loader`.
2. Executar `solve(instance)`.
3. Validar:
   * A rota começa e termina em `0`?
   * O tamanho da rota é $n + 1$?
   * O número de operações contadas em $n=4$ é exatamente $3! = 6$?
   * O número de operações em $n=8$ é $7! = 5040$?
4. Rodar o teste no terminal:
   ```bash
   python -m src.forca_bruta.test_brute_force
   ```

---

### Passo 5: Redigir o Capítulo 2 — Força Bruta
Edite o arquivo `docs/02_forca_bruta.md` contendo:
* Explicação do paradigma da Força Bruta no TSP.
* Análise da complexidade assintótica teórica: Tempo $O(n \cdot n!)$, Espaço $O(n)$.
* O código-fonte embutido com realce de sintaxe em Python (exigência do professor).
* Tabela com os resultados experimentais obtidos na sua máquina para $n = 4, 6, 8, 10$ (Tempo em segundos e contagem de permutações).
* Discussão sobre a explosão combinatória e a impossibilidade de executar para $n \ge 12$.

---

### Passo 6: Submissão do Pull Request (PR)
Suba seus commits para o GitHub e abra um PR para a branch `main`:
```bash
git push -u origin feat/integrante-1-forca-bruta
```
* No GitHub, preencha a descrição do PR usando o template de `Guias/Contrato-de-Regras.md`.
* Solicite a revisão de pelo menos **um colega do grupo**.
* Após a aprovação do colega, realize o **Squash and Merge**.

---

## 3. Checklist de Entregas e Commits

Marque cada entrega conforme for concluindo e realize o commit correspondente:

- [ ] **Entrega 1.1:** Estrutura inicial e Introdução/Modelagem do TSP
  * Arquivo: `docs/01_introducao_e_prova_np.md`
  * Commit: `docs: redige introdução e modelagem matemática do TSP`
- [ ] **Entrega 1.2:** Demonstração Formal de que o TSP é NP-Completo
  * Arquivo: `docs/01_introducao_e_prova_np.md`
  * Commit: `docs: formaliza prova de NP-completude via redução do ciclo hamiltoniano`
- [ ] **Entrega 1.3:** Implementação do Algoritmo de Força Bruta
  * Arquivo: `src/forca_bruta/brute_force_tsp.py`
  * Commit: `feat: implementa algoritmo exato de força bruta com interface TSPResult`
- [ ] **Entrega 1.4:** Testes Locais e Contagem de Permutações
  * Arquivo: `src/forca_bruta/test_brute_force.py`
  * Commit: `test: adiciona validação da força bruta em instâncias com n=4 e n=8`
- [ ] **Entrega 1.5:** Capítulo Documental da Força Bruta Completo
  * Arquivo: `docs/02_forca_bruta.md`
  * Commit: `docs: adiciona capitulo de forca bruta com analise assintotica e codigo`
- [ ] **Entrega 1.6:** Pull Request Aberto e Aprovado
  * Ação no GitHub: PR revisado e mergeado na `main`.

