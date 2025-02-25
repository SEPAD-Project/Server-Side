from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

class MyHandler(FTPHandler):
    def on_file_received(self, file):
        try:
            # getting recived file path
            file_path = os.path.abspath(file)
            
            # extracting school code, class name, national code from filename
            filename = os.path.basename(file_path)
            filename, suffix = str(filename).split('.')
            school_code, class_name, national_code = filename.split('_')[:3]
            
            # creating school directory if not exist
            school_dir = os.path.join(os.getcwd(), school_code)
            if not os.path.exists(school_dir):
                os.makedirs(school_dir)
            
            # creating class directory if not exist 
            class_dir = os.path.join(school_dir, class_name)
            if not os.path.exists(class_dir):
                os.makedirs(class_dir)
            
            # moving to class directory
            new_file_path = os.path.join(class_dir, f"{national_code}.{suffix}")
            if not os.path.exists(new_file_path):
                os.rename(file_path, new_file_path)
            else:
                os.replace(file_path, new_file_path)

            print(f"File <{filename}> uploaded successfully to <{new_file_path}>")
        except Exception as e:
            print(f"Error occured while uploaded file: {e}")

def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "password", ".", perm="elradfmw")
    
    handler = MyHandler
    handler.authorizer = authorizer
    
    server = FTPServer(("127.0.0.1", 2121), handler)
    server.serve_forever()

if __name__ == "__main__":
    start_ftp_server()