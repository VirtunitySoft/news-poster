import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

server : smtplib.SMTP_SSL = None

def load(smtp_server: str, smtp_port: int) -> None:
    """Load the SMTP server connection."""
    global server
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        print(f"SMTP server initialized at {smtp_server}:{smtp_port}.")
    except Exception as e:
        print(f"Failed to initialize SMTP server: {e}")
        server = None

def email(sender: str, password: str,receivers: list[str], subject: str, html_body: str) -> bool:
    """Send an email using the SMTP server."""
    if not server:
        print("SMTP server is not initialized.")
        return False

    try:
        # Login to the SMTP server
        server.login(sender, password)

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ", ".join(receivers)
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send the email
        server.sendmail(sender, receivers, msg.as_string())
        return True
    except Exception as e:
        return False