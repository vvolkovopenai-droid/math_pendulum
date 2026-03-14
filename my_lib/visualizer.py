import cv2
import numpy as np
from typing import Tuple, List

from my_lib.constants import (TRAJECTORY_LENGTH, CIRCLE_COLOR, CIRCLE_RADIUS,
                              LINE_THICKNESS, TEXT_X_DISTANCE,
                              TEXT_Y_DISTANCE, TEXT_PERIOD_SIZE, TEXT_PERIOD_COLOR, TEXT_PERIOD_THICKNESS,
                              TEXT_COORDINATES_SCALE, TEXT_COORDINATES_THICKNESS, TEXT_COORDINATES_COLOR,
                              LINE_COORDINATES_COLOR, X_POSITION_PERIOD, Y_POSITION_PERIOD)


class Drawer:

    def __init__(self, draw_trajectory: bool = True):
        self.draw_trajectory = draw_trajectory
        self.trajectory = []  # список точек для линии
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def draw_point(self, frame: np.ndarray, center: Tuple[int, int]) -> None:
        """Рисует точку в центре объекта."""
        x, y = center
        cv2.circle(
            frame,
            (x, y),
            CIRCLE_RADIUS,
            CIRCLE_COLOR,
            -1  # залитый круг
        )

    def draw_trajectory_line(self, frame: np.ndarray) -> None:
        """Рисует линию траектории из последних точек."""
        for i in range(1, len(self.trajectory)):
            cv2.line(
                frame,
                self.trajectory[i - 1],
                self.trajectory[i],
                LINE_COORDINATES_COLOR,
                LINE_THICKNESS
            )

    def draw_coordinates_text(self, frame: np.ndarray,
                               center: Tuple[int, int]) -> None:
        """Рисует текст с координатами рядом с объектом."""
        x, y = center
        cv2.putText(
            frame,
            f"({x}, {y})",
            (x + TEXT_X_DISTANCE, y - TEXT_Y_DISTANCE),
            self.font,
            TEXT_COORDINATES_SCALE,
            TEXT_COORDINATES_COLOR,
            TEXT_COORDINATES_THICKNESS
        )

    def update_trajectory(self, center: Tuple[int, int]) -> None:
        """Обновляет список точек траектории."""
        if self.draw_trajectory:
            self.trajectory.append(center)
            if len(self.trajectory) > TRAJECTORY_LENGTH:
                self.trajectory.pop(0)

    def draw(self, frame: np.ndarray, center: Tuple[int, int]) -> None:
        """
        Основной метод отрисовки.
        Рисует точку, координаты и (опционально) линию траектории.
        """
        self.draw_point(frame, center)
        self.draw_coordinates_text(frame, center)

        if self.draw_trajectory:
            self.draw_trajectory_line(frame)

    def draw_period_text(self, frame: np.ndarray, period: float) -> None:
        """Рисует текст с текущим периодом в верхнем левом углу."""
        cv2.putText(
            frame,
            f"Period: {period:.3f} s",
            (X_POSITION_PERIOD, Y_POSITION_PERIOD),
            self.font,
            TEXT_PERIOD_SIZE,  # размер
            TEXT_PERIOD_COLOR,
            TEXT_PERIOD_THICKNESS  # толщина
        )

    # def draw_info(self, frame: np.ndarray, frame_num: int, points_count: int) -> None:
    #     """Рисует дополнительную информацию на кадре."""
    #     cv2.putText(
    #         frame,
    #         f"Frame: {frame_num}",
    #         (20, 70),
    #         self.font,
    #         0.7,
    #         TEXT_COLOR,
    #         1
    #     )
    #     cv2.putText(
    #         frame,
    #         f"Points: {points_count}",
    #         (20, 100),
    #         self.font,
    #         0.7,
    #         TEXT_COLOR,
    #         1
    #     )