import pytest

from src.report_type import generate_report
from src.reports.average_gdp import AverageGdpReport
from src.reports.base import BaseReport


class TestGenerateReport:
    def test_generate_report_single_valid(self):

        report_classes = generate_report(["average-gdp"])

        assert len(report_classes) == 1
        assert report_classes[0] is AverageGdpReport
        assert issubclass(report_classes[0], BaseReport)

    def test_generate_report_multiple_calls_same_result(self):

        result1 = generate_report(["average-gdp"])
        result2 = generate_report(["average-gdp"])

        assert result1 == result2
        assert result1[0] is result2[0]

    def test_generate_report_unknown_report_name_raises_value_error(self):
        with pytest.raises(ValueError, match="Неизвестный тип отчёта: fake-report"):
            generate_report(["fake-report"])

    def test_generate_report_empty_list_returns_empty_list(self):
        report_classes = generate_report([])
        assert report_classes == []

    def test_generate_report_mixed_valid_and_invalid(self):
        with pytest.raises(ValueError, match="Неизвестный тип отчёта: invalid"):
            generate_report(["average-gdp", "invalid"])

    def test_generate_report_case_sensitive(self):
        with pytest.raises(ValueError, match="Неизвестный тип отчёта: AVERAGE-GDP"):
            generate_report(["AVERAGE-GDP"])


def test_generate_report_returns_list_of_types():
    report_classes = generate_report(["average-gdp"])

    for cls in report_classes:
        assert isinstance(cls, type)
        assert issubclass(cls, BaseReport)
