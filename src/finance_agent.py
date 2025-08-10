import json
import csv
import os
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()

CLIENT = Anthropic()
MODEL = "claude-sonnet-4-20250514"
CATEGORIES ='docs/transaction-categories.md'
PROMPT_TEMPLATE = 'docs/prompt-template.md'
TRANSACTIONS_CSV = 'data/transactions.csv'
VALID_PAYMENT_METHODS = ['Credit Card', 'Debit Card', 'Cash']

def add_user_message(messages, text):
	user_message = {"role": "user", "content": text}
	messages.append(user_message)
	
def add_assistant_message(messages, text):
	assistant_message = {"role": "assistant", "content": text}
	messages.append(assistant_message)
	
def chat(messages):
	message = CLIENT.messages.create(
		model=MODEL,
		max_tokens = 1000,
		messages = messages,
	)
	return message.content[0].text

def extract_template_content(template_content: str) -> str:
    """
    Extracts content between <prompt-template> tags.
    
    Args:
        template_content: Raw template file content
        
    Returns:
        Extracted template content
    """
    start_tag = "<prompt-template>"
    end_tag = "</prompt-template>"
    start_idx = template_content.find(start_tag) + len(start_tag)
    end_idx = template_content.find(end_tag)
    return template_content[start_idx:end_idx].strip()

def build_prompt(template: str, categories: str, transaction: dict) -> str:
    """
    Builds the complete prompt by replacing placeholders.
    
    Args:
        template: Prompt template string
        categories: Categories content
        transaction: Transaction dictionary
        
    Returns:
        Complete prompt string
    """
    transaction_json = json.dumps(transaction, indent=2)
    prompt = template.replace("{{CATEGORIES_FILE}}", categories)
    prompt = prompt.replace("{{TRANSACTION}}", transaction_json)
    return prompt

def categorize_transaction(transaction: dict):
    """
    Categorizes a single transaction using the Anthropic API.
    
    Args:
        transaction: Dictionary containing transaction details
        
    Returns:
        Dictionary with categorization results including category, reasoning, and confidence
    """
    # Read categories file
    with open(CATEGORIES, 'r', encoding='utf-8') as f:
        categories_content = f.read()
    
    # Read prompt template
    with open(PROMPT_TEMPLATE, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Extract template and build prompt
    template = extract_template_content(template_content)
    prompt = build_prompt(template, categories_content, transaction)
    
    # Make API call
    messages = []
    add_user_message(messages, prompt)
    response = chat(messages)
    
    # Extract JSON from response
    output_start = response.find("<output>") + len("<output>")
    output_end = response.find("</output>")
    json_str = response[output_start:output_end].strip()
    
    return json.loads(json_str)

def validate_payment_method(payment_method: str) -> str:
    """
    Validates and returns the payment method if valid.
    
    Args:
        payment_method: User input for payment method
        
    Returns:
        Valid payment method string
        
    Raises:
        ValueError: If payment method is not valid
    """
    if payment_method in VALID_PAYMENT_METHODS:
        return payment_method
    raise ValueError(f"Invalid payment method. Must be one of: {', '.join(VALID_PAYMENT_METHODS)}")

def get_user_transaction_input() -> dict:
    """
    Prompts user for transaction details via CLI.
    
    Returns:
        Dictionary containing transaction details
    """
    print("Enter transaction details:")
    
    merchant = input("Merchant: ").strip()
    description = input("Description: ").strip()
    
    # Get payment method with validation
    while True:
        print(f"Valid payment methods: {', '.join(VALID_PAYMENT_METHODS)}")
        payment_method = input("Payment method: ").strip()
        try:
            payment_method = validate_payment_method(payment_method)
            break
        except ValueError as e:
            print(f"Error: {e}")
    
    # Get amount
    while True:
        try:
            amount = float(input("Amount: $"))
            break
        except ValueError:
            print("Error: Please enter a valid number for amount")
    
    return {
        "merchant": merchant,
        "description": description,
        "payment_method": payment_method,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def save_transaction_to_csv(transaction: dict, categorization_result: dict):
    """
    Saves transaction and categorization result to CSV file.
    
    Args:
        transaction: Transaction details dictionary
        categorization_result: AI categorization result
    """
    file_exists = os.path.exists(TRANSACTIONS_CSV)
    
    with open(TRANSACTIONS_CSV, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'merchant', 'description', 'payment_method', 'amount', 
                     'category', 'confidence', 'reasoning']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writeheader()
        
        # Combine transaction and categorization data
        row_data = {
            'date': transaction['date'],
            'merchant': transaction['merchant'],
            'description': transaction['description'],
            'payment_method': transaction['payment_method'],
            'amount': transaction['amount'],
            'category': categorization_result['category'],
            'confidence': categorization_result['confidence'],
            'reasoning': categorization_result['reasoning']
        }
        
        writer.writerow(row_data)

def main():
    """Main CLI application loop."""
    print("Personal Finance Transaction Categorizer")
    print("=" * 40)
    
    while True:
        try:
            # Get transaction input from user
            transaction = get_user_transaction_input()
            
            # Categorize the transaction
            print("\nCategorizing transaction...")
            categorization_result = categorize_transaction(transaction)
            
            # Display results
            print(f"\nCategory: {categorization_result['category']}")
            print(f"Confidence: {categorization_result['confidence']}")
            print(f"Reasoning: {categorization_result['reasoning']}")
            
            # Save to CSV
            save_transaction_to_csv(transaction, categorization_result)
            print(f"\nTransaction saved to {TRANSACTIONS_CSV}")
            
            # Ask if user wants to continue
            continue_choice = input("\nEnter another transaction? (y/n): ").strip().lower()
            if continue_choice != 'y':
                break
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            continue_choice = input("Try again? (y/n): ").strip().lower()
            if continue_choice != 'y':
                break

if __name__ == "__main__":
    main()