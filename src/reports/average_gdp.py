from typing import Dict, List, Union

from src.reports.base import BaseReport, EconomicData


class AverageGdpReport(BaseReport):
    def generate(self, data: EconomicData) -> List[Dict[str, Union[str, float]]]:

        result: List[Dict[str, Union[str, float]]] = []

        for country, records in data.items():
            gdp_values = [r["gdp"] for r in records if r["gdp"] is not None]

            if not gdp_values:
                continue

            avg_gdp = sum(gdp_values) / len(gdp_values)
            result.append(
                {
                    "country": country,
                    "avg_gdp": round(avg_gdp, 2),
                }
            )

        result.sort(key=lambda x: x["avg_gdp"], reverse=True)

        return result
