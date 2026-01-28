# OTP generation and verification

import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from config import EMAIL_SETTINGS, OTP_EXPIRY_SECONDS

# In-memory store (ideally should be secure in production)
_otp_store = {}  # key: email, value: {'code': str, 'expiry': timestamp}

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    expiry = time.time() + OTP_EXPIRY_SECONDS
    _otp_store[email] = {'code': otp, 'expiry': expiry}
    
    # Send email
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SETTINGS['sender_email']
        msg['To'] = email
        msg['Subject'] = 'Your One-Time Password for SecureLock'
        
        body = f"Your One-Time Password is: {otp}\n\nIt will expire in 5 minutes."
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP_SSL(EMAIL_SETTINGS['smtp_server'], EMAIL_SETTINGS['smtp_port'], timeout=10)
        server.login(EMAIL_SETTINGS['sender_email'], EMAIL_SETTINGS['sender_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_SETTINGS['sender_email'], email, text)
        server.quit()
        print(f"OTP sent to {email}")
        return True
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        return False

def verify_otp(email, entered_code):
    if email not in _otp_store:
        return False
    
    stored = _otp_store[email]
    if time.time() > stored['expiry']:
        del _otp_store[email]
        return False
    
    if entered_code == stored['code']:
        del _otp_store[email]
        return True
    else:
        return False