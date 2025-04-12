from flask import Flask, jsonify
import subprocess
import os
import sys
import time

app = Flask(__name__)

class FlaskAppManager:
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
        self.process = None
        self._check_file_exists()

    def _check_file_exists(self):
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"API file not found: {self.file_path}")

    def start(self):
        if self.is_running():
            return {'status': 'error', 'message': 'Already running'}
        
        try:
            self.process = subprocess.Popen(
                [sys.executable, self.file_path],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            time.sleep(2)
            return {'status': 'success', 'message': 'Started successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def stop(self):
        if not self.is_running():
            return {'status': 'error', 'message': 'Not running'}
        
        try:
            self.process.kill()
            self.process.communicate()
            return {'status': 'success', 'message': 'Stopped successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def restart(self):
        stop_result = self.stop()
        if stop_result['status'] == 'error':
            return stop_result
        return self.start()

    def is_running(self):
        return self.process and self.process.poll() is None

    def get_status(self):
        return 'running' if self.is_running() else 'stopped'

# Initialize managers for APIs
apps = [
    FlaskAppManager("api1.py"),
    FlaskAppManager("api2.py"),
    FlaskAppManager("api3.py"),
    FlaskAppManager("api4.py")
]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)