import sys
import os
import pytest

# Ensure the auth modules are visible to pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth.otp import send_otp, verify_otp
from auth.fingerprint import authenticate_fingerprint

# ---- OTP Tests ----

import auth.otp  # Import the whole module to modify internal state

def test_verify_otp_success(monkeypatch):
    """Should pass if correct OTP is entered."""
    auth.otp._otp_store['code'] = '123456'
    monkeypatch.setattr('builtins.input', lambda _: '123456')
    assert auth.otp.verify_otp() == True

def test_verify_otp_failure(monkeypatch):
    """Should fail if incorrect OTP is entered."""
    auth.otp._otp_store['code'] = '123456'
    monkeypatch.setattr('builtins.input', lambda _: '000000')
    assert auth.otp.verify_otp() == False


# ---- Fingerprint Tests ----

def test_authenticate_fingerprint_success(monkeypatch):
    """Should return True if fingerprint matches (simulated)."""
    monkeypatch.setattr('random.choice', lambda _: True)
    assert authenticate_fingerprint() is True

def test_authenticate_fingerprint_failure(monkeypatch):
    """Should return False if fingerprint does not match (simulated)."""
    monkeypatch.setattr('random.choice', lambda _: False)
    assert authenticate_fingerprint() is False

# ---- Facial Recognition Skipped ----

@pytest.mark.skip(reason="Requires webcam input and a known_face.jpg file")
def test_authenticate_face():
    from auth.facial import authenticate_face
    assert authenticate_face() in [True, False]
