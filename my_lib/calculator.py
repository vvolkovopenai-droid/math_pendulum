import numpy as np
from typing import List, Optional

from my_lib.constants import THE_AMOUNT_OF_DATA_REQUIRED_FOR_ANALYSIS


def calculate_period(x_coords: List[float],
                     y_coords: List[float],
                     timestamps: List[float],
                     fps: float) -> Optional[float]:
    """
    Рассчитывает период колебаний по координатам грузика.

    Алгоритм:
    1. Центрирует координаты (вычитает среднее)
    2. Находит моменты пересечения нуля (снизу вверх)
    3. Вычисляет средний период между пересечениями

    Параметры:
        x_coords: список X-координат грузика
        y_coords: список Y-координат (не используется)
        timestamps: временные метки (не используются)
        fps: частота кадров видео

    Возвращает:
        Период в секундах или 0.0, если данных недостаточно
    """
    # Проверяем, достаточно ли данных для анализа
    if len(x_coords) < THE_AMOUNT_OF_DATA_REQUIRED_FOR_ANALYSIS:
        return 0.0

    # Преобразуем список в массив NumPy для удобства вычислений
    x = np.array(x_coords)

    # Центрируем данные: находим положение равновесия (среднее)
    # и вычитаем его, чтобы колебания происходили вокруг нуля
    average_x = x.mean()
    centered_x = x - average_x

    # Ищем моменты, когда грузик проходит через положение равновесия
    # (пересечение нуля снизу вверх)
    crossings = []
    for i in range(1, len(centered_x)):
        # Проверяем, было ли значение отрицательным, а стало неотрицательным
        if centered_x[i - 1] < 0 and centered_x[i] >= 0:
            dy = centered_x[i] - centered_x[i - 1]
            if dy == 0:
                continue

            # Линейная интерполяция для точного момента пересечения
            # fraction показывает, какую долю интервала между кадрами
            # заняло пересечение
            fraction = abs(centered_x[i - 1]) / dy

            # Точный индекс кадра (с дробной частью)
            exact_frame_idx = (i - 1) + fraction
            crossings.append(exact_frame_idx)

    # Если нашли меньше двух пересечений, период определить нельзя
    if len(crossings) < THE_AMOUNT_OF_DATA_REQUIRED_FOR_ANALYSIS:
        return 0.0

    # Разности между последовательными пересечениями - это периоды в кадрах
    periods_in_frames = np.diff(crossings)

    # Усредняем периоды для повышения точности
    mean_period_frames = np.mean(periods_in_frames)

    # Переводим из кадров в секунды
    return mean_period_frames / fps