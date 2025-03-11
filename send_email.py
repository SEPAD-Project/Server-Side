import smtplib
from email.message import EmailMessage


EMAIL_ADDRESS = "abolfazlrashidian94@gmail.com" 
EMAIL_PASSWORD = "xaom tzfe lkxx gvgc"   


def send_mail(subject, content, receiver):

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver
    msg.set_content(content)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  
            server.starttls() 
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print('EMAIL has been Sent')
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__name__":
    receiver_email = input('enter your email : ')
    send_mail('test', 'test content', receiver_email)