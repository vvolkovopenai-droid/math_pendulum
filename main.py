import sys
import os

# Добавляем текущую папку в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from my_lib.constants import VIDEO_PATH
from my_lib.app import PendulumTrackerApp


def main():

    # Здесь можно изменить режим отрисовки:
    draw_trajectory = True # True - с линией, False - без


    # Создаём и запускаем приложение
    app = PendulumTrackerApp(VIDEO_PATH, draw_trajectory)
    period = app.run()

    if period is not None and period > 0:
        print(f" ИТОГОВЫЙ ПЕРИОД КОЛЕБАНИЙ: {period:.3f} сек")
    elif period == 0.0:
        print("Не удалось рассчитать период (недостаточно пересечений нуля).")
    else:
        print("Не удалось рассчитать период.")


if __name__ == "__main__":
    main()