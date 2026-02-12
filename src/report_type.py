from typing import Dict, List, Type

from src.reports.average_gdp import AverageGdpReport
from src.reports.base import BaseReport


def generate_report(report_names: List[str]) -> List[Type[BaseReport]]:
    available_reports: Dict[str, Type[BaseReport]] = {
        "average-gdp": AverageGdpReport,
    }

    reports: List[Type[BaseReport]] = []
    for name in report_names:
        if name in available_reports:
            reports.append(available_reports[name])
        else:
            raise ValueError(f"Неизвестный тип отчёта: {name}")
    return reports
