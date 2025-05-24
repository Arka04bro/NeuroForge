#!/usr/bin/env python3

"""
Интерфейс для предсказания класса дрона по техническим характеристикам.
"""

import joblib
import numpy as np

# Пути к сохранённым моделям
model_path = "/home/eraly/projects/remember-ai/random_forest_model.pkl"
scaler_path = "/home/eraly/projects/remember-ai/scaler.pkl"

# Загрузка обученных компонентов с обработкой ошибок
try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except FileNotFoundError:
    print("Ошибка: не удалось найти сохранённые модели. Убедитесь, что обучение было выполнено.")
    exit(1)

# Словарь для обратного маппинга классов (на основе предоставленного порядка)
inverse_class_mapping = {
    0: 'FPV гоночный',
    1: 'Доставка',
    2: 'Игрушечный',
    3: 'Исследовательский',
    4: 'Любительский фото/видео',
    5: 'Профессиональный фото/видео',
    6: 'Сельскохозяйственный'
}

# Список признаков
features = [
    "Разрешение камеры (МП)",
    "Время полета (мин)",
    "Макс. ускорение (м/с²)",
    "Макс. высота (м)",
    "Макс. дальность (м)",
    "Макс. скорость (м/с)"
]

print("Введите характеристики дрона:")

# Сбор пользовательского ввода
input_data = []
for feature in features:
    while True:
        try:
            value = float(input(f"- {feature}: "))
            input_data.append(value)
            break
        except ValueError:
            print("Ошибка: введите числовое значение.")

# Преобразуем в массив и масштабируем
input_array = np.array([input_data])
input_scaled = scaler.transform(input_array)

# Предсказание
predicted_class_index = model.predict(input_scaled)[0]
predicted_label = inverse_class_mapping[predicted_class_index]

print(f"\n✅ Предсказанный класс дрона: {predicted_label}")
