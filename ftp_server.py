from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

class MyHandler(FTPHandler):
    pass

def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "password", ".", perm="elradfmw")
    
    handler = MyHandler
    handler.authorizer = authorizer
    
    server = FTPServer(("127.0.0.1", 2121), handler)
    server.serve_forever()

if __name__ == "__main__":
    start_ftp_server()