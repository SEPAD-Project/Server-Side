import time

BASE_PATH = "C://sap-project//log.txt"

def log_message(message, filename=BASE_PATH):
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a') as file:
        file.write(f"[{formatted_time}] {message}\n")

if __name__ == '__main__':
    log_message('this is test log')