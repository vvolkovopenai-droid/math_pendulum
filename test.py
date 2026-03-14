#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Тестовый файл для проверки импортов и структуры проекта.
"""

import sys
import os

print("=" * 50)
print("ПРОВЕРКА ИМПОРТОВ")
print("=" * 50)

print(f"\n📁 Текущая директория: {os.getcwd()}")
print(f"📁 Python путь:")

for i, p in enumerate(sys.path):
    print(f"  {i}: {p}")

print("\n📁 Содержимое текущей папки:")
for item in os.listdir('.'):
    print(f"  - {item}")

print("\n📁 Проверка папки my_lib:")
if os.path.exists('my_lib'):
    print("  ✅ Папка my_lib существует")
    print("  Содержимое my_lib:")
    for item in os.listdir('my_lib'):
        if item.endswith('.py') or item == '__init__.py':
            print(f"    - {item}")
else:
    print("  ❌ Папка my_lib НЕ найдена!")

print("\n📁 Проверка видеофайла:")
video_path = "source/videos/object2.mp4"
if os.path.exists(video_path):
    print(f"  ✅ Видео найдено: {video_path}")
    print(f"  Размер: {os.path.getsize(video_path)} байт")
else:
    print(f"  ❌ Видео НЕ найдено: {video_path}")

    # Проверяем папку source
    if os.path.exists('source'):
        print("  Папка source существует")
        if os.path.exists('source/videos'):
            print("  Папка source/videos существует")
            print("  Файлы в source/videos:")
            for f in os.listdir('source/videos'):
                print(f"    - {f}")
        else:
            print("  ❌ Папка source/videos НЕ найдена")
    else:
        print("  ❌ Папка source НЕ найдена")

print("\n📁 Пробуем импортировать модули:")

try:
    from my_lib.constants import VIDEO_PATH, WINDOW_NAME

    print(f"  ✅ constants.VIDEO_PATH = {VIDEO_PATH}")
except Exception as e:
    print(f"  ❌ Ошибка импорта constants: {e}")

try:
    from my_lib.tracker import BallTracker

    print("  ✅ tracker импортирован")
except Exception as e:
    print(f"  ❌ Ошибка импорта tracker: {e}")

try:
    from my_lib.calculator import calculate_period

    print("  ✅ calculator импортирован")
except Exception as e:
    print(f"  ❌ Ошибка импорта calculator: {e}")

try:
    from my_lib.visualizer import Drawer

    print("  ✅ visualizer импортирован")
except Exception as e:
    print(f"  ❌ Ошибка импорта visualizer: {e}")

try:
    from my_lib.app import PendulumTrackerApp

    print("  ✅ app импортирован")
except Exception as e:
    print(f"  ❌ Ошибка импорта app: {e}")

print("\n✅ Проверка завершена!")