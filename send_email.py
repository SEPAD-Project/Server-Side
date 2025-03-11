
import smtplib
from email.message import EmailMessage


EMAIL_ADDRESS = "abolfazlrashidian94@gmail.com" 
EMAIL_PASSWORD = ""   


receiver_email = input('enter your email : ')


msg = EmailMessage()
msg["Subject"] = "test subject"
msg["From"] = EMAIL_ADDRESS
msg["To"] = receiver_email
msg.set_content("test mail")

try:

    with smtplib.SMTP("smtp.example.com", 587) as server:  #
        server.starttls() 
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
    print('sended ')
except Exception as e:
    print(f"Error {e}")