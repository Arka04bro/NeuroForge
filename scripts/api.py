#!/usr/bin/env python3
"""
Скрипт для получения текущей скорости ветра в Актобе через WeatherAPI.com
Данные сохраняются в формате JSON и могут быть запущены по расписанию.
Также выводится оценка ветра по шкале Бофорта для дронов.

Для использования необходимо:
1. Зарегистрироваться на сайте https://www.weatherapi.com/ и получить API-ключ
2. Вставить API-ключ в переменную API_KEY ниже или передать через --api-key
3. Запустить скрипт вручную или настроить запуск по расписанию через cron
"""

import requests
import json
import os
import datetime
import sys

# Конфигурация
API_KEY = "8ba21d6fd9124110af0115102252305"  # Замените на ваш API-ключ с WeatherAPI.com
CITY = "Aktobe"  # Город для получения данных
BASE_URL = "https://api.weatherapi.com/v1/current.json"
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "wind_data")

# Шкала Бофорта для дронов
BEAUFORT_SCALE = [
    {"level": 0, "min_speed": 0, "max_speed": 1.5, "description": "Воздействие отсутствует"},
    {"level": 1, "min_speed": 1.5, "max_speed": 5, "description": "Очень легкий ветер, полет не затруднен"},
    {"level": 2, "min_speed": 5, "max_speed": 11, "description": "Идеален для спокойных полетов"},
    {"level": 3, "min_speed": 11, "max_speed": 19, "description": "Заметно для малых дронов (например, линейка Mini)"},
    {"level": 4, "min_speed": 19, "max_speed": 29, "description": "Умеренный ветер, предел для полета многих потребительских моделей"},
    {"level": 5, "min_speed": 29, "max_speed": 39, "description": "Сильный ветер, сложности даже для профессиональных моделей"},
    {"level": 6, "min_speed": 39, "max_speed": 50, "description": "Крайний предел, полеты невозможны для большинства дронов"},
    {"level": 7, "min_speed": 50, "max_speed": float('inf'), "description": "Экстремальный ветер, полеты запрещены"}
]

def get_beaufort_level(wind_speed_kph):
    """
    Определяет уровень ветра по шкале Бофорта для дронов
    
    Args:
        wind_speed_kph (float): Скорость ветра в км/ч
        
    Returns:
        dict: Информация о уровне ветра по шкале Бофорта
    """
    for level in BEAUFORT_SCALE:
        if level["min_speed"] <= wind_speed_kph < level["max_speed"]:
            return level
    
    # Если скорость выше всех уровней
    return BEAUFORT_SCALE[-1]

def get_wind_data(api_key, city):
    """
    Получает текущие данные о скорости ветра для указанного города
    
    Args:
        api_key (str): API-ключ для доступа к WeatherAPI.com
        city (str): Название города
        
    Returns:
        dict: Словарь с данными о ветре или None в случае ошибки
    """
    params = {
        'key': api_key,
        'q': city,
        'aqi': 'no'  # Не включать данные о качестве воздуха
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        
        data = response.json()
        
        # Получаем скорость ветра
        wind_speed_kph = data['current']['wind_kph']
        
        # Определяем уровень по шкале Бофорта
        beaufort_level = get_beaufort_level(wind_speed_kph)
        
        # Извлекаем только данные о ветре
        wind_data = {
            'location': {
                'name': data['location']['name'],
                'region': data['location']['region'],
                'country': data['location']['country'],
                'lat': data['location']['lat'],
                'lon': data['location']['lon'],
                'localtime': data['location']['localtime']
            },
            'wind': {
                'speed_kph': wind_speed_kph,
                'speed_mph': data['current']['wind_mph'],
                'direction_degree': data['current']['wind_degree'],
                'direction': data['current']['wind_dir'],
                'gust_kph': data['current']['gust_kph'],
                'gust_mph': data['current']['gust_mph'],
                'beaufort_level': beaufort_level['level'],
                'beaufort_description': beaufort_level['description']
            },
            'last_updated': data['current']['last_updated'],
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        return wind_data
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Ошибка при обработке данных: {e}")
        return None

def save_wind_data(data, output_dir=DEFAULT_OUTPUT_DIR, filename=None):
    """
    Сохраняет данные о ветре в JSON-файл
    
    Args:
        data (dict): Данные о ветре для сохранения
        output_dir (str): Директория для сохранения файла
        filename (str, optional): Имя файла. Если не указано, генерируется автоматически
        
    Returns:
        str: Путь к сохраненному файлу или None в случае ошибки
    """
    if data is None:
        return None
    
    # Создаем директорию, если она не существует
    os.makedirs(output_dir, exist_ok=True)
    
    # Генерируем имя файла, если не указано
    if filename is None:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"wind_data_aktobe_{current_date}.json"
    
    # Полный путь к файлу
    file_path = os.path.join(output_dir, filename)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return file_path
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")
        return None

def save_latest_data(data, output_dir=DEFAULT_OUTPUT_DIR):
    """
    Сохраняет последние данные о ветре в файл latest.json
    
    Args:
        data (dict): Данные о ветре для сохранения
        output_dir (str): Директория для сохранения файла
        
    Returns:
        str: Путь к сохраненному файлу или None в случае ошибки
    """
    return save_wind_data(data, output_dir, "latest.json")

def parse_args():
    """
    Обрабатывает аргументы командной строки без использования argparse
    
    Returns:
        dict: Словарь с аргументами командной строки
    """
    args = {
        'output_dir': DEFAULT_OUTPUT_DIR,
        'api_key': API_KEY,
        'city': CITY,
        'latest_only': False
    }
    
    # Простой парсер аргументов без использования argparse
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == '--output-dir' and i + 1 < len(sys.argv):
            args['output_dir'] = sys.argv[i + 1]
            i += 2
        elif arg == '--api-key' and i + 1 < len(sys.argv):
            args['api_key'] = sys.argv[i + 1]
            i += 2
        elif arg == '--city' and i + 1 < len(sys.argv):
            args['city'] = sys.argv[i + 1]
            i += 2
        elif arg == '--latest-only':
            args['latest_only'] = True
            i += 1
        elif arg == '--help' or arg == '-h':
            print_help()
            sys.exit(0)
        else:
            i += 1
    
    return args

def print_help():
    """
    Выводит справку по использованию скрипта
    """
    print(f"""
Использование: {sys.argv[0]} [опции]

Опции:
  --output-dir DIR    Директория для сохранения данных (по умолчанию: {DEFAULT_OUTPUT_DIR})
  --api-key KEY       API-ключ для WeatherAPI.com (если не указан в скрипте)
  --city CITY         Город для получения данных (по умолчанию: {CITY})
  --latest-only       Сохранять только в файл latest.json без создания нового файла
  --help, -h          Показать эту справку и выйти
    """)

def print_beaufort_scale():
    """
    Выводит таблицу шкалы Бофорта для дронов
    """
    print("\nТаблица воздействия ветра по шкале Бофорта:")
    print("=" * 80)
    print(f"{'Уровень по Бофорту':<20} {'Скорость ветра':<20} {'Воздействие на дрон':<40}")
    print("-" * 80)
    
    for level in BEAUFORT_SCALE:
        if level["max_speed"] == float('inf'):
            speed_range = f"Более {level['min_speed']} км/ч"
        else:
            speed_range = f"{level['min_speed']} — {level['max_speed']} км/ч"
        
        print(f"Уровень {level['level']:<12} {speed_range:<20} {level['description']:<40}")
    
    print("=" * 80)

def main():
    """
    Основная функция скрипта
    """
    # Получаем аргументы командной строки
    args = parse_args()
    
    # Используем API-ключ из аргументов, если он указан
    api_key = args['api_key']
    
    if api_key == "YOUR_API_KEY":
        print("Ошибка: API-ключ не указан. Укажите его в скрипте или через аргумент --api-key")
        return
    
    # Получаем данные о ветре
    wind_data = get_wind_data(api_key, args['city'])
    
    if wind_data:
        # Сохраняем последние данные
        latest_file = save_latest_data(wind_data, args['output_dir'])
        
        if not args['latest_only']:
            # Сохраняем данные в новый файл с датой и временем
            history_file = save_wind_data(wind_data, args['output_dir'])
            if history_file:
                print(f"Данные о ветре сохранены в файл: {history_file}")
        
        if latest_file:
            print(f"Последние данные о ветре сохранены в файл: {latest_file}")
            
            # Выводим текущую скорость ветра
            print(f"\nТекущая скорость ветра в {wind_data['location']['name']}:")
            print(f"  {wind_data['wind']['speed_kph']} км/ч ({wind_data['wind']['speed_mph']} миль/ч)")
            print(f"  Направление: {wind_data['wind']['direction']} ({wind_data['wind']['direction_degree']}°)")
            print(f"  Порывы до: {wind_data['wind']['gust_kph']} км/ч")
            print(f"  Последнее обновление: {wind_data['last_updated']}")
            
            # Выводим оценку по шкале Бофорта
            print(f"\nОценка по шкале Бофорта для дронов:")
            print(f"  Уровень {wind_data['wind']['beaufort_level']}")
            print(f"  {wind_data['wind']['beaufort_description']}")
            
            # Выводим полную таблицу шкалы Бофорта
            print_beaufort_scale()

if __name__ == "__main__":
    main()

"""
Данные о ветре сохранены в файл: /home/eraly/wind_data/wind_data_aktobe_2025-05-23_17-21-33.json
Последние данные о ветре сохранены в файл: /home/eraly/wind_data/latest.json

Текущая скорость ветра в Aktobe:
  13.7 км/ч (8.5 миль/ч)
  Направление: SSE (147°)
  Порывы до: 15.7 км/ч
  Последнее обновление: 2025-05-23 17:15

Оценка по шкале Бофорта для дронов:
  Уровень 3
  Заметно для малых дронов (например, линейка Mini)

Таблица воздействия ветра по шкале Бофорта:
================================================================================
Уровень по Бофорту   Скорость ветра       Воздействие на дрон                     
--------------------------------------------------------------------------------
Уровень 0            0 — 1.5 км/ч         Воздействие отсутствует                 
Уровень 1            1.5 — 5 км/ч         Очень легкий ветер, полет не затруднен  
Уровень 2            5 — 11 км/ч          Идеален для спокойных полетов           
Уровень 3            11 — 19 км/ч         Заметно для малых дронов (например, линейка Mini)
Уровень 4            19 — 29 км/ч         Умеренный ветер, предел для полета многих потребительских моделей
Уровень 5            29 — 39 км/ч         Сильный ветер, сложности даже для профессиональных моделей
Уровень 6            39 — 50 км/ч         Крайний предел, полеты невозможны для большинства дронов
Уровень 7            Более 50 км/ч        Экстремальный ветер, полеты запрещены   
================================================================================
"""
