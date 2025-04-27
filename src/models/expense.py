from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Expense:
    """Representation of an expense or income transaction"""

    amount: float
    merchant: str
    category: str
    date: Optional[datetime] = None
    message: str = ""
    is_income: bool = field(default=False, compare=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert expense to dictionary"""
        result = {
            "amount": self.amount,
            "merchant": self.merchant,
            "category": self.category,
            "message": self.message,
            "is_income": self.is_income,
        }

        if self.date:
            result["date"] = self.date.isoformat()

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expense":
        """Create expense from dictionary"""
        expense = cls(
            amount=data["amount"],
            merchant=data["merchant"],
            category=data["category"],
            message=data.get("message", ""),
            is_income=data.get("is_income", False),
        )

        if "date" in data and data["date"]:
            try:
                expense.date = datetime.fromisoformat(data["date"])
            except:
                pass

        return expense
