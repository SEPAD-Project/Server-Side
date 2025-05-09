from ftplib import FTP

def upload_file(ftp, file_path, school_code, class_name, national_code):
    try:
        filename = f"{school_code}_{class_name}_{national_code}.{str(file_path).split('.')[-1]}"

        # uploading file
        with open(file_path, 'rb') as file:
            ftp.storbinary(f'STOR {filename}', file)
        
        print(f"File {filename} uploaded successfully.")
    except Exception as e:
        print(f"Error uploading file: {e}")

def connect_and_upload(file_path, school_name, class_name, national_code):
    try:
        # connect to ftp server
        ftp = FTP()
        ftp.connect("127.0.0.1", 2121)
        ftp.login("user", "password")
        
        str(file_path)
        upload_file(ftp, str(file_path), str(school_name), str(class_name), str(national_code))
        

        ftp.quit()
    except Exception as e:
        print(f"Error occured while connecting or uploading: {e}")

if __name__ == "__main__":
    connect_and_upload(r'C:\Users\#AR\Desktop\Screenshot.png',
                       123, 1052, 929599999)