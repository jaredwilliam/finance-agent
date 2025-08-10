# Personal Finance Transaction Categorizer

An AI-powered CLI application that categorizes financial transactions using Anthropic's Claude API. Users can input transaction details, get intelligent categorization, and maintain a CSV log of all transactions for future reference.

## Features

- **Interactive CLI**: Easy-to-use command line interface for transaction input
- **AI Categorization**: Leverages Claude Sonnet 4 to intelligently categorize transactions
- **Validation**: Built-in validation for payment methods and amount inputs
- **CSV Logging**: Automatically saves all transactions and categorizations to CSV
- **Hierarchical Categories**: Supports detailed transaction categories based on Monarch Money structure

## Requirements

- Python 3.7+
- Anthropic API key
- Required packages: `anthropic`, `python-dotenv`

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install anthropic python-dotenv
   ```
3. Create a `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```
4. Ensure the `data/` directory exists for CSV output

## Usage

Run the application:
```bash
python src/finance_agent.py
```

The CLI will prompt you for:
- **Merchant**: Name of the business/vendor
- **Description**: Transaction description
- **Payment Method**: Must be one of: Credit Card, Debit Card, Cash
- **Amount**: Transaction amount in dollars

## Output

- **Console**: Displays categorization results with reasoning and confidence
- **CSV File**: Saves to `data/transactions.csv` with columns:
  - date, merchant, description, payment_method, amount
  - category, confidence, reasoning

## Categories

Transactions are categorized into hierarchical groups including:
- Income (Paychecks, Interest)
- Expenses (Food, Housing, Transportation, etc.)
- Transfers (Credit Card Payments, Balance Adjustments)

See `docs/transaction_categories.md` for the complete category structure.

## Architecture

The application follows modular design principles with separate functions for:
- Transaction input and validation
- AI prompt building and template processing
- API communication with Claude
- CSV data persistence