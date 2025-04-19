from typing import Dict, Any
import matplotlib.pyplot as plt

class ExpenseVisualizer:
    """Visualizes expense data using charts"""

    def generate_charts(self, analytics: Dict[str, Any]):
        """Generate and display expense charts

        Args:
            analytics: Analytics results
        """
        plt.figure(figsize=(12, 10))

        # Pie chart for category distribution
        plt.subplot(2, 1, 1)
        categories = list(analytics["category_totals"].keys())
        amounts = list(analytics["category_totals"].values())
        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        plt.title('Expenses by Category')

        # Bar chart for top merchants
        plt.subplot(2, 1, 2)
        merchants = list(analytics["top_merchants"].keys())
        merchant_amounts = list(analytics["top_merchants"].values())
        plt.bar(merchants, merchant_amounts)
        plt.title('Top Merchants')
        plt.xticks(rotation=45, ha='right')

        # Add monthly trend if available
        if analytics.get('monthly_summary') and len(analytics['monthly_summary']) > 1:
            plt.figure(figsize=(10, 6))
            months = sorted(analytics['monthly_summary'].keys())
            monthly_amounts = [analytics['monthly_summary'][month] for month in months]
            plt.plot(months, monthly_amounts, marker='o')
            plt.title('Monthly Expense Trend')
            plt.xlabel('Month')
            plt.ylabel('Amount (AED)')
            plt.xticks(rotation=45)
            plt.tight_layout()

        plt.tight_layout()
        plt.show()
