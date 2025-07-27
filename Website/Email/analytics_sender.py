import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_analytics_email(receiver, subject, pdf_bytes, filename="report.pdf"):
    """
    Send an email with an in-memory PDF attachment.

    Args:
        receiver (str): Recipient email address.
        subject (str): Email subject.
        pdf_bytes (bytes): PDF file content in bytes.
        filename (str): Filename to appear in the email attachment.
    """
    EMAIL_ADDRESS = "sepad.sender@gmail.com"
    EMAIL_PASSWORD = "pnxr nskb ohbk seap"

    # Create email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver
    msg["Subject"] = subject

    # Attach PDF
    part = MIMEApplication(pdf_bytes, _subtype="pdf")
    part.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(part)

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {receiver}")
    except Exception as e:
        print(f"Failed to send email: {e}")
