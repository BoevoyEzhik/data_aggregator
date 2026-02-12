import csv
from collections import defaultdict
from typing import Dict, List, DefaultDict


class DataReader:
    def __init__(self):
        self.data: DefaultDict[str, List[Dict]] = defaultdict(list)

    def read_all_files(self, file_paths: List[str]) -> Dict[str, List[Dict]]:
        for file_path in file_paths:
            try:
                self._read_single_file(file_path)
            except FileNotFoundError:
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            except Exception as e:
                raise ValueError(f"Ошибка при чтении файла {file_path}: {e}")
        return dict(self.data)

    def _read_single_file(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                self._process_row(row)

    def _process_row(self, row: Dict[str, str]) -> None:
        try:
            country = row["country"].strip()
            entry = {
                "year": int(row["year"]),
                "gdp": float(row["gdp"]) if row["gdp"] else None,
                "gdp_growth": float(row["gdp_growth"]) if row["gdp_growth"] else None,
                "inflation": float(row["inflation"]) if row["inflation"] else None,
                "unemployment": float(row["unemployment"]) if row["unemployment"] else None,
                "population": int(row["population"]) if row["population"] else None,
                "continent": row["continent"].strip(),
            }
            self.data[country].append(entry)
        except KeyError as e:
            raise KeyError(f"Отсутствует ожидаемый столбец в данных: {e}")
        except ValueError as e:
            raise ValueError(f"Ошибка преобразования данных в строке: {row}, ошибка: {e}")
