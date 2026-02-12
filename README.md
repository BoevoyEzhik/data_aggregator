# Анализ экономических данных

Скрипт для анализа макроэкономических показателей стран из CSV-файлов.

## Установка


```bash
pip install -r requirements.txt
```

Для запуска тестов:
```bash
pip install -r requirements-test.txt
```

## Использование

Основная команда:
```bash
python main.py --files <путь_к_файлу1.csv> <путь_к_файлу2.csv> --report <тип_отчёта>
```

### Пример запуска

```bash
python main.py --files economic1.csv economic2.csv --report average-gdp
```

Вывод:
```
--- Отчёт: AverageGdp ---
|    | country        |   avg_gdp |
|----|----------------|-----------|
|  1 | United States  |  23923.67 |
|  2 | China          |  17810.33 |


```

### Доступные отчеты

- `average-gdp` — среднее значение ВВП по странам (сортировка по убыванию)

## Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск с покрытием кода
pytest --cov=src --cov-report=term-missing

# Запуск конкретного теста
pytest tests/test_reports.py
```


## Формат CSV-файлов

CSV-файлы должны содержать следующие колонки:
- `country` — название страны
- `year` — год
- `gdp` — валовой внутренний продукт (в долларах)
- `gdp_growth` — рост ВВП (%)
- `inflation` — инфляция (%)
- `unemployment` — уровень безработицы (%)
- `population` — население
- `continent` — континент

Пример:
```csv
country,year,gdp,gdp_growth,inflation,unemployment,population,continent 
Germany,2020,3800000000000,0.8,1.5,3.2,83000000,Europe 
France,2020,2600000000000,0.7,1.1,8.1,67000000,Europe
```
## Требования к данным

- Поля `gdp`, `gdp_growth`, `inflation`, `unemployment`, `population` могут быть пустыми — они будут интерпретированы как `None`.
- Пустые строки или строки без обязательных полей (`country`, `year`, `gdp`) вызовут ошибку.
