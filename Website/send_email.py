import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_styled_email(receiver, title, attachment_path=None):
    # Email configuration
    EMAIL_ADDRESS = "sepad.sender@gmail.com"
    EMAIL_PASSWORD = "pnxr nskb ohbk seap "
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver
    msg['Subject'] = title
    
    # Attach file if provided
    if attachment_path:
        try:
            # Open the file in binary mode
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            # Encode file in ASCII characters
            encoders.encode_base64(part)
            
            # Add header with filename
            filename = attachment_path.split("/")[-1]  # Get just the filename
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            msg.attach(part)
        except Exception as e:
            print(f"Error attaching file: {e}")
            return

    # Send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully to {receiver}!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # Usage example
    receiver = "parsasafaie.2568@gmail.com"
    attachment_file = "test.pdf"  # Path to file
    send_styled_email(receiver, 'Analytics Report', attachment_file)