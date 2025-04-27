import json
import logging
import os
import sys

from src.db.data_source import MessageDatabase
from src.models.expense import Expense
from src.services.analytics import ExpenseAnalyzer
from src.services.categorizer import ExpenseCategorizer
from src.services.parser import convert_imessage_date, extract_payment_details
from src.ui.cli import ExpenseTrackerCLI
from src.ui.visualization import ExpenseVisualizer
from src.utils.config import Config, ExpenseStore

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def process_messages(messages, categorizer):
    """Process messages into expense objects"""
    expenses = []
    successful_count = 0
    unknown_merchants = 0

    for message in messages:
        # Extract payment details
        details = extract_payment_details(message["text"])

        # Skip messages with no amount (like promotional messages)
        if details["amount"] == 0:
            continue

        # Keep track of unknown merchants
        if details["merchant"] == "Unknown":
            unknown_merchants += 1
            # Optionally print problematic messages for debugging
            # print(f"Could not extract merchant from: {message['text']}")
        else:
            successful_count += 1

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
            message=details["message"],
        )

        # Add is_income flag if message represents income
        if "is_income" in details:
            setattr(expense, "is_income", details["is_income"])

        expenses.append(expense)

    print(f"Processed {len(expenses)} payment messages")
    print(f"Successfully extracted merchants: {successful_count}")
    print(f"Unknown merchants: {unknown_merchants}")

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
        if not db_path:
            print(
                "Error: Database path not configured. Set EXPENSE_TRACKER_DB_PATH environment variable."
            )
            return 1

        if not os.path.exists(db_path):
            print(f"Error: Database file not found at {db_path}")
            return 1

        db = MessageDatabase(db_path)

        # Get categories file path
        categories_file = args.categories or config.get("categories_file")

        # Initialize services
        categorizer = ExpenseCategorizer(categories_file)
        analyzer = ExpenseAnalyzer()
        visualizer = ExpenseVisualizer()
        expense_store = ExpenseStore(config.get("data_file"))

        # Display categories if requested
        if args.show_categories:
            cli.display_categories(categorizer.categories)
            return 0

        # Add keyword to category if requested
        if args.add_keyword:
            category, keyword = args.add_keyword
            categorizer.add_keyword(category, keyword)
            categorizer.save_categories(categories_file)
            print(f"Added keyword '{keyword}' to category '{category}'")
            return 0

        # Handle category update if requested
        if args.category and args.index is not None:
            result = expense_store.update_expense_category(args.index, args.category)
            if result:
                print(f"Updated expense {args.index} category to {args.category}")
            else:
                print(f"Failed to update expense {args.index}")
            return 0

        # Fetch data
        print("Fetching expenses from iMessage database...")
        messages = db.fetch_payment_messages(days=args.days)

        if not messages:
            print("No payment messages found.")
            return 0

        # Process messages
        print(f"Processing {len(messages)} messages...")
        expenses = process_messages(messages, categorizer)

        if not expenses:
            print("No valid expense data found in messages.")
            return 0

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
            with open(args.output, "w") as f:
                json.dump({"analytics": analytics, "expenses": expense_dicts}, f, indent=2)
            print(f"Report saved to {args.output}")

    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
        print(f"An error occurred: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
