from flask import Flask, jsonify, render_template, request
import subprocess
import os
import sys
import time
from configparser import ConfigParser
from pathlib import Path
from flask_cors import CORS
import psutil

config_path = os.path.join('../config.ini')
config = ConfigParser()
config.read(config_path)

port = int(config['ControlServer']['control_server_port'])
api1 = config['ControlServer']['api1']
api2 = config['ControlServer']['api2']
api3 = config['ControlServer']['api3']
api4 = config['ControlServer']['api4']

LOG_DIR = os.path.join('../', 'apis', 'api_logs')

app = Flask(__name__)
CORS(app)

class FlaskAppManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_path = os.path.abspath("../"+str(file_path))
        self.process = None
        self._check_file_exists()

    def _check_file_exists(self):
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"API file not found: {self.file_path}")

    def start(self, message='Started successfully'):
        if self.is_running():
            return {'status': 'error', 'message': 'Already running'}
        
        try:
            self.process = subprocess.Popen(
                [sys.executable, self.file_path],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            time.sleep(2)
            return {'status': 'success', 'message': message}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def stop(self):
        if not self.is_running():
            return {'status': 'error', 'message': 'Not running'}
        
        try:
            self.process.kill()
            self.process.communicate()
            return {'status': 'success', 'message': 'Stopped Successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def restart(self):
        stop_result = self.stop()
        if stop_result['status'] == 'error':
            return stop_result
        return self.start(message='RESTARTED Successfully')

    def is_running(self):
        return self.process and self.process.poll() is None

    def get_status(self):
        return 'running' if self.is_running() else 'stopped'

# Initialize managers for APIs
apps = [
    FlaskAppManager(Path(api1)),
    FlaskAppManager(Path(api2)),
    FlaskAppManager(Path(api3)),
    FlaskAppManager(Path(api4))
]

@app.route('/start/<int:api_number>', methods=['POST', 'GET'])
def start_api(api_number):
    if 1 <= api_number <= 4:
        result = apps[api_number-1].start()
        return jsonify(result)
    return jsonify({'status': 'error', 'message': 'Invalid API number'})

@app.route('/stop/<int:api_number>', methods=['POST', 'GET'])
def stop_api(api_number):
    if 1 <= api_number <= 4:
        result = apps[api_number-1].stop()
        return jsonify(result)
    return jsonify({'status': 'error', 'message': 'Invalid API number'})

@app.route('/restart/<int:api_number>', methods=['POST', 'GET'])
def restart_api(api_number):
    if 1 <= api_number <= 4:
        result = apps[api_number-1].restart()
        return jsonify(result)
    return jsonify({'status': 'error', 'message': 'Invalid API number'})

@app.route('/status', methods=['GET'])
def status():
    status_report = {}
    for i, manager in enumerate(apps, 1):
        status_report[f'api{i}'] = {
            'file': manager.file_path,
            'status': manager.get_status(),
            'pid': manager.process.pid if manager.process else None
        }
    return jsonify(status_report)

@app.route('/metrics')
def get_metrics():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    return jsonify({
        'cpu': round(cpu, 1),
        'memory': round(mem, 1),
        'disk': round(disk, 1),
        'network': round(net / 1024 / 1024, 2)
    })

@app.route('/get_api_logs', methods=['GET'])
def get_api_logs():
    # get api number
    api_number = request.args.get('api_number')
    
    if not api_number:
        return jsonify({
            'success': False,
            'api_number': None,
            'message': 'API number is required'
        }), 400
    
    # log file name
    log_file = os.path.join(LOG_DIR, f'api{api_number}_log.txt')
    
    # check file exists
    if not os.path.exists(log_file):
        return jsonify({
            'success': False,
            'api_number': api_number,
            'message': f'Log file for API {api_number} not found'
        }), 404
    
    try:
        # read fils
        with open(log_file, 'r') as f:
            content = f.read()
        
        # clean file content
        with open(log_file, 'w') as f:
            f.write('')
        
        # return success message
        return jsonify({
            'success': True,
            'api_number': api_number,
            'message': content
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'api_number': api_number,
            'message': f'Error processing log file: {str(e)}'
        }), 500

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)