# Entry point for SecureLock Web Interface
from interface.app import app
import webbrowser
import threading
import time

def open_browser():
    time.sleep(1)  # Wait for server to start
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    # Open browser automatically
    threading.Thread(target=open_browser).start()
    # Run the Flask app
    app.run(debug=True)