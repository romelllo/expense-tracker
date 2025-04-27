import logging
import sqlite3
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MessageDatabase:
    """Data source for accessing iMessage database"""

    def __init__(self, db_path: str):
        """Initialize database connection"""
        self.db_path = db_path

    def fetch_payment_messages(self, days: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch payment messages from the database

        Args:
            days: Optional number of days to limit the search

        Returns:
            List of dictionaries with message text and date
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Query to capture all relevant payment patterns
            query = """
            SELECT text, date FROM message
            WHERE (
                text LIKE '%Payment of AED%' OR
                text LIKE '%Your local transfer of AED%' OR
                text LIKE '%AED% sent by%' OR
                text LIKE '%AED% from% has been refunded%'
            )
            """

            params = []

            if days:
                # Convert days to iMessage timestamp format (Mac Absolute Time)

                # Current time in seconds since Unix epoch
                current_time_unix = time.time()

                # Convert to Mac epoch (seconds since 2001-01-01)
                mac_epoch_diff = 978307200  # Seconds between Unix epoch and Mac epoch
                current_time_mac = current_time_unix - mac_epoch_diff

                # Calculate cutoff time in seconds
                cutoff_time_mac = current_time_mac - (days * 86400)  # 86400 seconds in a day

                # Convert to nanoseconds for iMessage database
                cutoff_time_ns = int(cutoff_time_mac * 1e9)

                # Add to query with parameter
                query += " AND date > ?"
                params.append(cutoff_time_ns)

            # Sort by date descending to get newest messages first
            query += " ORDER BY date DESC"

            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()

            return [{"text": text, "date": date} for text, date in results]

        except Exception as e:
            logger.error(f"Database error: {e}")
            return []
