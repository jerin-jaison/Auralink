import logging
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)

def get_twilio_client():
    """Get authenticated Twilio client."""
    if settings.TWILIO_API_KEY_SID and settings.TWILIO_API_KEY_SECRET:
        return Client(settings.TWILIO_API_KEY_SID, settings.TWILIO_API_KEY_SECRET, account_sid=settings.TWILIO_ACCOUNT_SID)

    if not settings.TWILIO_ACCOUNT_SID:
        logger.error("Twilio Error: TWILIO_ACCOUNT_SID is missing in settings.")
        return None
    if not settings.TWILIO_AUTH_TOKEN:
        logger.error("Twilio Error: TWILIO_AUTH_TOKEN is missing in settings.")
        return None
        
    return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_twilio_otp(phone_number):
    """
    TEMPORARY: OTP System Disabled.
    Returns (success, message)
    """
    # Temporarily bypassed as per request
    return True, "pending"

    # if settings.DEBUG:
    #     print(f"\n========================================")
    #     print(f" DEBUG ONLY: OTP for {phone_number} is 123456")
    #     print(f"========================================\n")
    #     return True, "pending"

    # client = get_twilio_client()
    # if not client:
    #     return False, "SMS service not configured."
    
    # try:
    #     verification = client.verify \
    #         .v2 \
    #         .services(settings.TWILIO_VERIFY_SERVICE_SID) \
    #         .verifications \
    #         .create(to=phone_number, channel='sms')
        
    #     return True, verification.status
    # except TwilioRestException as e:
    #     logger.error(f"Twilio Send Error: {e}")
    #     return False, str(e.msg)
    # except Exception as e:
    #     logger.error(f"Error sending OTP: {e}")
    #     return False, "Failed to send OTP."

def verify_twilio_otp(phone_number, code):
    """
    TEMPORARY: OTP System Disabled.
    Returns (success, message)
    """
    # Temporarily bypassed as per request
    return True, "Verification successful."

    # if settings.DEBUG and str(code) == '123456':
    #     return True, "Verification successful."

    # client = get_twilio_client()
    # if not client:
    #     return False, "SMS service not configured."
    
    # try:
    #     verification_check = client.verify \
    #         .v2 \
    #         .services(settings.TWILIO_VERIFY_SERVICE_SID) \
    #         .verification_checks \
    #         .create(to=phone_number, code=code)
        
    #     if verification_check.status == 'approved':
    #         return True, "Verification successful."
    #     else:
    #         return False, "Invalid or expired code."
            
    # except TwilioRestException as e:
    #     logger.error(f"Twilio Verify Error: {e}")
    #     return False, str(e.msg)
    # except Exception as e:
    #     logger.error(f"Error verifying OTP: {e}")
    #     return False, "Failed to verify OTP."
