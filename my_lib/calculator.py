import numpy as np

from my_lib.constants import THE_AMOUNT_OF_DATA_REQUIRED_FOR_ANALYSIS


def calculate_period(x_coords, y_coords, timestamps, fps):

    # Проверяем, достаточно ли данных для анализа
    if len(x_coords) < THE_AMOUNT_OF_DATA_REQUIRED_FOR_ANALYSIS:
        return 0.0

    x = np.array(x_coords)

    average_x = x.mean()
    centered_x = x - average_x

    # Ищем моменты, когда грузик проходит через положение равновесия
    crossings = []
    for i in range(1, len(centered_x)):
        # Проверяем, было ли значение отрицательным, а стало неотрицательным
        if centered_x[i - 1] < 0 and centered_x[i] >= 0:
            dy = centered_x[i] - centered_x[i - 1]
            if dy == 0:
                continue

            fraction = abs(centered_x[i - 1]) / dy

            exact_frame_idx = (i - 1) + fraction
            crossings.append(exact_frame_idx)

    # Если нашли меньше двух пересечений, период определить нельзя
    if len(crossings) < THE_AMOUNT_OF_DATA_REQUIRED_FOR_ANALYSIS:
        return 0.0

    periods_in_frames = np.diff(crossings)

    mean_period_frames = np.mean(periods_in_frames)

    return mean_period_frames / fps