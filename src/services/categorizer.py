from typing import Dict, List


class ExpenseCategorizer:
    """Categorizes expenses based on merchant names"""

    def __init__(self):
        """Initialize with default categories and keywords"""
        self.categories: Dict[str, List[str]] = {
            "grocery": ["carrefour", "al maya", "spinneys", "waitrose", "viva"],
            "restaurant": ["gastronomy nasha kuhny"],
            "entertainment": ["cinema", "movie", "theatre", "event", "concert", "game", "amazon", "apple"],
            "transport": ["careem", "uber", "taxi", "rta", "metro", "bus", "petrol", "gas", "fuel"],
            "clothes": ["apparel", "fashion", "zara", "h&m", "clothing", "shoes", "dress", "wear"],
            "utilities": [" virgin mobile"],
            "other": [],  # Default category
        }

    def categorize(self, merchant: str) -> str:
        """Categorize a merchant based on keywords

        Args:
            merchant: The merchant name

        Returns:
            Category name
        """
        merchant_lower = merchant.lower()

        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in merchant_lower:
                    return category

        return "other"  # Default category

    def add_keyword(self, category: str, keyword: str) -> None:
        """Add a new keyword to a category

        Args:
            category: Category name
            keyword: Keyword to add
        """
        if category in self.categories:
            self.categories[category].append(keyword.lower())

    def add_category(self, category: str, keywords: List[str] = None) -> None:
        """Add a new category with optional keywords

        Args:
            category: New category name
            keywords: List of keywords for this category
        """
        if category not in self.categories:
            self.categories[category] = keywords or []
