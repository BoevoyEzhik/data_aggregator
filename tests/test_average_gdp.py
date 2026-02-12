import pytest

from src.reports.average_gdp import AverageGdpReport


class TestAverageGdpReport:
    def test_generate_single_country_valid_gdp(self):
        data = {
            "Germany": [
                {"year": 2020, "gdp": 100.0, "gdp_growth": 0.8, "inflation": 1.5, "unemployment": 3.2,
                 "population": 83000000, "continent": "Europe"},
                {"year": 2021, "gdp": 200.0, "gdp_growth": 2.9, "inflation": 3.1, "unemployment": 3.1,
                 "population": 83200000, "continent": "Europe"}
            ]
        }

        report = AverageGdpReport()
        result = report.generate(data)

        assert len(result) == 1
        assert result[0]["country"] == "Germany"
        expected_avg = (100.0 + 200.0) / 2
        assert result[0]["avg_gdp"] == round(expected_avg, 2)

    def test_generate_multiple_countries(self):
        data = {
            "Germany": [
                {"year": 2020, "gdp": 400.0},
                {"year": 2021, "gdp": 420.0}
            ],
            "France": [
                {"year": 2020, "gdp": 250.0},
                {"year": 2021, "gdp": 270.0}
            ],
            "Italy": [
                {"year": 2020, "gdp": 200.0},
                {"year": 2021, "gdp": 210.0}
            ]
        }

        report = AverageGdpReport()
        result = report.generate(data)

        assert len(result) == 3
        countries = [r["country"] for r in result]
        assert countries == ["Germany", "France", "Italy"]

        assert result[0]["avg_gdp"] == pytest.approx(410.0, abs=0.01)
        assert result[1]["avg_gdp"] == pytest.approx(260.0, abs=0.01)
        assert result[2]["avg_gdp"] == pytest.approx(205.0, abs=0.01)

    def test_generate_no_data_for_any_country(self):
        report = AverageGdpReport()
        result = report.generate({})
        assert result == []

    def test_generate_country_with_no_gdp_values(self):
        data = {
            "Japan": [
                {"year": 2020, "gdp": None},
                {"year": 2021, "gdp": None}
            ]
        }

        report = AverageGdpReport()
        result = report.generate(data)

        assert result == []

    def test_generate_mixed_valid_and_none_gdp(self):
        data = {
            "Canada": [
                {"year": 2020, "gdp": None},
                {"year": 2021, "gdp": 170.0},
                {"year": 2022, "gdp": 180.0}
            ]
        }

        report = AverageGdpReport()
        result = report.generate(data)

        assert len(result) == 1
        avg = (170.0 + 180.0) / 2
        assert result[0]["avg_gdp"] == round(avg, 2)

    def test_generate_one_year_per_country(self):
        data = {
            "USA": [{"year": 2020, "gdp": 2100.0}],
            "China": [{"year": 2020, "gdp": 1500.0}]
        }

        report = AverageGdpReport()
        result = report.generate(data)

        assert len(result) == 2
        assert result[0]["country"] == "USA"
        assert result[0]["avg_gdp"] == 2100.0
        assert result[1]["country"] == "China"
        assert result[1]["avg_gdp"] == 1500.0

    def test_generate_includes_only_country_and_avg_gdp(self):
        data = {
            "Germany": [
                {"year": 2020, "gdp": 400.0},
                {"year": 2021, "gdp": 420.0}
            ]
        }

        report = AverageGdpReport()
        result = report.generate(data)

        assert "country" in result[0]
        assert "avg_gdp" in result[0]
        assert len(result[0]) == 2
