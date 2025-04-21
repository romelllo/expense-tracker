import json
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration management using environment variables"""

    def __init__(self):
        """Initialize configuration from environment variables"""
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables with defaults"""
        return {
            # Get values from environment variables or use defaults
            "db_path": os.environ.get("EXPENSE_TRACKER_DB_PATH"),
            "data_file": os.environ.get("EXPENSE_TRACKER_DATA_FILE",
                "expenses.json"),
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

class ExpenseStore:
    """Store for persisting categorized expenses"""

    def __init__(self, data_file: str = "expenses.json"):
        """Initialize expense store

        Args:
            data_file: Path to data file
        """
        self.data_file = data_file

    def save_expenses(self, expenses: List[Dict[str, Any]]):
        """Save expenses to file

        Args:
            expenses: List of expense dictionaries
        """
        with open(self.data_file, "w") as f:
            json.dump(expenses, f, indent=2)

    def load_expenses(self) -> List[Dict[str, Any]]:
        """Load expenses from file

        Returns:
            List of expense dictionaries
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file) as f:
                    return json.load(f)
            except:
                return []
        return []

    def update_expense_category(self, index: int, category: str) -> Optional[Dict[str, Any]]:
        """Update category for a specific expense

        Args:
            index: Index of expense to update
            category: New category

        Returns:
            Updated expense or None if index is invalid
        """
        expenses = self.load_expenses()

        if 0 <= index < len(expenses):
            expenses[index]["category"] = category
            self.save_expenses(expenses)
            return expenses[index]

        return None
