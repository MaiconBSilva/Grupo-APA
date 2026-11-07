"""
Script utilitário para geração automática dos gráficos comparativos do TSP.
Salva os gráficos gerados no diretório docs/images/ para inclusão direta no relatório e nos slides.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.instance_loader import load_instance_from_json
from scripts.run_comparison import get_available_solvers


def generate_benchmark_plots():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n[!] Aviso: 'matplotlib' não está instalado.")
        print("Para gerar os gráficos automáticos, instale com: pip install -r requirements.txt")
        return

    images_dir = REPO_ROOT / "docs" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    instances_dir = REPO_ROOT / "data" / "instances"
    instances_files = sorted(
        [p for p in instances_dir.glob("*.json") if "berlin" not in p.stem],
        key=lambda p: int(p.stem.split("_")[1]) if "_" in p.stem else 0
    )

    solvers = get_available_solvers()
    if not solvers:
        print("\n[!] Nenhum algoritmo implementado encontrado em src/ para plotagem.")
        return

    print("Coletando dados para os gráficos de desempenho...")
    data_by_solver = {name: {"n": [], "time": [], "cost": []} for name in solvers}

    for inst_path in instances_files:
        inst = load_instance_from_json(inst_path)
        for name, (solve_fn, max_n) in solvers.items():
            if inst.dimension <= max_n:
                try:
                    res = solve_fn(inst)
                    data_by_solver[name]["n"].append(inst.dimension)
                    data_by_solver[name]["time"].append(res.execution_time_seconds)
                    data_by_solver[name]["cost"].append(res.best_cost)
                except Exception as e:
                    print(f"Erro ao executar {name} em {inst.name}: {e}")

    # 1. Gráfico de Tempo de Execução vs. n (Escala Logarítmica)
    plt.figure(figsize=(9, 5))
    for name, metrics in data_by_solver.items():
        if metrics["n"]:
            plt.plot(metrics["n"], metrics["time"], marker="o", linewidth=2, label=name)

    plt.yscale("log")
    plt.title("Comparativo de Desempenho: Tempo de Execução vs. Número de Cidades (n)", fontsize=12)
    plt.xlabel("Dimensão da Instância (n cidades)", fontsize=10)
    plt.ylabel("Tempo de Execução em Segundos (Escala Logarítmica)", fontsize=10)
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    time_plot_path = images_dir / "comparativo_tempo_execucao.png"
    plt.savefig(time_plot_path, dpi=300)
    plt.close()
    print(f" [+] Gráfico de tempos salvo em: {time_plot_path}")

    # 2. Gráfico de Custo da Rota vs. n
    plt.figure(figsize=(9, 5))
    for name, metrics in data_by_solver.items():
        if metrics["n"]:
            plt.plot(metrics["n"], metrics["cost"], marker="s", linewidth=2, label=name)

    plt.title("Comparativo de Qualidade da Solução: Custo Total vs. Dimensão (n)", fontsize=12)
    plt.xlabel("Dimensão da Instância (n cidades)", fontsize=10)
    plt.ylabel("Custo Total da Rota Encontrada", fontsize=10)
    plt.grid(True, ls="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    cost_plot_path = images_dir / "comparativo_custo_solucao.png"
    plt.savefig(cost_plot_path, dpi=300)
    plt.close()
    print(f" [+] Gráfico de custos salvo em: {cost_plot_path}")
    print("\nTodos os gráficos foram gerados com sucesso em docs/images/!")


if __name__ == "__main__":
    generate_benchmark_plots()

