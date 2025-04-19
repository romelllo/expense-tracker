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
