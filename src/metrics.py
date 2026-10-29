"""Métricas de campanhas: contagens e razões ponderadas pelos jogos."""
import pandas as pd


def summarize_campaigns(df):
    games = float(df["played"].sum())
    return {
        "campaigns": len(df),
        "team_games": games,
        "utilization": 100 * float(df["points"].sum()) / (3 * games) if games > 0 else None,
        "goals_per_game": float(df["goals"].sum()) / games if games > 0 else None,
        "goal_difference_per_game": float(df["goals_diff"].sum()) / games if games > 0 else None,
    }


def grouped_metrics(df, by):
    grouped = df.groupby(by, as_index=False).agg(
        campaigns=("team", "size"), team_games=("played", "sum"),
        points=("points", "sum"), goals=("goals", "sum"), goals_diff=("goals_diff", "sum"),
    )
    denominator = grouped["team_games"].where(grouped["team_games"] > 0)
    grouped["utilization"] = 100 * grouped["points"] / (3 * denominator)
    grouped["goals_per_game"] = grouped["goals"] / denominator
    grouped["goal_difference_per_game"] = grouped["goals_diff"] / denominator
    return grouped


def select_campaigns(df, items):
    """Sem seleção usa a base; seleção explícita sem correspondência fica vazia."""
    clubs = [item["team"] for item in items if isinstance(item, dict) and "team" in item]
    return df[df["team"].isin(clubs)] if clubs else df


def season_series(df, seasons):
    grouped = grouped_metrics(df, "season").set_index("season")
    years = range(min(seasons), max(seasons) + 1) if seasons else []
    result = grouped.reindex(years).rename_axis("season").reset_index()
    # Cada lacuna inicia um novo segmento: a linha não inventa continuidade.
    result["segment"] = result["utilization"].isna().cumsum()
    return result


def format_metric(value, decimals=2, suffix=""):
    if value is None or pd.isna(value):
        return "—"
    rounded = round(float(value), decimals)
    if rounded == 0:
        rounded = 0.0
    return f"{rounded:.{decimals}f}".replace(".", ",") + suffix
