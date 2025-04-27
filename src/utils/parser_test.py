import argparse
import json
import os
import sys
from typing import Any, Dict, List

# Add the parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.services.categorizer import ExpenseCategorizer
from src.services.parser import extract_payment_details


def test_parser(message: str) -> None:
    """Test parser with a single message"""
    details = extract_payment_details(message)
    print("\nInput Message:")
    print(message)
    print("\nExtracted Details:")
    for key, value in details.items():
        print(f"  {key}: {value}")


def test_categorizer(merchant: str, categories_file: str = None) -> None:
    """Test categorizer with a single merchant"""
    categorizer = ExpenseCategorizer(categories_file)
    category = categorizer.categorize(merchant)
    print(f"\nMerchant: {merchant}")
    print(f"Categorized as: {category}")


def batch_test(messages_file: str, categories_file: str = None) -> None:
    """Test parser and categorizer with a batch of messages"""
    try:
        categorizer = ExpenseCategorizer(categories_file)

        with open(messages_file, "r") as f:
            data = json.load(f)

        results = []
        success_count = 0
        for i, item in enumerate(data):
            message = item.get("text", "")
            details = extract_payment_details(message)

            # Only process payment messages that have an amount
            if details["amount"] > 0:
                merchant = details["merchant"]
                category = categorizer.categorize(merchant)

                result = {"message": message, "merchant": merchant, "category": category}

                if merchant != "Unknown":
                    success_count += 1

                results.append(result)

                # Print progress every 10 items
                if (i + 1) % 10 == 0:
                    print(f"Processed {i + 1} messages, {success_count} merchants extracted...")

        # Save results to file
        output_file = "parser_test_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\nResults saved to {output_file}")
        print(f"Processed {len(results)} payment messages")
        print(f"Successfully extracted merchants: {success_count}")
        print(f"Failed to extract merchants: {len(results) - success_count}")

    except Exception as e:
        print(f"Error in batch test: {e}")


def main():
    parser = argparse.ArgumentParser(description="Test message parsing and categorization")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Single message test
    message_parser = subparsers.add_parser("message", help="Test parsing a single message")
    message_parser.add_argument("message", help="Message text to parse")

    # Single merchant categorization test
    merchant_parser = subparsers.add_parser("merchant", help="Test categorizing a single merchant")
    merchant_parser.add_argument("merchant", help="Merchant name to categorize")
    merchant_parser.add_argument("--categories", help="Path to categories.json file")

    # Batch test
    batch_parser = subparsers.add_parser("batch", help="Test batch of messages from file")
    batch_parser.add_argument("file", help="JSON file with messages")
    batch_parser.add_argument("--categories", help="Path to categories.json file")

    args = parser.parse_args()

    if args.command == "message":
        test_parser(args.message)
    elif args.command == "merchant":
        test_categorizer(args.merchant, args.categories)
    elif args.command == "batch":
        batch_test(args.file, args.categories)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
