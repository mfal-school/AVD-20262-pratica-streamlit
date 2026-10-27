import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_data

# Esqueleto revisado com prompts/layout-skeleton-prompt.md em 27/10/2026.
# Referência visual: entregas/rascunho-dashboard1.png.
# Bloco 1 — cabeçalho do rascunho e carregamento do CSV já tratado.
st.set_page_config(
    page_title="Análise do Brasileirão — Correlação e Distribuição",
    layout="wide",
)

st.title("Análise do Brasileirão — Correlação e Distribuição")
st.caption("Dados da sua EDA no Colab. Cada registro representa um clube em uma temporada.")

df = load_data()

# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = ["points", "played", "won", "draw", "loss", "goals", "goals_taken", "goals_diff"]
ROTULOS = {
    "points": "Pontos", "played": "Jogos disputados", "won": "Vitórias",
    "draw": "Empates", "loss": "Derrotas", "goals": "Gols marcados",
    "goals_taken": "Gols sofridos", "goals_diff": "Saldo de gols",
    "saldo_resultado": "Resultado do saldo",
}

# Bloco 2 — sidebar do rascunho: filtros de campanhas, variáveis e intervalos.
with st.sidebar:
    st.header("Filtros")

    temporadas = st.multiselect(
        "Temporadas", options=sorted(df["season"].unique()),
        default=sorted(df["season"].unique()),
        key="temporadas",
    )
    times = st.multiselect(
        "Clubes", options=sorted(df["team"].unique()),
        help="Deixe vazio para mostrar todos os clubes.",
        key="clubes",
    )

    variaveis = st.multiselect(
        "Variáveis quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
        format_func=lambda var: ROTULOS[var],
        help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
        key="variaveis",
    )

    separar_por_classe = st.toggle(
        "Distinguir por saldo de gols",
        value=False,
        help="Compara campanhas com saldo positivo e saldo não positivo (zero ou negativo).",
        key="separar_por_saldo",
    )

    # Um slider de intervalo para cada variável selecionada
    intervalos = {}
    for var in variaveis:
        if pd.api.types.is_integer_dtype(df[var]):
            minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
        else:
            minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1
        if minimo == maximo:
            st.caption(f"{ROTULOS[var]}: {minimo} em todos os registros.")
            continue
        intervalos[var] = st.slider(
            f"Intervalo de {ROTULOS[var]}",
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            key=f"intervalo_{var}",
        )

# Bloco 3 — aplica o mesmo recorte aos dois gráficos do rascunho.
df_filtrado = df[df["season"].isin(temporadas)]
if times:
    df_filtrado = df_filtrado[df_filtrado["team"].isin(times)]
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

st.caption(f"{len(df_filtrado)} de {len(df)} campanhas nos filtros escolhidos.")
if df_filtrado.empty:
    st.warning("Nenhuma campanha encontrada. Ajuste os filtros para visualizar os dados.")
    st.stop()

# Blocos 4 e 5 — correlação à esquerda e distribuição na coluna maior à direita.
col_correlacao, col_distribuicao = st.columns([1, 1.5])

# Bloco 4 — heatmap de Spearman das variáveis e campanhas selecionadas.
with col_correlacao:
    st.subheader("Correlação")

    if len(variaveis) < 2:
        st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
    elif len(df_filtrado) < 2:
        st.warning("São necessárias pelo menos 2 campanhas para calcular a correlação.")
    else:
        correlacao = df_filtrado[variaveis].corr(method="spearman")
        fig = px.imshow(
            correlacao.rename(index=ROTULOS, columns=ROTULOS),
            text_auto=".2f", zmin=-1, zmax=1,
            color_continuous_scale="RdBu_r", aspect="auto",
            labels={"color": "Spearman"},
        )
        st.plotly_chart(fig, width="stretch")
        st.caption("Correlação de Spearman, como na EDA. Variáveis constantes não têm correlação definida.")

# Bloco 5 — seletor da variável e histograma; o toggle separa os saldos.
with col_distribuicao:
    st.subheader("Distribuição")

    if variaveis:
        variavel = st.selectbox(
            "Variável da distribuição", options=variaveis,
            format_func=lambda var: ROTULOS[var],
        )
        fig = px.histogram(
            df_filtrado, x=variavel,
            color="saldo_resultado" if separar_por_classe else None,
            barmode="overlay", opacity=0.75, labels=ROTULOS,
            color_discrete_map={
                "Saldo positivo": "#2A9D8F", "Saldo não positivo": "#E76F51",
            },
        )
        fig.update_yaxes(title="Quantidade de campanhas")
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Selecione uma variável para visualizar a distribuição.")

# TODO: Dashboard 2 — KPIs (Aula 22)
