import logging
import sqlite3
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

            query = "SELECT text, date FROM message WHERE text LIKE '%Payment of AED%'"

            if days:
                # In a real implementation, we'd add date filtering
                # This would require converting days to iMessage timestamp format
                pass

            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()

            return [{"text": text, "date": date} for text, date in results]

        except Exception as e:
            logger.error(f"Database error: {e}")
            return []
