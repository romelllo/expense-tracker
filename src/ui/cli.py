import argparse
from typing import Any, Dict, List

from tabulate import tabulate

from src.models.expense import Expense


class ExpenseTrackerCLI:
    """Command-line interface for the expense tracker"""

    def __init__(self):
        """Initialize CLI parser"""
        self.parser = argparse.ArgumentParser(description="Expense Tracker for iMessage Data")
        self._setup_arguments()

    def _setup_arguments(self):
        """Configure command line arguments"""
        self.parser.add_argument(
            "--days", type=int, default=30, help="Number of past days to analyze"
        )
        self.parser.add_argument("--plot", action="store_true", help="Generate and display charts")
        self.parser.add_argument("--output", help="Save report to file")
        self.parser.add_argument("--category", help="Update category for an expense")
        self.parser.add_argument("--index", type=int, help="Index of expense to update")
        self.parser.add_argument("--categories", help="Path to categories.json configuration file")
        self.parser.add_argument(
            "--add-keyword",
            nargs=2,
            metavar=("CATEGORY", "KEYWORD"),
            help="Add keyword to a category",
        )
        self.parser.add_argument(
            "--show-categories",
            action="store_true",
            help="Display current categories configuration",
        )

    def parse_args(self):
        """Parse command line arguments"""
        return self.parser.parse_args()

    def display_report(self, expenses: List[Expense], analytics: Dict[str, Any]):
        """Display expense report in the terminal

        Args:
            expenses: List of expenses
            analytics: Analytics results
        """
        print("\n===== EXPENSE REPORT =====")

        # Summary section
        print(f"Total Spent: AED {analytics.get('total_spent', 0):.2f}")
        if "total_income" in analytics and analytics["total_income"] > 0:
            print(f"Total Income: AED {analytics['total_income']:.2f}")
            print(f"Net Flow: AED {analytics['net_flow']:.2f}")
            print(
                f"Save Rate: {(analytics['net_flow'] / analytics['total_income']) * 100:.1f}%"
                if analytics["total_income"] > 0
                else "N/A"
            )

        # Category breakdown
        print("\n----- Category Breakdown -----")
        category_data = [
            (
                category,
                f"AED {amount:.2f}",
                f"{(amount / analytics['total_spent']) * 100:.1f}%"
                if analytics["total_spent"] > 0
                else "0%",
            )
            for category, amount in sorted(
                analytics["category_totals"].items(), key=lambda x: x[1], reverse=True
            )
        ]
        print(
            tabulate(category_data, headers=["Category", "Amount", "Percentage"], tablefmt="grid")
        )

        # Top merchants
        print("\n----- Top Merchants -----")
        merchant_data = [
            (merchant, f"AED {amount:.2f}")
            for merchant, amount in analytics["top_merchants"].items()
        ]
        print(tabulate(merchant_data, headers=["Merchant", "Amount"], tablefmt="grid"))

        # Top income sources (if available)
        if analytics.get("top_income_sources"):
            print("\n----- Top Income Sources -----")
            income_data = [
                (source, f"AED {amount:.2f}")
                for source, amount in analytics["top_income_sources"].items()
            ]
            print(tabulate(income_data, headers=["Source", "Amount"], tablefmt="grid"))

        # Recent transactions
        print("\n----- Recent Transactions -----")

        # Filter to show a mix of recent expenses and income
        all_transactions = []
        for i, exp in enumerate(expenses):
            type_label = "INCOME" if getattr(exp, "is_income", False) else "EXPENSE"
            all_transactions.append(
                (i, exp.merchant, f"AED {exp.amount:.2f}", exp.category, type_label)
            )

        # Show most recent 15 transactions
        recent_data = all_transactions[:15]
        print(
            tabulate(
                recent_data,
                headers=["Index", "Merchant", "Amount", "Category", "Type"],
                tablefmt="grid",
            )
        )

        # Monthly summary
        if analytics.get("monthly_summary"):
            print("\n----- Monthly Summary -----")
            monthly_data = [
                (month, f"AED {amount:.2f}")
                for month, amount in sorted(analytics["monthly_summary"].items())
            ]
            print(tabulate(monthly_data, headers=["Month", "Total"], tablefmt="grid"))

    def display_categories(self, categories: Dict[str, List[str]]):
        """Display current category configuration

        Args:
            categories: Dictionary of categories and associated keywords
        """
        print("\n===== CATEGORY CONFIGURATION =====")

        for category, keywords in sorted(categories.items()):
            print(f"\n----- {category.upper()} -----")
            if keywords:
                for i, keyword in enumerate(sorted(keywords)):
                    print(f"{i + 1}. {keyword}")
            else:
                print("No keywords defined")
