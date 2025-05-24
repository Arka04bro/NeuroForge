#!/usr/bin/env python3

"""
Интерфейс для предсказания класса дрона по техническим характеристикам.
"""

import joblib
import numpy as np

# Пути к сохранённым моделям
model_path = "random_forest_model.pkl"
scaler_path = "scaler.pkl"
encoder_path = "label_encoder.pkl"

# Загрузка обученных компонентов с обработкой ошибок
try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(encoder_path)
except FileNotFoundError:
    print("Ошибка: не удалось найти сохранённые модели. Убедитесь, что обучение было выполнено.")
    exit(1)

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
predicted_label = label_encoder.inverse_transform([predicted_class_index])[0]

print(f"\n✅ Предсказанный класс дрона: {predicted_label}") 

'''
Введите характеристики дрона:
- Разрешение камеры (МП):  12
- Время полета (мин):  30
- Макс. ускорение (м/с²):  4
- Макс. высота (м):  3000
- Макс. дальность (м):  4000
- Макс. скорость (м/с):  13

✅ Предсказанный класс дрона: Любительский фото/видео
'''
