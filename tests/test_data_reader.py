from unittest.mock import patch
import csv
from io import StringIO
import pytest

from src.data_reader import DataReader


class TestReadAllFiles:
    @patch("src.data_reader.DataReader._read_single_file")
    def test_read_all_files_success(self, mock_read_single):
        reader = DataReader()
        file_paths = ["file1.csv", "file2.csv"]

        result = reader.read_all_files(file_paths)

        assert mock_read_single.call_count == 2
        mock_read_single.assert_any_call("file1.csv")
        mock_read_single.assert_any_call("file2.csv")
        assert result == {}  # потому что mock, данные не заполняются

    @patch("src.data_reader.DataReader._read_single_file")
    def test_read_all_files_first_file_not_found(self, mock_read_single):
        mock_read_single.side_effect = [FileNotFoundError(), None]

        reader = DataReader()

        with pytest.raises(FileNotFoundError, match=r"Файл не найден: file1\.csv"):
            reader.read_all_files(["file1.csv", "file2.csv"])

    @patch("src.data_reader.DataReader._read_single_file")
    def test_read_all_files_second_file_not_found(self, mock_read_single):
        mock_read_single.side_effect = [None, FileNotFoundError()]

        reader = DataReader()

        with pytest.raises(FileNotFoundError, match=r"Файл не найден: file2\.csv"):
            reader.read_all_files(["file1.csv", "file2.csv"])

    @patch("src.data_reader.DataReader._read_single_file")
    def test_read_all_files_value_error(self, mock_read_single):
        mock_read_single.side_effect = ValueError("test error")

        reader = DataReader()

        with pytest.raises(ValueError, match=r"Ошибка при чтении файла file1\.csv: test error"):
            reader.read_all_files(["file1.csv"])

    def test_read_all_files_returns_dict(self):
        reader = DataReader()
        reader.data["Germany"].append({"year": 2020, "gdp": 1.0})

        result = reader.read_all_files([])

        assert isinstance(result, dict)
        assert "Germany" in result
        assert len(result["Germany"]) == 1
        assert result["Germany"][0]["year"] == 2020


class TestReadSingleFile:
    def create_mock_csv(self, data):
        output = StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return output.getvalue()

    @patch("builtins.open")
    def test_read_single_file_success(self, mock_file):
        mock_data = [
            {"country": "Germany", "year": "2020", "gdp": "3800000000000", "gdp_growth": "0.8",
             "inflation": "1.5", "unemployment": "3.2", "population": "83000000", "continent": "Europe"},
            {"country": "France", "year": "2020", "gdp": "2600000000000", "gdp_growth": "0.7",
             "inflation": "1.1", "unemployment": "8.1", "population": "67000000", "continent": "Europe"}
        ]
        csv_content = self.create_mock_csv(mock_data)

        mock_file.return_value.__enter__.return_value = StringIO(csv_content)

        reader = DataReader()

        with patch.object(reader, '_process_row') as mock_process_row:
            reader._read_single_file("dummy.csv")

            assert mock_process_row.call_count == 2
            mock_process_row.assert_any_call(mock_data[0])
            mock_process_row.assert_any_call(mock_data[1])


class TestProcessRow:
    def test_process_row_valid_data(self):
        reader = DataReader()
        row = {
            "country": "Germany",
            "year": "2020",
            "gdp": "3800000000000",
            "gdp_growth": "0.8",
            "inflation": "1.5",
            "unemployment": "3.2",
            "population": "83000000",
            "continent": "Europe"
        }

        reader._process_row(row)

        assert "Germany" in reader.data
        record = reader.data["Germany"][0]
        assert record["year"] == 2020
        assert record["gdp"] == 3800000000000.0
        assert record["gdp_growth"] == 0.8
        assert record["inflation"] == 1.5
        assert record["unemployment"] == 3.2
        assert record["population"] == 83000000
        assert record["continent"] == "Europe"

    def test_process_row_empty_numeric_fields(self):
        reader = DataReader()
        row = {
            "country": "Japan",
            "year": "2020",
            "gdp": "",
            "gdp_growth": "",
            "inflation": "",
            "unemployment": "",
            "population": "",
            "continent": "Asia"
        }

        reader._process_row(row)

        japan = reader.data["Japan"][0]
        assert japan["gdp"] is None
        assert japan["gdp_growth"] is None
        assert japan["inflation"] is None
        assert japan["unemployment"] is None
        assert japan["population"] is None

    def test_process_row_missing_country(self):
        reader = DataReader()
        row = {
            "year": "2020",
            "gdp": "1.0",
            "gdp_growth": "0.8",
            "inflation": "1.5",
            "unemployment": "3.2",
            "population": "83000000",
            "continent": "Europe"
        }

        with pytest.raises(KeyError):
            reader._process_row(row)

    def test_process_row_invalid_year(self):
        reader = DataReader()
        row = {
            "country": "Germany",
            "year": "abc",
            "gdp": "1.0",
            "gdp_growth": "0.8",
            "inflation": "1.5",
            "unemployment": "3.2",
            "population": "83000000",
            "continent": "Europe"
        }

        with pytest.raises(ValueError, match=r"Ошибка преобразования данных в строке"):
            reader._process_row(row)

    def test_process_row_invalid_gdp(self):
        reader = DataReader()
        row = {
            "country": "Germany",
            "year": "2020",
            "gdp": "invalid",
            "gdp_growth": "0.8",
            "inflation": "1.5",
            "unemployment": "3.2",
            "population": "83000000",
            "continent": "Europe"
        }

        with pytest.raises(ValueError, match=r"Ошибка преобразования данных в строке"):
            reader._process_row(row)

    def test_process_row_invalid_population_float_string(self):
        reader = DataReader()
        row = {
            "country": "India",
            "year": "2020",
            "gdp": "2.7e12",
            "gdp_growth": "1.2",
            "inflation": "4.0",
            "unemployment": "5.5",
            "population": "1380000000.0",  # Это вызовет ValueError
            "continent": "Asia"
        }

        with pytest.raises(ValueError, match=r"Ошибка преобразования данных в строке"):
            reader._process_row(row)

    def test_process_row_population_integer_string(self):
        reader = DataReader()
        row = {
            "country": "India",
            "year": "2020",
            "gdp": "2.7e12",
            "gdp_growth": "1.2",
            "inflation": "4.0",
            "unemployment": "5.5",
            "population": "1380000000",
            "continent": "Asia"
        }

        reader._process_row(row)

        india = reader.data["India"][0]
        assert india["population"] == 1380000000
        assert isinstance(india["population"], int)

    def test_process_row_multiple_rows_same_country(self):
        reader = DataReader()
        row1 = {
            "country": "Germany",
            "year": "2020",
            "gdp": "3.8e12",
            "gdp_growth": "0.8",
            "inflation": "1.5",
            "unemployment": "3.2",
            "population": "83000000",
            "continent": "Europe"
        }
        row2 = {
            "country": "Germany",
            "year": "2021",
            "gdp": "4.1e12",
            "gdp_growth": "2.9",
            "inflation": "3.1",
            "unemployment": "3.1",
            "population": "83200000",
            "continent": "Europe"
        }

        reader._process_row(row1)
        reader._process_row(row2)

        germany = reader.data["Germany"]
        assert len(germany) == 2
        assert germany[0]["year"] == 2020
        assert germany[1]["year"] == 2021

    def test_process_row_continent_stripped(self):
        reader = DataReader()
        row = {
            "country": "Japan",
            "year": "2020",
            "gdp": "5.0e12",
            "gdp_growth": "1.0",
            "inflation": "2.0",
            "unemployment": "2.8",
            "population": "126000000",
            "continent": " Asia "
        }

        reader._process_row(row)

        japan = reader.data["Japan"][0]
        assert japan["continent"] == "Asia"


