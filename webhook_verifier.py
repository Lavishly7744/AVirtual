import hmac
import hashlib
import time

# Secret for HMAC signature
WEBHOOK_SECRET = "my_am3x_shared_secret"

# Returns True if signature and timestamp match
def verify_webhook(payload: str, timestamp: str, received_sig: str) -> bool:
    try:
        # Check timestamp freshness (max 5 min = 300s)
        now = int(time.time())
        if abs(now - int(timestamp)) > 300:
            return False

        # Recalculate signature
        base_string = f"{timestamp}.{payload}"
        expected_sig = hmac.new(
            WEBHOOK_SECRET.encode(),
            base_string.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_sig, received_sig)
    except Exception:
        return False
