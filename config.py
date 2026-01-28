# Configuration settings for SecureLock

# To configure email sending for OTP:
# 1. Use a Gmail account.
# 2. Enable 2-Step Verification in Google Account settings.
# 3. Generate an App Password: Go to Google Account > Security > App passwords > Generate for "Mail".
# 4. Replace the values below with your Gmail and the app password (not your regular password).
# 5. Restart the app.
# For other providers, update smtp_server and smtp_port accordingly.

EMAIL_SETTINGS = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 465,
    'sender_email': 'securel834@gmail.com',  # Replace with your Gmail address
    'sender_password': 'oyezuqneteqkbthy'   # Replace with 16-character app password
}
OTP_EXPIRY_SECONDS = 300  # OTP validity duration in seconds (5 minutes)