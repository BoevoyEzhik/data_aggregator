# Анализ рейтинга брендов

Скрипт для анализа данных о рейтингах товаров из CSV файлов.

## Установка

```bash
pip install -r requirements.txt
```

Для разработки (с тестами):
```bash
pip install -r dev.txt
```

## Использование

Основная команда:
```bash
python main.py --files <путь_к_файлу1.csv> <путь_к_файлу2.csv> --report <тип_отчета>
```

### Пример запуска

```bash
python main.py --files products1.csv products2.csv --report average-rating
```

Вывод:
```
+----+----------+----------+
|    | brand    |   rating |
|----+----------+----------|
|  1 | apple    |     4.55 |
|  2 | samsung  |     4.53 |
|  3 | xiaomi   |     4.37 |
+----+----------+----------+
```

### Доступные отчеты

- `average-rating` — средний рейтинг по брендам (бренды сортируются по рейтингу)

## Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск с покрытием кода
pytest --cov=src --cov-report=term-missing

# Запуск конкретного теста
pytest tests/test_reports.py
```


## Формат CSV файлов

CSV файлы должны содержать следующие колонки:
- `name` — название товара
- `brand` — бренд
- `price` — цена
- `rating` — рейтинг

Пример:
```csv
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
```
