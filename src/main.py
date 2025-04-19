import logging
import json
import sys
from typing import List

from src.db.data_source import MessageDatabase
from src.models.expense import Expense
from src.services.parser import extract_payment_details, convert_imessage_date
from src.services.categorizer import ExpenseCategorizer
from src.services.analytics import ExpenseAnalyzer
from src.ui.cli import ExpenseTrackerCLI
from src.ui.visualization import ExpenseVisualizer
from src.utils.config import Config, ExpenseStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def process_messages(messages, categorizer):
    """Process messages into expense objects"""
    expenses = []

    for message in messages:
        # Extract payment details
        details = extract_payment_details(message["text"])

        # Convert date if available
        date = None
        if "date" in message and message["date"]:
            date = convert_imessage_date(message["date"])

        # Categorize the expense
        category = categorizer.categorize(details["merchant"])

        # Create expense object
        expense = Expense(
            amount=details["amount"],
            merchant=details["merchant"],
            category=category,
            date=date,
            message=details["message"]
        )

        expenses.append(expense)

    return expenses

def main():
    """Main entry point for the expense tracker CLI"""
    try:
        # Initialize components
        config = Config()
        cli = ExpenseTrackerCLI()
        args = cli.parse_args()

        # Initialize data source
        db_path = config.get("db_path")
        db = MessageDatabase(db_path)

        # Initialize services
        categorizer = ExpenseCategorizer()
        analyzer = ExpenseAnalyzer()
        visualizer = ExpenseVisualizer()
        expense_store = ExpenseStore(config.get("data_file"))

        # Handle category update if requested
        if args.category and args.index is not None:
            result = expense_store.update_expense_category(args.index, args.category)
            if result:
                print(f"Updated expense {args.index} category to {args.category}")
            else:
                print(f"Failed to update expense {args.index}")
            return

        # Fetch data
        print("Fetching expenses from iMessage database...")
        messages = db.fetch_payment_messages(days=args.days)

        if not messages:
            print("No payment messages found.")
            return

        # Process messages
        print(f"Processing {len(messages)} messages...")
        expenses = process_messages(messages, categorizer)

        # Save expenses
        expense_dicts = [exp.to_dict() for exp in expenses]
        expense_store.save_expenses(expense_dicts)

        # Analyze expenses
        print("Analyzing expenses...")
        analytics = analyzer.analyze(expenses)

        # Display report
        cli.display_report(expenses, analytics)

        # Generate charts if requested
        if args.plot:
            print("Generating charts...")
            visualizer.generate_charts(analytics)

        # Save report if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump({
                    "analytics": analytics,
                    "expenses": expense_dicts
                }, f, indent=2)
            print(f"Report saved to {args.output}")

    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
        print(f"An error occurred: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
