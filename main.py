# Entry point for SecureLock

from auth.facial import authenticate_face
from auth.fingerprint import authenticate_fingerprint
from auth.otp import send_otp, verify_otp

def main():
    print("=== Welcome to SecureLock ===")
    print("Please choose a second authentication method:")
    print("1. Facial Recognition")
    print("2. Fingerprint Scan")
    print("3. One-Time Password (OTP)\n")
    
    choice = input("Enter your choice (1/2/3): ").strip()

    authenticated = False

    if choice == "1":
        print("\n[Facial Recognition Selected]")
        authenticated = authenticate_face()
    elif choice == "2":
        print("\n[Fingerprint Scan Selected]")
        authenticated = authenticate_fingerprint()
    elif choice == "3":
        print("\n[OTP Verification Selected]")
        send_otp()
        authenticated = verify_otp()
    else:
        print("Invalid choice. Please restart the program.")

    if authenticated:
        print("\n✅ Access granted. You may now continue securely.")
        # TODO: Add optional functionality here (e.g., file/text processing)
    else:
        print("\n❌ Authentication failed. Access denied.")

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