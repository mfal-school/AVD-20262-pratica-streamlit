"""Desenha o planejamento do Dashboard 2 definido antes de sua implementação."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BG, GREEN, INK, BORDER = "#F7F8F2", "#176B4D", "#172C26", "#D8E1D5"


def main():
    df = pd.read_csv(ROOT / "data/clean/dataset.csv")
    fig, ax = plt.subplots(figsize=(18, 11), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set(xlim=(0, 1800), ylim=(1100, 0))
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    def box(x, y, w, h, color="white"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=12", facecolor=color, edgecolor=BORDER))

    def text(x, y, value, size=12, color=INK, weight="normal"):
        ax.text(x, y, value, va="top", fontsize=size, color=color, weight=weight, linespacing=1.6)

    text(40, 25, "AULA 22 · PLANEJAMENTO DO DASHBOARD 2 · 27/10/2026", 12, GREEN, "bold")
    text(40, 62, "Brasileirão em números", 28, weight="bold")
    text(40, 115, "Uma campanha = um clube em uma temporada. Indicadores definidos antes do desenho.", 13)
    box(40, 165, 300, 835, "#EDF1E7")
    text(62, 190, "Filtros comuns", 18, weight="bold")
    text(62, 240, "Temporadas", weight="bold")
    box(62, 275, 255, 70)
    text(78, 290, "2003 a 2024\nTodas selecionadas", 12)
    text(62, 380, "Clubes", weight="bold")
    box(62, 415, 255, 50)
    text(78, 430, "Todos os clubes  ▾", 12)
    text(62, 500, "Afetam as duas abas.", 11, GREEN)
    box(62, 570, 255, 180, "#F7F8F2")
    text(78, 590, "Dashboard 1  ▸", 13, weight="bold")
    text(78, 635, "Variáveis e intervalos\nficam agrupados aqui.\nNão alteram os KPIs.", 11)
    text(62, 870, "Fonte: Kaggle / EDA\n450 campanhas · 44 clubes", 11)

    text(380, 177, "Dashboard 1 · Exploração", 13)
    text(835, 177, "Dashboard 2 · Desempenho", 13, GREEN, "bold")
    ax.plot([835, 1195], [212, 212], color=GREEN, lw=3)
    box(380, 240, 1380, 82)
    text(400, 258, "○  Somente campanhas com 38 jogos", 12)
    text(1000, 258, "Clubes no ranking: 12  ──●────", 12)
    total_games = df.played.sum()
    values = [str(len(df)), f"{100 * df.points.sum() / (3 * total_games):.1f}%", f"{df.goals.sum() / total_games:.2f}", "0,00"]
    labels = ["Campanhas", "Aproveitamento", "Gols por jogo", "Saldo por jogo"]
    for i, (label, value) in enumerate(zip(labels, values)):
        x = 380 + i * 350
        box(x, 350, 330, 130)
        text(x+18, 368, label, 12)
        text(x+18, 408, value.replace(".", ","), 26, GREEN, "bold")
    text(380, 505, "Seleção: todos os clubes do recorte", 12, GREEN)
    text(1340, 505, "[ Limpar seleção do gráfico ]", 11)
    box(380, 550, 640, 375)
    box(1040, 550, 720, 375)
    text(400, 568, "Comparar clubes", 17, weight="bold")
    text(400, 603, "Aproveitamento · clique / Shift + clique", 10)
    ranking = df.groupby("team")[["points", "played"]].sum()
    ranking["rate"] = ranking.points / (3 * ranking.played) * 100
    ranking = ranking.sort_values("rate", ascending=False).head(6)
    for i, (club, row) in enumerate(ranking.iterrows()):
        y = 650 + i * 37
        text(400, y, club, 11)
        ax.barh(y+10, row.rate*5, left=575, height=20, color=GREEN if i == 0 else "#ADC6B5")
    text(1060, 568, "Evolução por temporada", 17, weight="bold")
    text(1060, 603, "Aproveitamento (%) · dos clubes selecionados", 10)
    ax.plot([1100, 1695], [855, 855], color=BORDER)
    ax.plot([1100, 1100], [655, 855], color=BORDER)
    ax.plot([1120, 1220, 1320, 1420, 1520, 1680], [780, 730, 760, 695, 720, 670], color=GREEN, marker="o", lw=2)
    text(1100, 870, "2003                  temporada                  2024", 10)
    text(1060, 915, "Traçado ilustrativo: o app calculará os valores reais.", 9)
    text(380, 950, "▸ Ver campanhas selecionadas", 12, weight="bold")
    text(380, 1005, "Fluxo: widgets → seleção no ranking → KPIs + evolução + tabela. Duplo clique ou botão limpa a seleção.", 11)
    text(380, 1045, "O limite de barras não limita os KPIs. Taxas = razão das somas, ponderadas pelos jogos.", 10)
    target = ROOT / "entregas/rascunho-dashboard2.png"
    target.parent.mkdir(exist_ok=True)
    fig.savefig(target, facecolor=BG)
    plt.close(fig)
    print(target)


if __name__ == "__main__":
    main()
