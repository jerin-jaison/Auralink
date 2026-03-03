import logging

logger = logging.getLogger(__name__)

# OTP / Twilio integration has been removed.
# These stub functions are kept so existing imports do not break
# while the codebase is being cleaned up.

def send_otp(phone_number):
    """Stub: OTP sending removed."""
    return True, "ok"

def verify_otp(phone_number, code):
    """Stub: OTP verification removed."""
    return True, "ok"
