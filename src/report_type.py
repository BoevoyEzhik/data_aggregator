from typing import Type, List

from src.reports.average_gdp import AverageGdpReport
from src.reports.base import BaseReport


def generate_report(report_names: List[str]) -> List[Type[BaseReport]]:
    available_reports = {
        "average-gdp": AverageGdpReport,
    }

    reports = []
    for name in report_names:
        if name in available_reports:
            reports.append(available_reports[name])
        else:
            raise ValueError(f"Неизвестный тип отчёта: {name}")
    return reports
