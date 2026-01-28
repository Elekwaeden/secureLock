from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add parent directory to path for imports
sys.path.append(os.path.dirname(BASE_DIR))

from auth.facial import authenticate_face
from auth.fingerprint import authenticate_fingerprint
from auth.otp import send_otp, verify_otp

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/authenticate/<method>")
def auth_page(method):
    return render_template("authenticate.html", method=method)

@app.route("/auth/<method>", methods=["POST"])
def auth_method(method):
    if method == "face":
        result = authenticate_face()
    elif method == "fingerprint":
        result = authenticate_fingerprint()
    elif method == "otp":
        email = request.form.get('email')
        if not email:
            return redirect(url_for("auth_page", method="otp"))
        success = send_otp(email)
        if success:
            session['otp_email'] = email
            return redirect(url_for("enter_otp"))
        else:
            return redirect(url_for("result", status="fail"))
    else:
        return jsonify({"status": "error", "message": "Invalid method"})

    if result:
        return redirect(url_for("result", status="success"))
    else:
        return redirect(url_for("result", status="fail"))

@app.route("/enter_otp", methods=["GET", "POST"])
def enter_otp():
    if request.method == "POST":
        email = session.get('otp_email')
        if not email:
            return redirect(url_for("auth_page", method="otp"))
        code = request.form.get('otp_code')
        if verify_otp(email, code):
            session.pop('otp_email', None)
            return redirect(url_for("result", status="success"))
        else:
            return render_template("enter_otp.html", error="Invalid or expired OTP")
    return render_template("enter_otp.html")

@app.route("/result/<status>")
def result(status):
    return render_template("result.html", status=status)

if __name__ == "__main__":
    app.run(debug=True)
