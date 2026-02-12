from argparse import Namespace
from unittest.mock import patch, MagicMock

import pytest

from src.cli import parse_arguments, validate_arguments


@patch("src.cli.argparse.ArgumentParser.parse_args")
def test_parse_arguments_success(mock_parse_args: MagicMock):
    mock_parse_args.return_value = Namespace(
        files=["data1.csv", "data2.csv"],
        report=["average-gdp"]
    )

    args = parse_arguments()

    assert args.files == ["data1.csv", "data2.csv"]
    assert args.report == ["average-gdp"]


@patch("src.cli.argparse.ArgumentParser.parse_args")
def test_parse_arguments_single_file(mock_parse_args: MagicMock):
    mock_parse_args.return_value = Namespace(
        files=["single.csv"],
        report=["average-gdp"]
    )

    args = parse_arguments()

    assert args.files == ["single.csv"]
    assert args.report == ["average-gdp"]


def test_validate_arguments_valid():
    args = Namespace(
        files=["data.csv"],
        report=["average-gdp"]
    )
    validate_arguments(args)


@pytest.mark.parametrize("invalid_files", [[], None])
def test_validate_arguments_no_files(invalid_files):
    args = Namespace(
        files=invalid_files,
        report=["average-gdp"]
    )
    with pytest.raises(ValueError, match="Необходимо указать хотя бы один файл"):
        validate_arguments(args)


@pytest.mark.parametrize("invalid_report", [[], None])
def test_validate_arguments_no_report(invalid_report):
    args = Namespace(
        files=["data.csv"],
        report=invalid_report
    )
    with pytest.raises(ValueError, match="Необходимо указать тип отчета"):
        validate_arguments(args)


@patch("src.cli.argparse.ArgumentParser.exit")
@patch("src.cli.argparse.ArgumentParser.error")
def test_parse_arguments_invalid_report_choice(mock_error: MagicMock, mock_exit: MagicMock):
    with patch("sys.argv", ["main.py", "--files", "data.csv", "--report", "unknown-report"]):
        parse_arguments()
        mock_error.assert_called()
