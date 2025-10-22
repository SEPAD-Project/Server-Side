from ftplib import FTP
import os

def upload_to_ftp(host, port, username, password, local_file_path, remote_file_name=None):
    """
    Upload file to FTP server
    
    Parameters:
    host: server address
    port: server port
    username: username
    password: password
    local_file_path: local file path
    remote_file_name: remote file name (optional)
    """
    
    if remote_file_name is None:
        remote_file_name = os.path.basename(local_file_path)
    
    try:
        # Connect to FTP server
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(username, password)
        
        print(f"Successfully connected to {host}:{port}")
        
        # Upload file
        with open(local_file_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_file_name}', file)
        
        print(f"File {local_file_path} uploaded successfully as {remote_file_name}")
        
        # Close connection
        ftp.quit()
        return True
        
    except Exception as e:
        print(f"Upload error: {e}")
        return False

# Usage example
if __name__ == "__main__":
    # Your FTP server details
    HOST = "185.4.21.110"
    PORT = 2121
    USERNAME = "user"
    PASSWORD = "password"
    LOCAL_FILE = "x.txt"  # Change this to your file path
    
    upload_to_ftp(HOST, PORT, USERNAME, PASSWORD, LOCAL_FILE)