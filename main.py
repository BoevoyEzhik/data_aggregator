from tabulate import tabulate  # type: ignore

from src.cli import parse_arguments, validate_arguments
from src.data_reader import DataReader
from src.report_type import generate_report


def main() -> None:

    args = parse_arguments()
    validate_arguments(args)

    data_reader = DataReader()
    try:
        data = data_reader.read_all_files(file_paths=args.files)
    except Exception as e:
        print(f"Ошибка при чтении файлов: {e}")
        return

    if not data:
        print("Нет данных для обработки.")
        return

    report_classes = generate_report(args.report)

    for ReportClass in report_classes:
        report = ReportClass()
        try:
            report_data = report.generate(data)
        except Exception as e:
            print(f"Ошибка при генерации отчёта {ReportClass.__name__}: {e}")
            continue

        if not report_data:
            print(f"Отчёт {ReportClass.__name__} не содержит данных.")
            continue


        print(f"\n--- Отчёт: {ReportClass.__name__.replace('Report', '')} ---")
        print(
            tabulate(
                report_data,
                headers="keys",
                tablefmt="github",
                floatfmt=".2f",
                showindex=range(1, len(report_data) + 1),
            )
        )


if __name__ == "__main__":
    main()
