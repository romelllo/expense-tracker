import argparse
import json
import os
from typing import Dict, List, Set


def load_json(file_path: str) -> List[Dict]:
    """Load JSON data from file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []


def save_json(file_path: str, data) -> bool:
    """Save data to JSON file"""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        return False


def extract_merchant_suggestions(expenses: List[Dict]) -> Dict[str, Set[str]]:
    """Extract unique merchants from expenses and suggest categories"""
    merchants = {}

    for expense in expenses:
        merchant = expense.get("merchant", "").strip()
        if merchant and merchant != "Unknown":
            merchants[merchant] = merchants.get(merchant, set())
            if "category" in expense and expense["category"] != "other":
                merchants[merchant].add(expense["category"])

    return merchants


def update_categories(categories_file: str, expenses_file: str) -> None:
    """Update categories based on expense data"""
    # Load data
    categories = load_json(categories_file)
    expenses = load_json(expenses_file)

    if not categories or not expenses:
        print("Error: Could not load categories or expenses")
        return

    # Extract merchant information
    merchants = extract_merchant_suggestions(expenses)

    # Find uncategorized merchants (those with 'other' category)
    uncategorized = []
    for expense in expenses:
        if expense.get("category") == "other":
            merchant = expense.get("merchant", "").strip()
            if merchant and merchant not in uncategorized:
                uncategorized.append(merchant)

    # Print statistics
    print(f"Found {len(merchants)} unique merchants")
    print(f"Found {len(uncategorized)} uncategorized merchants")

    # Process each uncategorized merchant
    for merchant in uncategorized:
        print(f"\nMerchant: {merchant}")
        print("Choose a category:")

        # List existing categories
        for i, category in enumerate(categories.keys()):
            print(f"{i + 1}. {category}")

        print("n. Create new category")
        print("s. Skip this merchant")

        choice = input("Enter your choice: ")

        if choice == "s":
            continue
        elif choice == "n":
            new_category = input("Enter new category name: ")
            if new_category and new_category not in categories:
                categories[new_category] = []
            categories[new_category].append(merchant)
            print(f"Added {merchant} to new category {new_category}")
        elif choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = list(categories.keys())[int(choice) - 1]
            categories[category].append(merchant)
            print(f"Added {merchant} to category {category}")

    # Save updated categories
    if save_json(categories_file, categories):
        print(f"\nUpdated categories saved to {categories_file}")
    else:
        print(f"\nFailed to save updated categories")


def main():
    parser = argparse.ArgumentParser(description="Helper for updating expense categories")
    parser.add_argument("--categories", required=True, help="Path to categories.json file")
    parser.add_argument("--expenses", required=True, help="Path to expenses.json file")

    args = parser.parse_args()
    update_categories(args.categories, args.expenses)


if __name__ == "__main__":
    main()
