import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_html_email(theme='light'):
    """Generate HTML content with specified theme (light/dark)"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        :root {{
            --primary-color: { '#3498db' if theme == 'light' else '#2ecc71' };
            --hover-scale: 1.05;
        }}

        body {{
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', system-ui;
            background: {'linear-gradient(135deg, #f8f9fa, #e9ecef)' if theme == 'light' 
                        else 'linear-gradient(135deg, #2c3e50, #34495e)'};
            min-height: 100vh;
        }}

        .container {{
            max-width: 600px;
            margin: 40px auto;
            padding: 40px;
            background: {'#ffffff' if theme == 'light' else '#2c3e50'};
            border-radius: 16px;
            box-shadow: 0 8px 30px { 'rgba(0,0,0,0.1)' if theme == 'light' 
                                   else 'rgba(0,0,0,0.3)' };
            transition: transform 0.3s ease;
        }}

        .container:hover {{
            transform: translateY(-5px);
        }}

        h1 {{
            color: {'#2c3e50' if theme == 'light' else '#ecf0f1'};
            text-align: center;
            font-size: 2.4em;
            margin-bottom: 30px;
        }}

        .content {{
            line-height: 1.6;
            color: {'#7f8c8d' if theme == 'light' else '#bdc3c7'};
            font-size: 16px;
        }}

        .button-container {{
            display: flex;
            justify-content: center;
            margin: 30px 0;
        }}

        .cta-button {{
            padding: 15px 40px;
            background: var(--primary-color);
            color: white !important;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-block;
            border: none;
            cursor: pointer;
        }}

        .cta-button:hover {{
            transform: scale(var(--hover-scale));
            box-shadow: 0 5px 15px { 'rgba(52, 152, 219, 0.3)' if theme == 'light' 
                                    else 'rgba(46, 204, 113, 0.3)' };
        }}

        .features {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin: 30px 0;
        }}

        .feature-card {{
            padding: 20px;
            background: {'#f8f9fa' if theme == 'light' else '#34495e'};
            border-radius: 8px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to Our Platform</h1>
        
        <div class="content">
            <p>Discover amazing features and enhance your experience with our premium services.</p>
            
            <div class="features">
                <div class="feature-card">
                    <h3>🚀 Fast Performance</h3>
                    <p>Lightning-fast loading times and smooth operations</p>
                </div>
                <div class="feature-card">
                    <h3>🔒 Secure Storage</h3>
                    <p>Military-grade encryption for your data</p>
                </div>
            </div>
        </div>

        <div class="button-container">
            <a href="#" class="cta-button">Get Started Now</a>
        </div>
    </div>
</body>
</html>
"""

def send_styled_email(theme, RECEIVER_EMAIL):
    # Email configuration
    EMAIL_ADDRESS = "abolfazlrashidian94@gmail.com" 
    EMAIL_PASSWORD = "xaom tzfe lkxx gvgc"   


    # Create message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"Styled Email ({theme.capitalize()} Theme)"

    # Generate HTML content
    html_content = generate_html_email(theme)
    msg.attach(MIMEText(html_content, 'html'))

    # Send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully with {theme} theme!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__" :
    # Usage example
    receiver = input('enter email : ')
    receiver =  "crax6ix@gmail.com"
    send_styled_email('light', receiver)  # Change to 'light' for light theme
