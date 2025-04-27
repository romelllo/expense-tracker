from typing import Any, Dict, List

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

        # Total amount - separate incoming and outgoing
        outgoing = (
            df[~df.get("is_income", False)]["amount"].sum()
            if "is_income" in df
            else df["amount"].sum()
        )
        incoming = df[df.get("is_income", True)]["amount"].sum() if "is_income" in df else 0

        # Net flow (income - expenses)
        net_flow = incoming - outgoing

        # Category breakdown (ignore income categories for expense breakdown)
        expense_df = df[~df.get("is_income", False)] if "is_income" in df else df
        category_totals = expense_df.groupby("category")["amount"].sum().to_dict()

        # Top merchants by spending
        top_merchants = (
            expense_df.groupby("merchant")["amount"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .to_dict()
        )

        # Top income sources
        top_income_sources = {}
        if "is_income" in df and df["is_income"].any():
            income_df = df[df["is_income"]]
            top_income_sources = (
                income_df.groupby("merchant")["amount"]
                .sum()
                .sort_values(ascending=False)
                .head(3)
                .to_dict()
            )

        # Monthly breakdown if dates are available
        monthly_summary = {}
        if "date" in df.columns and df["date"].notna().any():
            df["month"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
            monthly_summary = df.groupby("month")["amount"].sum().to_dict()

            # Monthly breakdown by category
            monthly_categories = {}
            for month in df["month"].unique():
                month_df = df[df["month"] == month]
                monthly_categories[month] = month_df.groupby("category")["amount"].sum().to_dict()

        return {
            "total_spent": outgoing,
            "total_income": incoming,
            "net_flow": net_flow,
            "category_totals": category_totals,
            "top_merchants": top_merchants,
            "top_income_sources": top_income_sources,
            "monthly_summary": monthly_summary,
            "monthly_categories": monthly_categories if "date" in df.columns else {},
        }
