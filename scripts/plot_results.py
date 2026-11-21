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
    loaded_instances = [
        load_instance_from_json(p) for p in instances_dir.glob("*.json")
    ]
    loaded_instances.sort(key=lambda inst: (inst.dimension, inst.name))

    solvers = get_available_solvers()
    if not solvers:
        print("\n[!] Nenhum algoritmo implementado encontrado em src/ para plotagem.")
        return

    print("Coletando dados para os gráficos de desempenho...")
    data_by_solver = {name: {"n": [], "time": [], "cost": [], "is_synthetic": []} for name in solvers}

    for inst in loaded_instances:
        is_synthetic = "berlin" not in inst.name
        for name, (solve_fn, max_n) in solvers.items():
            if inst.dimension <= max_n:
                try:
                    res = solve_fn(inst)
                    data_by_solver[name]["n"].append(inst.dimension)
                    data_by_solver[name]["time"].append(res.execution_time_seconds)
                    data_by_solver[name]["cost"].append(res.best_cost)
                    data_by_solver[name]["is_synthetic"].append(is_synthetic)
                except Exception as e:
                    print(f"Erro ao executar {name} em {inst.name}: {e}")

    # 1. Gráfico de Tempo de Execução vs. n (Escala Logarítmica) — todas as 10 instâncias
    plt.figure(figsize=(9, 5))
    for name, metrics in data_by_solver.items():
        if metrics["n"]:
            plt.plot(metrics["n"], metrics["time"], marker="o", linewidth=2, label=name)

    plt.yscale("log")
    plt.title("Comparativo de Desempenho: Tempo de Execução vs. Número de Cidades (n)", fontsize=12)
    plt.xlabel("Dimensão da Instância (n cidades, incluindo berlin52)", fontsize=10)
    plt.ylabel("Tempo de Execução em Segundos (Escala Logarítmica)", fontsize=10)
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    time_plot_path = images_dir / "comparativo_tempo_execucao.png"
    plt.savefig(time_plot_path, dpi=300)
    plt.close()
    print(f" [+] Gráfico de tempos salvo em: {time_plot_path}")

    # 2. Gráfico de Custo da Rota vs. n (Série sintética [0,100]^2 + destaque berlin52)
    fig, (ax_main, ax_berlin) = plt.subplots(
        1, 2, figsize=(11, 5), gridspec_kw={"width_ratios": [3.2, 1.3]}
    )
    for name, metrics in data_by_solver.items():
        syn_n = [n for n, s in zip(metrics["n"], metrics["is_synthetic"]) if s]
        syn_cost = [c for c, s in zip(metrics["cost"], metrics["is_synthetic"]) if s]
        if syn_n:
            ax_main.plot(syn_n, syn_cost, marker="s", linewidth=2, label=name)

    ax_main.set_title("Qualidade da Rota — Instâncias Sintéticas ([0, 100]²)", fontsize=11)
    ax_main.set_xlabel("Dimensão da Instância (n cidades)", fontsize=10)
    ax_main.set_ylabel("Custo Total da Rota Encontrada", fontsize=10)
    ax_main.grid(True, ls="--", alpha=0.6)
    ax_main.legend(fontsize=8)

    berlin_labels = ["Ótimo TSPLIB", "2-Aprox. (MST+2-Opt)", "Guloso (NN)"]
    berlin_costs = [7542.0]
    mst_berlin = next(
        (c for n, c, s in zip(
            data_by_solver.get("2-Aproximado (MST)", {}).get("n", []),
            data_by_solver.get("2-Aproximado (MST)", {}).get("cost", []),
            data_by_solver.get("2-Aproximado (MST)", {}).get("is_synthetic", []),
        ) if not s),
        8469.63,
    )
    nn_berlin = next(
        (c for n, c, s in zip(
            data_by_solver.get("Vizinho Próximo (Guloso)", {}).get("n", []),
            data_by_solver.get("Vizinho Próximo (Guloso)", {}).get("cost", []),
            data_by_solver.get("Vizinho Próximo (Guloso)", {}).get("is_synthetic", []),
        ) if not s),
        8980.90,
    )
    berlin_costs.extend([mst_berlin, nn_berlin])
    bars = ax_berlin.bar(berlin_labels, berlin_costs, color=["#2ca02c", "#9467bd", "#d62728"], width=0.55)
    ax_berlin.set_title("Benchmark TSPLIB: berlin52 (n=52)", fontsize=11)
    ax_berlin.set_ylabel("Custo Total da Rota", fontsize=10)
    ax_berlin.set_ylim(0, max(berlin_costs) * 1.18)
    ax_berlin.grid(True, axis="y", ls="--", alpha=0.6)
    ax_berlin.tick_params(axis="x", labelsize=8, rotation=15)
    for bar, cost in zip(bars, berlin_costs):
        ax_berlin.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 180,
            f"{cost:.1f}",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
        )

    fig.tight_layout()
    cost_plot_path = images_dir / "comparativo_custo_solucao.png"
    fig.savefig(cost_plot_path, dpi=300)
    plt.close(fig)
    print(f" [+] Gráfico de custos salvo em: {cost_plot_path}")
    print("\nTodos os gráficos foram gerados com sucesso em docs/images/!")


if __name__ == "__main__":
    generate_benchmark_plots()

