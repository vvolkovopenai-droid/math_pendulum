import cv2

from my_lib.constants import (DEFAULT_FPS, WINDOW_NAME, WAIT_KEY_DELAY,
                              ESC_KEY_CODE, AMOUNT_OF_DATA_REQUIRED_TO_CALCULATE_THE_PERIOD, VIDEO_PATH)
from my_lib.tracker import BallTracker
from my_lib.calculator import calculate_period
from my_lib.visualizer import Drawer


class PendulumTrackerApp:

    def __init__(self):
        self.video_path = VIDEO_PATH
        self.cap = None # переменная capture для захвата видео
        self.fps = DEFAULT_FPS
        self.total_frames = 0
        self.frame_num = 0
        self.tracker = BallTracker()
        self.drawer = Drawer()

        # Хранилища данных
        self.timestamps = [] # время каждого кадра в секундах
        self.x_vals = []
        self.y_vals = []

    def open_video(self):
        print(f"Попытка открыть видео: {self.video_path}")
        self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            print("Не удалось открыть видео.")
            return False

        video_fps = self.cap.get(cv2.CAP_PROP_FPS)
        if video_fps > 0:
            self.fps = video_fps

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"Параметры видео:")
        print(f"   - Путь: {self.video_path}")
        print(f"   - FPS: {self.fps:.2f}")
        print(f"   - Кадров: {self.total_frames}")

        return True

    def process_frame(self, frame):
        current_time = self.frame_num / self.fps

        center = self.tracker.track(frame)

        if center is not None:
            x, y = center

            self.timestamps.append(current_time)
            self.x_vals.append(float(x))
            self.y_vals.append(float(y))

            self.drawer.update_trajectory(center)
            self.drawer.draw(frame, center)

    def handle_exit_key(self, key) :

        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            return True
        if key == ESC_KEY_CODE:
            return True
        return False

    def run(self):

        if not self.open_video():
            return None

        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Конец видео")
                break

            self.frame_num += 1

            self.process_frame(frame)

            if len(self.x_vals) > 0:
                current_period = calculate_period(
                    self.x_vals, self.y_vals, self.timestamps, self.fps
                )
                self.drawer.draw_period_text(frame, current_period)

            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(WAIT_KEY_DELAY) & 0xFF
            if self.handle_exit_key(key):
                break

        self.cap.release()
        cv2.destroyAllWindows()

        print(f"\nСтатистика:")
        print(f"   - Обработано кадров: {self.frame_num}")
        print(f"   - Найдено координат: {len(self.x_vals)}")

        if len(self.x_vals) < AMOUNT_OF_DATA_REQUIRED_TO_CALCULATE_THE_PERIOD:
            print("Слишком мало данных для расчёта периода.")
            return None

        period = calculate_period(self.x_vals,
                                  self.y_vals,
                                  self.timestamps,
                                  self.fps)

        if period is not None and period > 0:
            print(f" ИТОГОВЫЙ ПЕРИОД КОЛЕБАНИЙ: {period:.3f} сек")
        elif period == 0.0:
            print("Не удалось рассчитать период (недостаточно пересечений нуля).")
        else:
            print("Не удалось рассчитать период.")


        return period