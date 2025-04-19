import argparse
from tabulate import tabulate
from typing import List, Dict, Any
from src.models.expense import Expense

class ExpenseTrackerCLI:
    """Command-line interface for the expense tracker"""

    def __init__(self):
        """Initialize CLI parser"""
        self.parser = argparse.ArgumentParser(description='Expense Tracker for iMessage Data')
        self._setup_arguments()

    def _setup_arguments(self):
        """Configure command line arguments"""
        self.parser.add_argument('--days', type=int, help='Number of past days to analyze')
        self.parser.add_argument('--plot', action='store_true', help='Generate and display charts')
        self.parser.add_argument('--output', help='Save report to file')
        self.parser.add_argument('--category', help='Update category for an expense')
        self.parser.add_argument('--index', type=int, help='Index of expense to update')

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
        print(f"Total Spent: AED {analytics['total_spent']:.2f}")

        print("\n----- Category Breakdown -----")
        category_data = [
            (category, f"AED {amount:.2f}", f"{(amount/analytics['total_spent'])*100:.1f}%")
            for category, amount in analytics['category_totals'].items()
        ]
        print(tabulate(category_data, headers=["Category", "Amount", "Percentage"], tablefmt="grid"))

        print("\n----- Top Merchants -----")
        merchant_data = [
            (merchant, f"AED {amount:.2f}")
            for merchant, amount in analytics['top_merchants'].items()
        ]
        print(tabulate(merchant_data, headers=["Merchant", "Amount"], tablefmt="grid"))

        print("\n----- Recent Transactions -----")
        recent_data = [
            (i, exp.merchant, f"AED {exp.amount:.2f}", exp.category)
            for i, exp in enumerate(expenses[:10])  # Last 10 transactions
        ]
        print(tabulate(recent_data, headers=["Index", "Merchant", "Amount", "Category"], tablefmt="grid"))

        if analytics.get('monthly_summary'):
            print("\n----- Monthly Summary -----")
            monthly_data = [
                (month, f"AED {amount:.2f}")
                for month, amount in sorted(analytics['monthly_summary'].items())
            ]
            print(tabulate(monthly_data, headers=["Month", "Total"], tablefmt="grid"))
