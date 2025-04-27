from typing import Any, Dict

import matplotlib.pyplot as plt
import numpy as np


class ExpenseVisualizer:
    """Visualizes expense data using charts"""

    def generate_charts(self, analytics: Dict[str, Any]):
        """Generate and display expense charts

        Args:
            analytics: Analytics results
        """
        # Cash flow overview
        plt.figure(figsize=(15, 12))

        # Create a cash flow overview chart at the top
        if "total_income" in analytics and analytics["total_income"] > 0:
            plt.subplot(3, 2, 1)
            cash_flow_labels = ["Income", "Expenses", "Net"]
            cash_flow_values = [
                analytics["total_income"],
                analytics["total_spent"],
                analytics["net_flow"],
            ]
            colors = ["green", "red", "blue" if analytics["net_flow"] >= 0 else "orange"]
            plt.bar(cash_flow_labels, cash_flow_values, color=colors)
            plt.title("Cash Flow Overview")
            plt.ylabel("Amount (AED)")

            # Add value labels on bars
            for i, v in enumerate(cash_flow_values):
                plt.text(i, v / 2, f"AED {v:.0f}", ha="center", color="white", fontweight="bold")

        # Pie chart for category distribution
        plt.subplot(3, 2, 2)
        categories = list(analytics["category_totals"].keys())
        amounts = list(analytics["category_totals"].values())

        # Sort categories by amount for better visualization
        sorted_indices = np.argsort(amounts)
        categories = [categories[i] for i in sorted_indices]
        amounts = [amounts[i] for i in sorted_indices]

        # Show only top categories, group small ones as "Other"
        if len(categories) > 7:
            top_categories = categories[-7:]
            top_amounts = amounts[-7:]
            other_amount = sum(amounts[:-7])
            categories = top_categories + ["Other"]
            amounts = top_amounts + [other_amount]

        plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
        plt.title("Expenses by Category")
        plt.axis("equal")

        # Bar chart for top merchants
        plt.subplot(3, 2, 3)
        merchants = list(analytics["top_merchants"].keys())
        merchant_amounts = list(analytics["top_merchants"].values())

        # Horizontal bar chart for better readability of merchant names
        y_pos = np.arange(len(merchants))
        plt.barh(y_pos, merchant_amounts, align="center")
        plt.yticks(y_pos, merchants)
        plt.title("Top Merchants")
        plt.xlabel("Amount (AED)")

        # Add income sources if available
        if analytics.get("top_income_sources"):
            plt.subplot(3, 2, 4)
            sources = list(analytics["top_income_sources"].keys())
            source_amounts = list(analytics["top_income_sources"].values())

            y_pos = np.arange(len(sources))
            plt.barh(y_pos, source_amounts, align="center", color="green")
            plt.yticks(y_pos, sources)
            plt.title("Top Income Sources")
            plt.xlabel("Amount (AED)")

        # Add monthly trend if available
        if analytics.get("monthly_summary") and len(analytics["monthly_summary"]) > 1:
            plt.subplot(3, 2, (5, 6))
            months = sorted(analytics["monthly_summary"].keys())
            monthly_amounts = [analytics["monthly_summary"][month] for month in months]

            plt.plot(months, monthly_amounts, marker="o", linewidth=2)
            plt.title("Monthly Expense Trend")
            plt.xlabel("Month")
            plt.ylabel("Amount (AED)")
            plt.grid(True, linestyle="--", alpha=0.7)
            plt.xticks(rotation=45)

            # Add value labels on points
            for i, v in enumerate(monthly_amounts):
                plt.text(
                    i, v + max(monthly_amounts) * 0.05, f"AED {v:.0f}", ha="center", va="bottom"
                )

        plt.tight_layout()
        plt.show()

        # If monthly category data is available, create a stacked bar chart
        if analytics.get("monthly_categories") and len(analytics["monthly_categories"]) > 1:
            self._plot_monthly_category_breakdown(analytics["monthly_categories"])

    def _plot_monthly_category_breakdown(self, monthly_categories):
        """Plot a stacked bar chart showing category breakdown by month

        Args:
            monthly_categories: Dictionary mapping months to category totals
        """
        plt.figure(figsize=(12, 8))

        months = sorted(monthly_categories.keys())
        all_categories = set()
        for month_data in monthly_categories.values():
            all_categories.update(month_data.keys())

        all_categories = sorted(all_categories)

        # Create a data structure for stacked bars
        data = {}
        for category in all_categories:
            data[category] = []
            for month in months:
                data[category].append(monthly_categories[month].get(category, 0))

        # Create the stacked bar chart
        bottom = np.zeros(len(months))
        for category in all_categories:
            plt.bar(months, data[category], bottom=bottom, label=category)
            bottom += np.array(data[category])

        plt.title("Monthly Expenses by Category")
        plt.xlabel("Month")
        plt.ylabel("Amount (AED)")
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
