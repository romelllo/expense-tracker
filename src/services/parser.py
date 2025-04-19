import re
from typing import Dict, Any, Optional
from datetime import datetime

def extract_payment_details(message: str) -> Dict[str, Any]:
    """Extract payment details from message text

    Args:
        message: The payment message text

    Returns:
        Dictionary with extracted details (amount, merchant)
    """
    amount_match = re.search(r'AED\s+(\d+\.?\d*)', message)
    merchant_match = re.search(r'done at ([^using]+)', message)

    amount = float(amount_match.group(1)) if amount_match else 0.0
    merchant = merchant_match.group(1).strip() if merchant_match else "Unknown"

    return {
        "amount": amount,
        "merchant": merchant,
        "message": message
    }

def convert_imessage_date(timestamp: int) -> Optional[datetime]:
    """Convert iMessage timestamp to Python datetime

    Args:
        timestamp: iMessage timestamp (nanoseconds since 2001-01-01)

    Returns:
        Python datetime object
    """
    if not timestamp:
        return None

    # iMessage uses nanoseconds since 2001-01-01
    # First, convert to seconds
    timestamp_seconds = timestamp / 1e9

    # Mac Absolute Time epoch starts at 2001-01-01
    # Unix epoch starts at 1970-01-01
    # The difference is 978307200 seconds
    unix_timestamp = timestamp_seconds + 978307200

    try:
        return datetime.fromtimestamp(unix_timestamp)
    except (OSError, ValueError, OverflowError) as e:
        # If the timestamp is still invalid, let's try a different approach
        # Some versions of iMessage may use a different epoch or format
        try:
            # Try interpreting as milliseconds since Unix epoch
            return datetime.fromtimestamp(timestamp / 1e6)
        except:
            # As a last resort, return current date
            print(f"Warning: Could not convert timestamp {timestamp}: {e}")
            return None
