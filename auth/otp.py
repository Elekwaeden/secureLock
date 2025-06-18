# OTP generation and verification

import random
from colorama import Fore
import time

# In-memory store (ideally should be secure in production)
_otp_store = {}

def send_otp():
    otp = str(random.randint(100000, 999999))
    _otp_store['code'] = otp
    print(f"{Fore.YELLOW}[OTP] Your One-Time Password is: {otp}")
    print(f"{Fore.CYAN}(It will expire in 5 minutes.)")
    time.sleep(1.5)

def verify_otp():
    entered = input(f"\n{Fore.BLUE}Enter the OTP: ").strip()
    expected = _otp_store.get('code')
    
    if entered == expected:
        print(f"{Fore.GREEN}✅ OTP verified successfully.")
        return True
    else:
        print(f"{Fore.RED}❌ Incorrect OTP.")
        return False
