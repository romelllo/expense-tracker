from typing import List, Dict, Any
import pandas as pd
from src.models.expense import Expense

class ExpenseAnalyzer:
    """Analyzes expense data and generates reports"""

    def analyze(self, expenses: List[Expense]) -> Dict[str, Any]:
        """Generate analytics for a list of expenses

        Args:
            expenses: List of Expense objects

        Returns:
            Dictionary containing analysis results
        """
        if not expenses:
            return {"error": "No expenses found"}

        # Convert to DataFrame for easier analysis
        df = pd.DataFrame([exp.to_dict() for exp in expenses])

        # Total amount
        total_spent = df["amount"].sum()

        # Category breakdown
        category_totals = df.groupby("category")["amount"].sum().to_dict()

        # Top merchants
        top_merchants = df.groupby("merchant")["amount"].sum().sort_values(ascending=False).head(5).to_dict()

        # Monthly breakdown if dates are available
        monthly_summary = {}
        if "date" in df.columns and df["date"].notna().any():
            df["month"] = pd.to_datetime(df["date"]).dt.strftime('%Y-%m')
            monthly_summary = df.groupby("month")["amount"].sum().to_dict()

        return {
            "total_spent": total_spent,
            "category_totals": category_totals,
            "top_merchants": top_merchants,
            "monthly_summary": monthly_summary
        }
