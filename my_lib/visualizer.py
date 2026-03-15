import cv2

from my_lib.constants import (TRAJECTORY_LENGTH, CIRCLE_COLOR, CIRCLE_RADIUS,
                              LINE_THICKNESS, TEXT_X_DISTANCE,
                              TEXT_Y_DISTANCE, TEXT_PERIOD_SIZE, TEXT_PERIOD_COLOR, TEXT_PERIOD_THICKNESS,
                              TEXT_COORDINATES_SCALE, TEXT_COORDINATES_THICKNESS, TEXT_COORDINATES_COLOR,
                              LINE_COORDINATES_COLOR, X_POSITION_PERIOD, Y_POSITION_PERIOD, DRAW_TRAJECTORY,
                              CIRCLE_INSIDE)


class Drawer:

    def __init__(self):
        self.draw_trajectory = DRAW_TRAJECTORY
        self.trajectory = []  # список точек для линии
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def draw_point(self, frame, center):
        x, y = center
        cv2.circle(
            frame,
            (x, y),
            CIRCLE_RADIUS,
            CIRCLE_COLOR,
            CIRCLE_INSIDE  # залитый круг
        )

    def draw_trajectory_line(self, frame) :
        for i in range(1, len(self.trajectory)):
            cv2.line(
                frame,
                self.trajectory[i - 1],
                self.trajectory[i],
                LINE_COORDINATES_COLOR,
                LINE_THICKNESS
            )

    def draw_coordinates_text(self, frame, center):
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

    def update_trajectory(self, center):
        if self.draw_trajectory:
            self.trajectory.append(center)
            if len(self.trajectory) > TRAJECTORY_LENGTH:
                self.trajectory.pop(0) #удаляет первый элемент

    def draw(self, frame, center):
        self.draw_point(frame, center)
        self.draw_coordinates_text(frame, center)
        if self.draw_trajectory:
            self.draw_trajectory_line(frame)

    def draw_period_text(self, frame, period):
        cv2.putText(
            frame,
            f"Period: {period:.3f} s",
            (X_POSITION_PERIOD, Y_POSITION_PERIOD),
            self.font,
            TEXT_PERIOD_SIZE,
            TEXT_PERIOD_COLOR,
            TEXT_PERIOD_THICKNESS
        )