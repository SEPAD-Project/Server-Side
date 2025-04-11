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
        if not self.is_running():
            print(f"{self.file_path} is not running")
            return False
        
        try:
            self.process.kill()
            self.process.communicate()
            print(f"API stopped: {self.file_path}")
            return True
        except Exception as e:
            print(f"Stop error: {str(e)}")
            return False

    def restart(self):
        self.stop()
        return self.start()

    def is_running(self):
        return self.process and self.process.poll() is None

    def status(self):
        if self.is_running():
            return f"Running (PID: {self.process.pid})"
        return "Stopped"

def main():
    apps_config = [
        {"file": "api1.py"},
        {"file": "api2.py"},
        {"file": "api3.py"},
        {"file": "api4.py"}
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
            cmd = input("> ").lower().split()
            if not cmd:
                continue

            if cmd[0] == "exit":
                for app in apps:
                    app.stop()
                break

            elif cmd[0] == "status":
                for i, app in enumerate(apps, 1):
                    print(f"[API {i}] {app.file_path}")
                    print(f"  Status: {app.status()}")

            elif cmd[0] in ("start", "stop", "restart"):
                if len(cmd) < 2:
                    print("Missing API number!")
                    continue

                try:
                    index = int(cmd[1]) - 1
                    if index < 0 or index >= len(apps):
                        print("Invalid API number! Use 1-4")
                        continue

                    operation = getattr(apps[index], cmd[0])
                    operation()
                except ValueError:
                    print("Invalid number format!")

            else:
                print("Invalid command!")

        except KeyboardInterrupt:
            print("\nExiting...")
            for app in apps:
                app.stop()
            break

if __name__ == "__main__":
    main()