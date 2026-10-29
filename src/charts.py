"""Visuais Altair do Dashboard 2, conforme o rascunho planejado."""
import altair as alt

GREEN = "#176B4D"


def club_ranking(data):
    selection = alt.selection_point(
        name="clubes_selecionados", fields=["team"],
        toggle="event.shiftKey", clear="dblclick",
    )
    return (
        alt.Chart(data)
        .mark_bar(color=GREEN, cornerRadiusEnd=3)
        .encode(
            x=alt.X("utilization:Q", title="Aproveitamento (%)", scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("team:N", title=None, sort=data["team"].tolist()),
            opacity=alt.when(selection).then(alt.value(1)).otherwise(alt.value(0.25)),
            tooltip=[
                alt.Tooltip("team:N", title="Clube"),
                alt.Tooltip("utilization:Q", title="Aproveitamento (%)", format=".1f"),
                alt.Tooltip("campaigns:Q", title="Campanhas", format="d"),
                alt.Tooltip("team_games:Q", title="Jogos do clube", format="d"),
            ],
        )
        .add_params(selection)
        .properties(height=max(320, len(data) * 25))
    )


def utilization_timeline(data):
    return (
        alt.Chart(data)
        .mark_line(color=GREEN, point=True, strokeWidth=2.5)
        .encode(
            x=alt.X("season:Q", title="Temporada", scale=alt.Scale(zero=False), axis=alt.Axis(format="d", tickMinStep=1)),
            y=alt.Y("utilization:Q", title="Aproveitamento (%)", scale=alt.Scale(domain=[0, 100])),
            detail="segment:N",
            tooltip=[
                alt.Tooltip("season:Q", title="Temporada", format="d"),
                alt.Tooltip("utilization:Q", title="Aproveitamento (%)", format=".1f"),
                alt.Tooltip("campaigns:Q", title="Campanhas", format="d"),
            ],
        )
        .properties(height=320)
    )
