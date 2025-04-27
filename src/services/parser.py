import re
from datetime import datetime
from typing import Any, Dict, Optional


def extract_payment_details(message: str) -> Dict[str, Any]:
    """Extract payment details from message text

    Args:
        message: The payment message text

    Returns:
        Dictionary with extracted details (amount, merchant, direction)
    """
    result = {"amount": 0.0, "merchant": "Unknown", "message": message, "is_income": False}

    # Handle payment messages
    if "Payment of AED" in message:
        # Extract the amount
        amount_match = re.search(r"Payment of AED\s+(\d+\.?\d*)", message)

        # Extract the merchant more reliably with lookahead and lookbehind
        merchant_match = re.search(r"done at (.*?)(?= using| with|$)", message)

        if amount_match:
            result["amount"] = float(amount_match.group(1))

        if merchant_match:
            result["merchant"] = merchant_match.group(1).strip()

    # Handle incoming transfer messages
    elif "AED" in message and ("sent by" in message or "has been credited" in message):
        amount_match = re.search(r"AED\s+([0-9,]+\.?\d*)", message)
        sender_match = re.search(r"sent by ([^and]+?)(?:and|$)", message)

        if amount_match:
            # Remove commas in numbers like 1,000
            amount_str = amount_match.group(1).replace(",", "")
            result["amount"] = float(amount_str)
            result["is_income"] = True

        if sender_match:
            result["merchant"] = f"Transfer from {sender_match.group(1).strip()}"
        else:
            result["merchant"] = "Incoming Transfer"

    # Handle outgoing transfer messages
    elif "Your local transfer of AED" in message:
        amount_match = re.search(r"transfer of AED\s+([0-9,]+\.?\d*)", message)
        recipient_match = re.search(r"to (.*?)(?= from|$)", message)

        if amount_match:
            # Remove commas in numbers like 1,000
            amount_str = amount_match.group(1).replace(",", "")
            result["amount"] = float(amount_str)

        if recipient_match:
            result["merchant"] = f"Transfer to {recipient_match.group(1).strip()}"
        else:
            result["merchant"] = "Outgoing Transfer"

    # Handle refund messages
    elif "refunded" in message and "AED" in message:
        amount_match = re.search(r"AED\s+([0-9,]+\.?\d*)", message)
        source_match = re.search(r"from (.*?)(?= has| to|$)", message)

        if amount_match:
            # Remove commas in numbers like 1,000
            amount_str = amount_match.group(1).replace(",", "")
            result["amount"] = float(amount_str)
            result["is_income"] = True

        if source_match:
            result["merchant"] = f"Refund from {source_match.group(1).strip()}"
        else:
            result["merchant"] = "Refund"

    # For debugging - log any issues with extraction
    if result["merchant"] == "Unknown" and "Payment" in message:
        print(f"Warning: Could not extract merchant from: {message}")

    return result


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
