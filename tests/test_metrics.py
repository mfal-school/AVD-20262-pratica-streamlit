import unittest
from unittest.mock import patch

import pandas as pd

from src.data_loader import load_data
from src.metrics import format_metric, grouped_metrics, season_series, select_campaigns, summarize_campaigns


class MetricsTests(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            "team": ["A", "B"], "season": [2020, 2022],
            "played": [1, 3], "points": [3, 0], "goals": [1, 3], "goals_diff": [1, -3],
        })

    def test_rates_weight_games_instead_of_averaging_percentages(self):
        result = summarize_campaigns(self.data)
        self.assertEqual(result["campaigns"], 2)
        self.assertEqual(result["utilization"], 25)  # Média simples daria 50%.
        self.assertEqual(result["goals_per_game"], 1)
        self.assertEqual(result["goal_difference_per_game"], -0.5)
        same_club = self.data.assign(team="A")
        self.assertEqual(grouped_metrics(same_club, "team").iloc[0].utilization, 25)

    def test_empty_and_zero_denominators_are_undefined(self):
        for frame in [self.data.iloc[:0], self.data.assign(played=0)]:
            result = summarize_campaigns(frame)
            self.assertIsNone(result["utilization"])
            self.assertIsNone(result["goals_per_game"])
            self.assertEqual(format_metric(result["utilization"]), "—")
        self.assertEqual(format_metric(-0.0003), "0,00")

    def test_selection_empty_single_multiple_and_no_matches(self):
        self.assertEqual(len(select_campaigns(self.data, [])), 2)
        self.assertEqual(select_campaigns(self.data, [{"team": "A"}]).team.tolist(), ["A"])
        self.assertEqual(len(select_campaigns(self.data, [{"team": "A"}, {"team": "B"}])), 2)
        self.assertTrue(select_campaigns(self.data, [{"team": "missing"}]).empty)

    def test_missing_seasons_break_the_line(self):
        series = season_series(self.data, [2020, 2022])
        self.assertEqual(series.season.tolist(), [2020, 2021, 2022])
        self.assertTrue(pd.isna(series.loc[1, "utilization"]))
        self.assertNotEqual(series.loc[0, "segment"], series.loc[2, "segment"])

    def test_cache_avoids_rereads_and_returns_independent_data(self):
        load_data.clear()
        with patch("src.data_loader.pd.read_csv", wraps=pd.read_csv) as reader:
            first = load_data()
            original = first.iloc[0].points
            first.loc[0, "points"] = -999
            second = load_data()
            self.assertEqual(reader.call_count, 1)
            self.assertEqual(second.iloc[0].points, original)
        load_data.clear()


if __name__ == "__main__":
    unittest.main()
