import base64
import json
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def array(value):
    if isinstance(value, dict) and "bdata" in value:
        result = np.frombuffer(base64.b64decode(value["bdata"]), dtype=value["dtype"])
        if "shape" in value:
            result = result.reshape(tuple(int(n) for n in value["shape"].split(",")))
        return result
    return np.asarray(value)


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
        self.assert_ok()

    def assert_ok(self):
        self.assertFalse(self.at.exception, [item.message for item in self.at.exception])

    def test_initial_tabs_charts_and_metrics(self):
        self.assertEqual(len(self.at.tabs), 2)
        self.assertEqual(len(self.at.get("plotly_chart")), 2)
        self.assertEqual(len(self.at.get("vega_lite_chart")), 2)
        self.assertEqual([m.value for m in self.at.metric], ["450", "45,5%", "1,28", "0,00"])

    def test_zero_one_two_and_more_variables(self):
        for variables, charts in [([], 0), (["points"], 1), (["points", "won"], 2), (["points", "won", "goals"], 2)]:
            with self.subTest(variables=variables):
                self.at.multiselect(key="variaveis").set_value(variables).run()
                self.assert_ok()
                self.assertEqual(len(self.at.get("plotly_chart")), charts)
                self.assertEqual(self.at.metric[0].value, "450")

    def test_filter_combinations_recalculate_data_and_correlation(self):
        self.at.multiselect(key="variaveis").set_value(["points", "won"]).run()
        self.at.slider(key="intervalo_points").set_value((40, 60)).run()
        self.at.multiselect(key="temporadas").set_value([2024]).run()
        self.assert_ok()
        df = pd.read_csv(ROOT / "data/clean/dataset.csv")
        expected = df[(df.season == 2024) & df.points.between(40, 60)]
        plots = self.at.get("plotly_chart")
        heatmap = json.loads(plots[0].proto.spec)["data"][0]
        histogram = json.loads(plots[1].proto.spec)["data"][0]
        self.assertAlmostEqual(array(heatmap["z"])[0, 1], spearmanr(expected.points, expected.won).statistic)
        np.testing.assert_array_equal(array(histogram["x"]), expected.points.to_numpy())
        self.assertEqual(len(expected), 12)
        self.assertEqual(self.at.metric[0].value, "20")  # Sliders do D1 não filtram D2.

    def test_histogram_selection_class_toggle_and_removed_variable(self):
        self.at.selectbox(key="d1_distribuicao").select("goals").run()
        self.at.toggle(key="separar_por_saldo").set_value(True).run()
        self.assert_ok()
        traces = json.loads(self.at.get("plotly_chart")[1].proto.spec)["data"]
        self.assertEqual(len(traces), 2)
        self.assertEqual(sum(len(array(trace["x"])) for trace in traces), 450)
        self.at.multiselect(key="variaveis").set_value(["points", "won"]).run()
        self.assert_ok()
        self.assertEqual(self.at.selectbox(key="d1_distribuicao").value, "points")

    def test_single_campaign_and_constant_variable(self):
        self.at.multiselect(key="temporadas").set_value([2022]).run()
        self.at.multiselect(key="variaveis").set_value(["played", "points"]).run()
        self.assert_ok()
        self.assertTrue(any("constantes" in item.value for item in self.at.info))
        self.at.multiselect(key="clubes").set_value(["Flamengo"]).run()
        self.assert_ok()
        self.assertEqual(len(self.at.get("plotly_chart")), 1)
        self.assertEqual(self.at.metric[0].value, "1")

    def test_empty_period_keeps_both_tabs_and_undefined_kpis(self):
        self.at.multiselect(key="temporadas").set_value([]).run()
        self.assert_ok()
        self.assertEqual(len(self.at.tabs), 2)
        self.assertEqual([m.value for m in self.at.metric], ["0", "—", "—", "—"])
        self.assertEqual(len(self.at.get("plotly_chart")), 0)
        self.assertEqual(len(self.at.get("vega_lite_chart")), 0)

    def test_empty_d1_intervals_do_not_stop_d2(self):
        self.at.multiselect(key="variaveis").set_value(["points", "won"]).run()
        self.at.slider(key="intervalo_points").set_value((100, 100)).run()
        self.at.slider(key="intervalo_won").set_value((1, 1)).run()
        self.assert_ok()
        self.assertEqual(len(self.at.get("plotly_chart")), 0)
        self.assertEqual(self.at.metric[0].value, "450")

    def test_d2_38_games_filter_and_ranking_limit(self):
        self.at.slider(key="d2_limite").set_value(1).run()
        self.assert_ok()
        self.assertEqual(self.at.metric[0].value, "450")
        self.at.toggle(key="d2_somente_38").set_value(True).run()
        self.assert_ok()
        self.assertEqual(self.at.metric[0].value, "378")
        self.at.multiselect(key="temporadas").set_value([2003]).run()
        self.assert_ok()
        self.assertEqual([m.value for m in self.at.metric], ["0", "—", "—", "—"])
        self.assertEqual(len(self.at.get("plotly_chart")), 2)


if __name__ == "__main__":
    unittest.main()
