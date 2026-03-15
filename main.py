import sys
import os

from my_lib.constants import VIDEO_PATH
from my_lib.app import PendulumTrackerApp


def main():
    app = PendulumTrackerApp(VIDEO_PATH)
    app.run()

if __name__ == "__main__":
    main()