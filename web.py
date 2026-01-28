from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add parent directory to path for imports
sys.path.append(BASE_DIR)

from auth.facial import authenticate_face
from auth.fingerprint import authenticate_fingerprint
from auth.otp import send_otp, verify_otp

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "interface", "templates"),
    static_folder=os.path.join(BASE_DIR, "interface", "static")
)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/manifest.json")
def manifest():
    manifest_data = {
        "name": "SecureLock - Multi-Factor Authentication",
        "short_name": "SecureLock",
        "description": "Advanced biometric and OTP authentication system featuring facial recognition, fingerprint scanning, and one-time passwords",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait-primary",
        "background_color": "#0a0a0a",
        "theme_color": "#00ffff",
        "icons": [
            {
                "src": "https://cdn.jsdelivr.net/npm/twemoji@14.0.2/dist/twemoji.min.js",
                "sizes": "192x192",
                "type": "application/javascript",
                "purpose": "any"
            },
            {
                "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'><circle cx='256' cy='256' r='240' fill='%2300ffff' opacity='0.1'/><path d='M256 80c-47 0-85 38-85 85v20h170v-20c0-47-38-85-85-85zm-95 125h190v140c0 26-21 47-47 47H208c-26 0-47-21-47-47v-140z' fill='%2300ffff'/></svg>",
                "sizes": "512x512",
                "type": "image/svg+xml",
                "purpose": "any"
            }
        ],
        "categories": ["security", "productivity"]
    }
    return jsonify(manifest_data)

@app.route("/sw.js")
def service_worker():
    """Serve service worker from root to ensure correct scope"""
    import mimetypes
    with open(os.path.join(BASE_DIR, "interface", "static", "js", "sw.js"), "r") as f:
        content = f.read()
    # Return with correct content-type
    from flask import Response
    return Response(content, mimetype="application/javascript", headers={
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Service-Worker-Allowed": "/"
    })

@app.route("/favicon.ico")
def favicon():
    """Serve favicon to prevent 404"""
    return "", 204  # No content

@app.route("/health")
def health():
    return jsonify({"status": "SecureLock web interface running"})

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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False) 
