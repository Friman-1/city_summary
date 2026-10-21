# City Summary
CLI-утилита «Сводка по городу», которая получает погоду и курс валюты к рублю из внешних API и печатает сводку.

# Требования
Python 3.12

Библиотека requests (указана в requirements.txt)

## Установка
`pip install -r requirements.txt`

## Запуск
`python main.py --city [Город]`

### Курс другой валюты (по умолчанию USD):

`python main.py --city Moscow --currency EUR`

### Сводка в формате JSON:

`python main.py --city Moscow --json`