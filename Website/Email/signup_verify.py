import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def verify_code_sender(receiver, title, html_content=None):
    # Email configuration
    EMAIL_ADDRESS = "sepad.sender@gmail.com"
    EMAIL_PASSWORD = "pnxr nskb ohbk seap"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver
    msg['Subject'] = title
    
    # Attach HTML content if provided
    if html_content:
        msg.attach(MIMEText(html_content, 'html'))
    else:
        msg.attach(MIMEText("No HTML content provided", 'plain'))

    # Send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully to {receiver}!")
        return True, f"Email sent successfully to {receiver}!"
    except Exception as e:
        error_msg = f"Error sending email: {e}"
        print(error_msg)
        return False, error_msg

if __name__ == "__main__":
    # Example usage with HTML content
    receiver = "parsasafaie.2568@gmail.com"
    
    # HTML content example
    html_content = """
    <html>
        <body>
            <h1 style="color: #0066cc;">Hello!</h1>
            <p>This is a test<p>
        </body>
    </html>
    """
    
    verify_code_sender(receiver=receiver, title='Verify your email', html_content=html_content)