# Expense Tracker for iMessage Banking Notifications

This tool automatically extracts and categorizes expenses from your iMessage banking notifications. It analyzes messages containing payment details, categorizes merchants, and generates reports with visualizations.

## Features

- **Automated Expense Tracking**: Extracts transaction details from banking SMS and iMessage notifications
- **Smart Categorization**: Automatically categorizes transactions based on merchant names
- **Interactive Reports**: View expense breakdowns by category, merchant, and time period
- **Data Visualization**: Generate charts and graphs of your spending patterns
- **Customizable Categories**: Define and maintain your own expense categories
- **Transaction Management**: Review, recategorize, or exclude transactions as needed

## Installation

### Prerequisites

- Python 3.8 or higher
- Access to an iMessage database (typically on macOS)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/romelllo/expense-tracker.git
   cd expense-tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   # Create a .env file in the project root
   echo "EXPENSE_TRACKER_DB_PATH=/path/to/chat.db" > .env
   echo "EXPENSE_TRACKER_CATEGORIES_FILE=src/utils/categories.json" >> .env
   ```

   On macOS, the iMessage database is typically located at:
   ```
   ~/Library/Messages/chat.db
   ```

## Usage

### Basic Usage

Generate an expense report for the last 30 days:

```bash
python -m src.main
```

### Command-Line Options

```bash
python -m src.main --days 90 --plot --output report.json
```

Options:
- `--days NUM`: Analyze expenses from the last NUM days (default: 30)
- `--plot`: Generate and display visualizations
- `--output FILE`: Save the report to a JSON file
- `--categories FILE`: Specify a custom categories configuration file
- `--show-categories`: Display the current category configuration
- `--category NAME --index NUM`: Update the category of a specific expense
- `--add-keyword CATEGORY KEYWORD`: Add a keyword to a category

### Managing Categories

Display current category configuration:

```bash
python -m src.main --show-categories
```

Add a new keyword to a category:

```bash
python -m src.main --add-keyword restaurant "pizza hut"
```

Update an expense's category:

```bash
python -m src.main --category entertainment --index 5
```

## Testing

The project includes tools to test the parser and categorizer functionality.

### Parser Testing

Test a single message:

```bash
python -m src.utils.parser_test message "Payment of AED 48 was done at Restaurant Name using your card 1234"
```

Test categorizing a merchant:

```bash
python -m src.utils.parser_test merchant "Restaurant Name" --categories src/utils/categories.json
```

Batch test multiple messages from a file:

```bash
python -m src.utils.parser_test batch test_messages.json --categories src/utils/categories.json
```

### Creating Test Data

Create a JSON file with sample messages:

```json
[
  {"text": "Payment of AED 48 was done at Restaurant Name using your card 1234"},
  {"text": "Payment of AED 35.53 was done at Grocery Store using your card 1234"}
]
```

## Category Management

### Category Configuration

Categories are defined in `src/utils/categories.json`:

```json
{
  "grocery": ["supermarket", "grocery", "carrefour"],
  "restaurant": ["cafe", "restaurant", "dining"],
  "transport": ["uber", "taxi", "metro"],
  ...
}
```

### Interactive Category Helper

To help categorize new merchants:

```bash
python -m src.utils.category_helper --categories src/utils/categories.json --expenses expenses.json
```

This tool will:
1. Scan your expenses for uncategorized merchants
2. Allow you to assign them to existing categories
3. Create new categories as needed
4. Save the updated configuration

## Project Structure

```
expense-tracker/
├── expenses.json             # Generated expense data
├── requirements.txt          # Project dependencies
├── README.md                 # This file
└── src/
    ├── db/                   # Database access
    │   └── data_source.py    # iMessage database connector
    ├── main.py               # Main entry point
    ├── models/               # Data models
    │   └── expense.py        # Expense representation
    ├── services/             # Core logic
    │   ├── analytics.py      # Data analysis
    │   ├── categorizer.py    # Transaction categorization
    │   └── parser.py         # Message parsing
    ├── ui/                   # User interface
    │   ├── cli.py            # Command-line interface
    │   └── visualization.py  # Charts and graphs
    └── utils/                # Utility modules
        ├── categories.json   # Category configuration
        ├── config.py         # Configuration management
        ├── category_helper.py # Category management tool
        ├── parser_test.py    # Testing utilities
        └── date_utils.py     # Date handling utilities
```

## To Do:
- [ ] Add support for more banks, payment systems and currencies
- [ ] Improve categorization algorithm
- [ ] Add more visualizations and reports
- [ ] Implement a web interface for easier access
- [ ] Add unit tests for all modules
- [ ] Improve error handling and logging

## FAQ

**Q: Does this tool have access to my banking information?**
A: No. The tool only reads locally stored message notifications that you've already received. It does not connect to any banking services or send data anywhere.

**Q: What banks/payment systems are supported?**
A: The tool is designed to work with any bank that sends payment notifications containing transaction amount and merchant information. It's specifically optimized for messages containing "AED" currency.

**Q: Can I add support for another currency?**
A: Yes! You would need to modify the regular expressions in `src/services/parser.py` to match your currency's format.

**Q: Why are some merchants not categorized correctly?**
A: The categorization system relies on keyword matching. If a merchant name doesn't contain any keywords from your categories, it will be marked as "other". Use the category helper to improve categorization over time.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- This project was inspired by the need for better expense tracking when banks don't provide proper categorization
- Thanks to all the open-source libraries that made this project possible

---

For issues, questions, or contributions, please open an issue or pull request on GitHub.
