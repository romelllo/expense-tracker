import os
import json
from typing import Dict, Any, List, Optional

class Config:
    """Configuration management"""

    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration

        Args:
            config_file: Path to config file
        """
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "db_path": "/Users/romannovikov/Library/Messages/chat.db",
            "data_file": "expenses.json"
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return default_config
        else:
            # Save default config
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config

    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()

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
        with open(self.data_file, 'w') as f:
            json.dump(expenses, f, indent=2)

    def load_expenses(self) -> List[Dict[str, Any]]:
        """Load expenses from file

        Returns:
            List of expense dictionaries
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
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
