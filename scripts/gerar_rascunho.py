"""Gera o rascunho do Dashboard 1 com uma prévia dos dados reais.

Execute da raiz: .venv/Scripts/python.exe scripts/gerar_rascunho.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / "entregas"
df = pd.read_csv(ROOT / "data/clean/dataset.csv")
COLUNAS = ["points", "played", "won", "draw", "loss", "goals", "goals_taken", "goals_diff"]
ROTULOS = ["Pontos", "Jogos", "Vitórias", "Empates", "Derrotas", "Gols pró", "Gols contra", "Saldo"]
LARGURA, ALTURA = 1800, 1080
FUNDO, TEXTO, CINZA, BORDA = "#FFF9F2", "#272727", "#646464", "#DDD7CE"
LARANJA = "#E96812"

plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none"})
fig = plt.figure(figsize=(18, 10.8), dpi=100, facecolor=FUNDO)
canvas = fig.add_axes([0, 0, 1, 1], zorder=0)
canvas.set(xlim=(0, LARGURA), ylim=(ALTURA, 0))
canvas.axis("off")


def texto(x, y, valor, tamanho=12, cor=TEXTO, peso="normal", **kwargs):
    canvas.text(x, y, valor, fontsize=tamanho, color=cor, weight=peso,
                va="top", linespacing=1.5, **kwargs)


def caixa(x, y, largura, altura, fundo="white", borda=BORDA, raio=12):
    canvas.add_patch(FancyBboxPatch(
        (x, y), largura, altura, boxstyle=f"round,pad=0,rounding_size={raio}",
        facecolor=fundo, edgecolor=borda, linewidth=1.4,
    ))


def seletor(x, y, largura, valor):
    caixa(x, y, largura, 44, fundo="#FAFAF8", raio=6)
    texto(x + 12, y + 11, valor, 11)
    canvas.plot([x + largura - 27, x + largura - 21, x + largura - 15],
                [y + 19, y + 25, y + 19], color=CINZA, lw=1.5)


def intervalo(y, rotulo, coluna):
    texto(64, y, rotulo, 11, peso="bold")
    texto(64, y + 26, str(int(df[coluna].min())), 10, CINZA)
    texto(354, y + 26, str(int(df[coluna].max())), 10, CINZA, ha="right")
    canvas.plot([74, 344], [y + 58, y + 58], color=LARANJA, lw=3)
    for x in (74, 344):
        canvas.add_patch(Circle((x, y + 58), 6, color=LARANJA))


texto(40, 29, "AULA 21  /  RASCUNHO DO DASHBOARD 1", 11, LARANJA, "bold")
texto(40, 63, "Brasileirão: correlação e distribuição", 26, peso="bold")
texto(40, 114, "Como vitórias, gols e saldo se relacionam com os pontos de uma campanha?", 14, CINZA)
texto(1760, 35, "PROTÓTIPO ESTÁTICO", 10, CINZA, ha="right")

caixa(40, 175, 340, 710, fundo="#FFF4E8", borda=LARANJA, raio=20)
caixa(400, 175, 530, 710, borda=LARANJA, raio=20)
caixa(950, 175, 810, 710, borda=LARANJA, raio=20)

texto(64, 199, "01  Filtros", 18, peso="bold")
texto(64, 237, "Aplicados aos dois gráficos", 10, CINZA)
texto(64, 273, "Temporadas", 12, peso="bold")
seletor(64, 300, 292, f"Todas · {df.season.min()}–{df.season.max()}")
texto(64, 365, "Clubes", 12, peso="bold")
seletor(64, 392, 292, "Todos os clubes")
texto(64, 453, "Variáveis quantitativas", 12, peso="bold")
caixa(64, 481, 292, 98, fundo="#FAFAF8", raio=6)
texto(76, 491, "Pontos · Jogos · Vitórias · Empates\nDerrotas · Gols marcados\nGols sofridos · Saldo de gols", 10)
texto(64, 589, "Seleção múltipla · 8 selecionadas", 9, CINZA)
caixa(64, 624, 36, 20, fundo="#D2D2CF", borda="#D2D2CF", raio=10)
canvas.add_patch(Circle((74, 634), 7, color="white"))
texto(110, 623, "Distinguir por saldo de gols", 10)
intervalo(671, "Intervalo de pontos", "points")
intervalo(757, "Intervalo de saldo de gols", "goals_diff")
texto(64, 851, "Mais intervalos na rolagem da sidebar.", 9, CINZA)

texto(424, 199, "02  Correlação", 18, peso="bold")
texto(424, 237, "Heatmap · coeficiente de Spearman", 11, CINZA)
texto(424, 285, f"{len(df)} de {len(df)} campanhas selecionadas", 11)
corr = df[COLUNAS].corr(method="spearman")
ax = fig.add_axes([504 / LARGURA, 1 - 714 / ALTURA, 390 / LARGURA, 390 / ALTURA])
im = ax.imshow(corr, vmin=-1, vmax=1, cmap="RdBu_r")
ax.set_xticks(range(8), ROTULOS, rotation=45, ha="right", fontsize=9)
ax.set_yticks(range(8), ROTULOS, fontsize=9)
ax.tick_params(length=0, pad=6)
for i in range(8):
    for j in range(8):
        valor = corr.iloc[i, j]
        ax.text(j, i, f"{valor:.2f}", ha="center", va="center", fontsize=8,
                color="white" if abs(valor) > .6 else TEXTO)
for spine in ax.spines.values():
    spine.set_visible(False)
cax = fig.add_axes([504 / LARGURA, 1 - 812 / ALTURA, 390 / LARGURA, 12 / ALTURA])
fig.colorbar(im, cax=cax, orientation="horizontal", ticks=[-1, 0, 1])
cax.tick_params(labelsize=9)
texto(424, 850, "Associação não implica causalidade.", 10, CINZA)

texto(974, 199, "03  Distribuição", 18, peso="bold")
texto(974, 237, "Histograma · frequência de campanhas", 11, CINZA)
texto(974, 273, "Variável da distribuição", 12, peso="bold")
seletor(974, 300, 410, "Pontos")
ax_hist = fig.add_axes([1040 / LARGURA, 1 - 737 / ALTURA, 675 / LARGURA, 345 / ALTURA])
ax_hist.hist(df["points"], bins=15, color="#777777", edgecolor="white", linewidth=1)
ax_hist.set_xlabel("Pontos na temporada", fontsize=11, labelpad=12)
ax_hist.set_ylabel("Quantidade de campanhas", fontsize=11, labelpad=12)
ax_hist.set_axisbelow(True)
ax_hist.grid(axis="y", color="#E9E9E9")
ax_hist.spines[["top", "right"]].set_visible(False)
ax_hist.spines[["left", "bottom"]].set_color(BORDA)
ax_hist.tick_params(labelsize=10)
texto(974, 806, "Ao ativar a distinção por saldo:", 11, peso="bold")
canvas.add_patch(Circle((982, 850), 6, color="#2A9D8F"))
texto(997, 840, "Saldo positivo (> 0)", 10)
canvas.add_patch(Circle((1280, 850), 6, color="#E76F51"))
texto(1295, 840, "Saldo não positivo (≤ 0)", 10)

texto(40, 920, "LEITURA DO PROTÓTIPO", 10, LARANJA, "bold")
texto(40, 950, "1. Escolha temporadas, clubes e intervalos.\n2. Compare a correlação e a distribuição no mesmo recorte.", 11)
texto(790, 950, "Gráficos calculados com o CSV tratado do projeto.\nUma linha = um clube em uma temporada; o recorte inicial inclui todas as campanhas.", 11)
texto(40, 1035, "Estrutura baseada no slide 16 da Aula 21 e em prompts/prof_rascunho_dashboard1.png.", 10, CINZA)
texto(1760, 1035, "Rascunho documentado em 22/10/2026", 10, CINZA, ha="right")

if __name__ == "__main__":
    DESTINO.mkdir(exist_ok=True)
    for extensao in ("png", "svg"):
        arquivo = DESTINO / f"rascunho-dashboard1.{extensao}"
        fig.savefig(arquivo, facecolor=FUNDO, dpi=150)
        if extensao == "svg":
            linhas = arquivo.read_text(encoding="utf-8").splitlines()
            arquivo.write_text("\n".join(linha.rstrip() for linha in linhas) + "\n", encoding="utf-8")
        print(arquivo)
    plt.close(fig)
