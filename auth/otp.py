# OTP generation and verification

import random
import time

# Global storage (simulate session memory)
otp_store = {
    "otp": None,
    "expiry": None
}

def generate_otp(length=6):
    """Generate a numeric OTP of specified length"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp():
    """Simulate sending OTP to user (print to console)"""
    otp = generate_otp()
    expiry_time = time.time() + 300  # OTP valid for 5 minutes (300 seconds)

    otp_store["otp"] = otp
    otp_store["expiry"] = expiry_time

    print(f"[OTP] Your One-Time Password is: {otp}")
    print("(It will expire in 5 minutes.)")

def verify_otp():
    """Verify the user-input OTP"""
    if otp_store["otp"] is None:
        print("❌ No OTP was generated.")
        return False

    if time.time() > otp_store["expiry"]:
        print("❌ OTP has expired.")
        return False

    user_input = input("Enter the OTP you received: ").strip()

    if user_input == otp_store["otp"]:
        print("✅ OTP verified successfully.")
        return True
    else:
        print("❌ Incorrect OTP.")
        return False
