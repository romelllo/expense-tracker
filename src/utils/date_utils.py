from datetime import datetime, timedelta
from typing import Optional

def get_date_threshold(days: int) -> datetime:
    """Get date threshold for filtering

    Args:
        days: Number of days back

    Returns:
        Datetime threshold
    """
    return datetime.now() - timedelta(days=days)

def format_date(date: Optional[datetime]) -> str:
    """Format date for display

    Args:
        date: Date to format

    Returns:
        Formatted date string
    """
    if not date:
        return "Unknown"

    return date.strftime("%Y-%m-%d %H:%M")

def convert_imessage_timestamp(timestamp: int) -> Optional[datetime]:
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
        return None
