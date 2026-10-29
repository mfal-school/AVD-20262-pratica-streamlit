from hashlib import sha256
import json

import pandas as pd
import plotly.express as px
import streamlit as st

from src.charts import club_ranking, utilization_timeline
from src.data_loader import load_data
from src.metrics import (
    format_metric, grouped_metrics, season_series, select_campaigns, summarize_campaigns,
)

# Rascunhos em entregas/; métricas e widgets planejados em justificativa-metricas.md.
st.set_page_config(page_title="Brasileirão em números", layout="wide")
st.title("Brasileirão em números")
st.caption("Explore relações e compare desempenho. Uma campanha representa um clube em uma temporada.")

df = load_data()
VARS_QUANT = ["points", "played", "won", "draw", "loss", "goals", "goals_taken", "goals_diff"]
ROTULOS = {
    "points": "Pontos", "played": "Jogos disputados", "won": "Vitórias",
    "draw": "Empates", "loss": "Derrotas", "goals": "Gols marcados",
    "goals_taken": "Gols sofridos", "goals_diff": "Saldo de gols",
    "saldo_resultado": "Resultado do saldo", "team": "Clube", "season": "Temporada",
}


@st.cache_data(ttl=300, max_entries=64, show_spinner=False)
def spearman_matrix(data, variables):
    return data[list(variables)].corr(method="spearman")


# Filtros comuns às duas abas; os intervalos do D1 são aplicados separadamente.
with st.sidebar:
    st.header("Filtros comuns")
    st.caption("Temporadas e clubes afetam as duas abas.")
    temporadas = st.multiselect(
        "Temporadas", options=sorted(df["season"].unique()),
        default=sorted(df["season"].unique()), key="temporadas",
    )
    times = st.multiselect(
        "Clubes", options=sorted(df["team"].unique()), key="clubes",
        help="Deixe vazio para mostrar todos os clubes.", placeholder="Todos os clubes",
    )
    with st.expander("Dashboard 1 · variáveis e intervalos", expanded=True):
        st.caption("Estes controles afetam somente o Dashboard 1.")
        variaveis = st.multiselect(
            "Variáveis quantitativas", options=VARS_QUANT, default=VARS_QUANT,
            format_func=lambda var: ROTULOS[var], key="variaveis",
        )
        separar_por_classe = st.toggle(
            "Distinguir por saldo de gols", value=False, key="separar_por_saldo",
            help="Compara saldo positivo com saldo zero ou negativo.",
        )
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
                f"Intervalo de {ROTULOS[var]}", min_value=minimo, max_value=maximo,
                value=(minimo, maximo), step=passo, key=f"intervalo_{var}",
            )
    st.caption("Fonte: EDA do Brasileirão · Kaggle, versão 19.")

df_base = df[df["season"].isin(temporadas)]
if times:
    df_base = df_base[df_base["team"].isin(times)]

tab_exploracao, tab_desempenho = st.tabs(["Dashboard 1 · Exploração", "Dashboard 2 · Desempenho"])

with tab_exploracao:
    df_filtrado = df_base
    for var, (inicio, fim) in intervalos.items():
        df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]
    st.caption(f"{len(df_filtrado)} de {len(df)} campanhas nos filtros escolhidos.")
    if df_filtrado.empty:
        st.warning("Nenhuma campanha encontrada. Ajuste os filtros para visualizar os dados.")
    else:
        # Layout do rascunho do D1: correlação à esquerda, distribuição à direita.
        col_correlacao, col_distribuicao = st.columns([1, 1.5])
        with col_correlacao:
            st.subheader("Correlação")
            if len(variaveis) < 2:
                st.info("Selecione pelo menos 2 variáveis para calcular a correlação.")
            elif len(df_filtrado) < 2:
                st.info("São necessárias pelo menos 2 campanhas para calcular a correlação.")
            else:
                correlacao = spearman_matrix(df_filtrado, tuple(variaveis))
                constantes = [ROTULOS[v] for v in variaveis if df_filtrado[v].nunique() < 2]
                if constantes:
                    st.info("Coeficiente indefinido para variáveis constantes: " + ", ".join(constantes) + ".")
                if correlacao.notna().any().any():
                    fig = px.imshow(
                        correlacao.rename(index=ROTULOS, columns=ROTULOS),
                        text_auto=".2f", zmin=-1, zmax=1, color_continuous_scale="RdBu_r",
                        aspect="auto", labels={"color": "Spearman"},
                    )
                    st.plotly_chart(fig, width="stretch", key="d1_correlacao",
                                    alt="Matriz de correlação de Spearman das variáveis selecionadas.")
                st.caption("Spearman, como na EDA. Associação não implica causalidade.")
        with col_distribuicao:
            st.subheader("Distribuição")
            if variaveis:
                # Remove uma escolha antiga se ela saiu da lista de variáveis.
                if st.session_state.get("d1_distribuicao") not in variaveis:
                    st.session_state["d1_distribuicao"] = variaveis[0]
                variavel = st.selectbox(
                    "Variável da distribuição", options=variaveis,
                    format_func=lambda var: ROTULOS[var], key="d1_distribuicao",
                )
                fig = px.histogram(
                    df_filtrado, x=variavel,
                    color="saldo_resultado" if separar_por_classe else None,
                    barmode="overlay", opacity=0.8, labels=ROTULOS,
                    color_discrete_sequence=["#176B4D"],
                    color_discrete_map={"Saldo positivo": "#176B4D", "Saldo não positivo": "#C98618"},
                )
                fig.update_yaxes(title="Quantidade de campanhas")
                st.plotly_chart(fig, width="stretch", key="d1_histograma",
                                alt=f"Distribuição de {ROTULOS[variavel]} nas campanhas filtradas.")
            else:
                st.info("Selecione uma variável para visualizar a distribuição.")

with tab_desempenho:
    st.subheader("Desempenho dos clubes")
    st.caption("Taxas ponderadas pelos jogos. Os intervalos de variáveis do Dashboard 1 não alteram estes indicadores.")
    controles = st.columns([1, 1])
    with controles[0]:
        somente_38 = st.toggle("Somente campanhas com 38 jogos", key="d2_somente_38")
    with controles[1]:
        limite = st.slider("Clubes no ranking", 1, int(df["team"].nunique()), 12, key="d2_limite")

    base_kpis = df_base[df_base["played"] == 38] if somente_38 else df_base
    # Reservas mantêm os KPIs acima dos gráficos, mesmo lendo a seleção depois.
    indicadores = st.container()
    contexto = st.container()
    st.session_state.setdefault("d2_selecao_versao", 0)
    if st.button("Limpar seleção do gráfico", key="d2_limpar"):
        st.session_state["d2_selecao_versao"] += 1

    selecionado = base_kpis
    itens = []
    if not base_kpis.empty:
        ranking = grouped_metrics(base_kpis, "team").sort_values(
            ["utilization", "team"], ascending=[False, True], na_position="last",
        ).head(limite)
        # Um novo contexto limpa seleções antigas sem escrever no estado read-only do gráfico.
        assinatura = json.dumps([
            sorted(int(t) for t in temporadas), sorted(times), somente_38,
            limite, st.session_state["d2_selecao_versao"],
        ], ensure_ascii=True)
        chave_ranking = "d2_ranking_" + sha256(assinatura.encode()).hexdigest()[:16]
        col_ranking, col_evolucao = st.columns([1, 1.25])
        with col_ranking:
            st.subheader("Comparar clubes")
            st.caption("Clique em uma barra; Shift + clique inclui outros clubes. Duplo clique limpa.")
            evento = st.altair_chart(
                club_ranking(ranking), width="stretch", key=chave_ranking,
                on_select="rerun", selection_mode="clubes_selecionados",
                alt="Ranking de aproveitamento por clube. Selecione barras para filtrar os indicadores e a evolução.",
            )
            itens = evento.selection.get("clubes_selecionados", [])
            selecionado = select_campaigns(base_kpis, itens)
            st.caption(f"Exibindo {len(ranking)} de {base_kpis['team'].nunique()} clubes. O limite de barras não restringe os KPIs.")
        with col_evolucao:
            st.subheader("Evolução por temporada")
            st.caption("Aproveitamento agregado dos clubes selecionados em cada temporada.")
            if not selecionado.empty:
                st.altair_chart(
                    utilization_timeline(season_series(selecionado, temporadas)),
                    width="stretch", key="d2_evolucao",
                    alt="Evolução do aproveitamento dos clubes selecionados, por temporada, com lacunas nos anos sem campanhas.",
                )

    resumo = summarize_campaigns(selecionado)
    with indicadores:
        cards = st.columns(4)
        cards[0].metric("Campanhas", resumo["campaigns"], border=True,
                        help="Número de combinações clube-temporada no recorte selecionado.")
        cards[1].metric("Aproveitamento", format_metric(resumo["utilization"], 1, "%"), border=True,
                        help="100 × soma dos pontos / (3 × soma dos jogos disputados). Usa os pontos oficiais.")
        cards[2].metric("Gols por jogo", format_metric(resumo["goals_per_game"]), border=True,
                        help="Soma dos gols marcados / soma dos jogos dos clubes. Não é o total de gols da partida.")
        cards[3].metric("Saldo por jogo", format_metric(resumo["goal_difference_per_game"]), border=True,
                        help="Soma dos saldos de gols / soma dos jogos dos clubes. Pode ser negativo.")
    with contexto:
        if selecionado.empty:
            st.warning("Nenhuma campanha para os KPIs. Ajuste os filtros ou limpe a seleção do gráfico.")
        else:
            nomes = ", ".join(item["team"] for item in itens) if itens else "todos os clubes do recorte"
            st.caption(f"Seleção: {nomes} · {len(selecionado)} campanhas · {selecionado['team'].nunique()} clubes.")

    if not selecionado.empty:
        with st.expander("Ver campanhas selecionadas"):
            st.dataframe(
                selecionado[["season", "team", "points", "played", "goals", "goals_diff"]]
                .sort_values(["season", "team"]).rename(columns=ROTULOS),
                hide_index=True, width="stretch", alt="Campanhas utilizadas nos indicadores do Dashboard 2.",
            )
    st.caption("Cada jogo pode aparecer para os dois clubes. As taxas usam jogos de clubes, não partidas únicas do campeonato.")
