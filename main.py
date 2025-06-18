# Entry point for SecureLock
from auth.facial import authenticate_face
from auth.fingerprint import authenticate_fingerprint
from auth.otp import send_otp, verify_otp
from colorama import Fore, Style, init
import time
import os

init(autoreset=True)

def display_welcome():
    os.system('cls' if os.name == 'nt' else 'clear')

    banner = f"""
{Fore.CYAN}
   ╔════════════════════════════════════════╗
   ║                                        ║
   ║    🔐  W E L C O M E   T O   S E C U R E L O C K  🔐    ║
   ║                                        ║
   ╚════════════════════════════════════════╝
{Style.RESET_ALL}
    """

    tagline = f"{Fore.LIGHTWHITE_EX}Your digital gatekeeper. Choose your security method wisely."
    print(banner)
    print(tagline)
    time.sleep(1.5)

def main():
    display_welcome()

    print("\nPlease choose a second authentication method:")
    print("1. Facial Recognition 📷")
    print("2. Fingerprint Scan 🖐️")
    print("3. One-Time Password (OTP) 🔑\n")

    choice = input("Enter your choice (1/2/3): ").strip()
    ...


    print(f"{Fore.MAGENTA}\n🔄 Initializing authentication sequence...\n")
    time.sleep(1.2)

    authenticated = False

    if choice == "1":
        print(f"{Fore.CYAN}[Facial Recognition Selected] 📷 Starting facial recognition...\n")
        authenticated = authenticate_face()
    elif choice == "2":
        print(f"{Fore.CYAN}[Fingerprint Scan Selected] ✋ Initiating fingerprint scan...\n")
        authenticated = authenticate_fingerprint()
    elif choice == "3":
        print(f"{Fore.CYAN}[OTP Selected] 🔑 Generating your One-Time Password...\n")
        send_otp()
        authenticated = verify_otp()
    else:
        print(f"{Fore.RED}❌ Invalid choice. Please restart the program.")
        return

    time.sleep(1)

    if authenticated:
        print(f"{Fore.GREEN}\n✅ Access granted. Welcome aboard!")
    else:
        print(f"{Fore.RED}\n❌ Authentication failed. Please try again.")

if __name__ == "__main__":
    main()

# This code serves as the main entry point for the SecureLock application.
# It prompts the user to select a second authentication method and processes the choice.
# The authentication methods are imported from their respective modules.
# The user can choose between facial recognition, fingerprint scan, or OTP verification.
# The program will then authenticate the user based on their choice and provide feedback.
# If authentication is successful, the user can proceed; otherwise, access is denied.
# The code is structured to allow for easy expansion with additional authentication methods in the future.
# The main function orchestrates the flow of the application, ensuring a user-friendly experience.
# The code is designed to be modular, with each authentication method handled in its own module.
# This modular approach allows for easy maintenance and updates to individual authentication methods.
# The program is intended to be run in a secure environment where user data is handled responsibly.
# The SecureLock application is a simple yet effective way to enhance security through multiple authentication methods.