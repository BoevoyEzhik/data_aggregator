import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Генерация отчётов по экономическим данным"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Один или несколько CSV-файлов для обработки",
    )
    parser.add_argument(
        "--report",
        nargs="+",
        required=True,
        choices=["average-gdp"],
        help="Тип отчёта для генерации",
    )
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> None:
    if not args.files:
        raise ValueError("Необходимо указать хотя бы один файл")

    if not args.report:
        raise ValueError("Необходимо указать тип отчета")
