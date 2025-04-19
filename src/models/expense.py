from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Expense:
    """Representation of an expense transaction"""
    amount: float
    merchant: str
    category: str
    date: Optional[datetime] = None
    message: str = ""

    def to_dict(self):
        """Convert expense to dictionary"""
        result = {
            "amount": self.amount,
            "merchant": self.merchant,
            "category": self.category,
            "message": self.message
        }

        if self.date:
            result["date"] = self.date.isoformat()

        return result

    @classmethod
    def from_dict(cls, data):
        """Create expense from dictionary"""
        expense = cls(
            amount=data["amount"],
            merchant=data["merchant"],
            category=data["category"],
            message=data.get("message", "")
        )

        if "date" in data and data["date"]:
            try:
                expense.date = datetime.fromisoformat(data["date"])
            except:
                pass

        return expense
