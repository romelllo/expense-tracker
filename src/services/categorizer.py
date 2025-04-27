import json
import os
import re
from typing import Dict, List, Tuple


class ExpenseCategorizer:
    """Categorizes expenses based on merchant names"""

    def __init__(self, config_path: str = None):
        """Initialize with categories from config file or default categories

        Args:
            config_path: Path to categories.json configuration file
        """
        self.categories: Dict[str, List[str]] = {}
        self.config_path = config_path

        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    self.categories = json.load(f)
                # Normalize all category keywords to lowercase for case-insensitive matching
                self._normalize_categories()
            except Exception as e:
                print(f"Error loading categories from {config_path}: {e}")
                self._init_default_categories()
        else:
            self._init_default_categories()

    def _normalize_categories(self):
        """Convert all category keywords to lowercase for case-insensitive matching"""
        normalized = {}
        for category, keywords in self.categories.items():
            normalized[category] = [kw.lower() for kw in keywords]
        self.categories = normalized

    def _init_default_categories(self):
        """Initialize with default categories if config file not available"""
        self.categories = {
            "grocery": ["carrefour", "al maya", "spinneys", "waitrose", "viva", "supermarket"],
            "restaurant": ["restaurant", "cafe", "food", "gastronomy", "thai", "hanoi"],
            "entertainment": ["cinema", "movie", "theatre", "event", "concert", "game", "louvre"],
            "transport": ["careem", "uber", "taxi", "rta", "metro", "bus", "petrol", "gas", "fuel"],
            "clothes": [
                "h&m",
                "apparel",
                "fashion",
                "zara",
                "clothing",
                "shoes",
                "dress",
                "wear",
                "thrift",
            ],
            "services": ["apple", "virgin mobile"],
            "other": [],  # Default category
        }
        self._normalize_categories()

    def save_categories(self, config_path: str = None) -> bool:
        """Save current categories to a JSON file

        Args:
            config_path: Path where to save the configuration

        Returns:
            Success status of the save operation
        """
        save_path = config_path or self.config_path
        if not save_path:
            print("Error: No config path specified for saving categories")
            return False

        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, "w") as f:
                json.dump(self.categories, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving categories to {save_path}: {e}")
            return False

    def categorize(self, merchant: str) -> str:
        """Categorize a merchant based on keywords

        Args:
            merchant: The merchant name

        Returns:
            Category name
        """
        if not merchant or merchant == "Unknown":
            return "other"

        merchant_lower = merchant.lower()
        best_match = "other"
        best_match_score = 0

        # Try different matching strategies, looking for the best match
        for category, keywords in self.categories.items():
            for keyword in keywords:
                # Skip empty keywords
                if not keyword:
                    continue

                # Exact match has highest priority
                if keyword == merchant_lower:
                    return category

                # Contained as whole word
                if re.search(r"\b" + re.escape(keyword) + r"\b", merchant_lower):
                    # Longer keyword = better match
                    if len(keyword) > best_match_score:
                        best_match = category
                        best_match_score = len(keyword)

                # Simple contains match (less priority than word boundary match)
                elif keyword in merchant_lower and len(keyword) > best_match_score:
                    best_match = category
                    best_match_score = len(keyword)

        # Debug output if needed
        # if merchant_lower != "unknown" and best_match == "other":
        #     print(f"Could not categorize merchant: '{merchant_lower}'")

        return best_match

    def add_keyword(self, category: str, keyword: str) -> None:
        """Add a new keyword to a category

        Args:
            category: Category name
            keyword: Keyword to add
        """
        if category in self.categories:
            # Normalize keyword to lowercase and avoid duplicates
            keyword_lower = keyword.lower()
            if keyword_lower not in self.categories[category]:
                self.categories[category].append(keyword_lower)

    def add_category(self, category: str, keywords: List[str] = None) -> None:
        """Add a new category with optional keywords

        Args:
            category: New category name
            keywords: List of keywords for this category
        """
        if category not in self.categories:
            # Normalize all keywords to lowercase
            self.categories[category] = [kw.lower() for kw in (keywords or [])]
