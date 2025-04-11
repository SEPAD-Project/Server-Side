import subprocess
import os
import sys
import time

class FlaskAppManager:
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)

        self.process = None
        self._check_file_exists()

    def _check_file_exists(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def is_running(self):
        pass

    def status(self):
        pass

def main():
    apps_config = [
    ]

    apps = [
        FlaskAppManager(
            cfg["file"],
        ) for cfg in apps_config
    ]

    print("Windows Flask API Manager")
    print("Commands: start <1-4>, stop <1-4>, restart <1-4>, status, exit")

    while True:
        try:
            pass

        except KeyboardInterrupt:
            print("\nExiting...")
            for app in apps:
                app.stop()
            break

if __name__ == "__main__":
    main()