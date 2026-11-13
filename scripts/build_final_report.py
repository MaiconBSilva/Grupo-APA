import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
OUTPUT_FILE = DOCS_DIR / "Trabalho-Final-Completo.md"

CHAPTERS_ORDER = [
    "01_introducao_e_prova_np.md",
    "02_forca_bruta.md",
    "03_backtracking.md",
    "04_inviabilidade_dc.md",
    "05_programacao_dinamica.md",
    "06_algoritmos_aproximados.md",
    "07_analise_comparativa.md",
    "08_conclusao_e_referencias.md",
]

PAGE_BREAK = """

<div style="page-break-after: always; break-after: page;"></div>

\\newpage

"""


def build_final_report():
    print(f"Concatenando capítulos de {DOCS_DIR} para {OUTPUT_FILE}...")
    combined_content = []

    header = f"""---
title: "Trabalho Final de Análise e Projeto de Algoritmos"
subtitle: "Implementação e Análise de Estratégias para o Problema do Caixeiro Viajante (TSP)"
author:
  - "Maicon Brendo da Silva (202204199)"
  - "Pedro Lucas Barbosa Guedes (202305533)"
  - "Rodrigo Yuji Okida Tamoto (201811626)"
  - "Victor Hugo Silva Ferreira (202304809)"
date: "Novembro de 2026"
geometry: "margin=2.5cm"
output: pdf_document
---
{PAGE_BREAK}"""
    combined_content.append(header)

    for chapter_filename in CHAPTERS_ORDER:
        chapter_path = DOCS_DIR / chapter_filename
        if chapter_path.exists():
            print(f" [+] Lendo {chapter_filename}")
            content = chapter_path.read_text(encoding="utf-8")
            combined_content.append(content)
            combined_content.append(PAGE_BREAK)
        else:
            print(f" [!] Aviso: {chapter_filename} ainda não foi criado (será preenchido pelo integrante responsável).")

    OUTPUT_FILE.write_text("\n".join(combined_content), encoding="utf-8")
    print(f"\nDocumento final gerado com sucesso em: {OUTPUT_FILE}")
    print("Dica: você pode converter para PDF usando Pandoc (`pandoc docs/Trabalho-Final-Completo.md -o docs/Trabalho-Final.pdf --pdf-engine=xelatex`) ou via extensão Markdown PDF no VSCode.")


if __name__ == "__main__":
    build_final_report()
