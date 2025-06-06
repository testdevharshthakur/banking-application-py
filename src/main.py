import os
from src.accounts import (
    ACCOUNTS,  # ACCOUNTS is global, so changes to it in accounts.py
    # are reflected here. It is the core data storage.
    create_account,
    authenticate_account,
    get_account_details,
)
from src.transactions import (
    deposit,
    withdraw,
    transfer,
    get_transaction_history,
)

CURRENT_ACCOUNT: Optional[str] = None  # Stores the currently logged-in account number


def clear_screen() -> None:
    """Clears the terminal screen for a cleaner UI."""
    # 'cls' for Windows, 'clear' for macOS/Linux
    os.system("cls" if os.name == "nt" else "clear")


def display_main_menu() -> None:
    """Displays the main menu options for unauthenticated users."""
    print("\n===== Banking System Terminal =====")
    print("1. Create New Account")
    print("2. Login")
    print("3. Exit")
    print("===================================")


def display_account_menu(account_name: str) -> None:
    """
    Displays the menu options for a logged-in user.

    Args:
        account_name (str): The name of the currently logged-in account holder.
    """
    print(f"\n===== Welcome, {account_name}! =====")
    print("1. Deposit Funds")
    print("2. Withdraw Funds")
    print("3. Check Balance")
    print("4. Transfer Funds")
    print("5. View Transactions")
    print("6. Logout")
    print("===================================")


def handle_create_account() -> None:
    """Handles the user interaction for creating a new account."""
    print("\n--- Create New Account ---")
    name = input("Enter your full name: ").strip()
    while True:
        pin = input("Create a 4-digit PIN: ").strip()
        if len(pin) == 4 and pin.isdigit():
            break
        print("PIN must be a 4-digit number.")
    while True:
        try:
            initial_deposit = float(input("Enter initial deposit amount: $"))
            if initial_deposit >= 0:
                break
            print("Initial deposit cannot be negative.")
        except ValueError:
            print("Invalid amount. Please enter a number.")

    account_number = create_account(name, pin, initial_deposit)
    if account_number:
        print("\nAccount created successfully!")
        print(f"Your account number is: {account_number}")
        print("Please remember your account number and PIN.")
    else:
        print("\nAccount creation failed. Please check inputs.")


def handle_login() -> bool:
    """
    Handles the user login process.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    global CURRENT_ACCOUNT
    print("\n--- Account Login ---")
    account_number = input("Enter your account number: ").strip()
    pin = input("Enter your PIN: ").strip()

    authenticated_account = authenticate_account(account_number, pin)
    if authenticated_account:
        CURRENT_ACCOUNT = authenticated_account
        print(f"Welcome back, {ACCOUNTS[CURRENT_ACCOUNT]['name']}!")
        return True
    else:
        print("Invalid account number or PIN.")
        return False


def handle_deposit(account_number: str) -> None:
    """Handles the deposit operation for the logged-in user."""
    print("\n--- Deposit Funds ---")
    while True:
        try:
            amount = float(input("Enter amount to deposit: $"))
            if deposit(account_number, amount):
                print(f"Successfully deposited ${amount:.2f}.")
                print(f"Current balance: ${ACCOUNTS[account_number]['balance']:.2f}")
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")


def handle_withdraw(account_number: str) -> None:
    """Handles the withdrawal operation for the logged-in user."""
    print("\n--- Withdraw Funds ---")
    while True:
        try:
            amount = float(input("Enter amount to withdraw: $"))
            if withdraw(account_number, amount):
                print(f"Successfully withdrew ${amount:.2f}.")
                print(f"Current balance: ${ACCOUNTS[account_number]['balance']:.2f}")
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")


def handle_check_balance(account_number: str) -> None:
    """Displays the current balance of the logged-in account."""
    print("\n--- Account Balance ---")
    account_details = get_account_details(account_number)
    if account_details:
        print(f"Account Holder: {account_details['name']}")
        print(f"Account Number: {account_number}")
        print(f"Current Balance: ${account_details['balance']:.2f}")
    else:
        print("Error: Account details not found. Please re-login.")


def handle_transfer(source_account_number: str) -> None:
    """Handles the transfer operation for the logged-in user."""
    print("\n--- Transfer Funds ---")
    target_account_number = input("Enter recipient's account number: ").strip()

    while True:
        try:
            amount = float(input("Enter amount to transfer: $"))
            if transfer(source_account_number, target_account_number, amount):
                print(
                    f"Successfully transferred ${amount:.2f} to account"
                    f" {target_account_number}."
                )
                print(
                    "Your new balance:"
                    f" ${ACCOUNTS[source_account_number]['balance']:.2f}"
                )
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")


def handle_view_transactions(account_number: str) -> None:
    """Displays the transaction history for the logged-in account."""
    print(f"\n--- Transaction History for Account {account_number} ---")
    transactions = get_transaction_history(account_number)
    if not transactions:
        print("No transactions yet.")
        return

    for i, tx in enumerate(transactions):
        print(f"--- Transaction {i + 1} ---")
        print(f"Type: {tx['type'].replace('_', ' ').title()}")
        print(f"Amount: ${tx['amount']:.2f}")
        if "target_account" in tx and tx["target_account"]:
            if tx["type"] == "transfer_sent":
                print(f"To Account: {tx['target_account']}")
            elif tx["type"] == "transfer_received":
                print(f"From Account: {tx['target_account']}")
        print(f"Date/Time: {tx['timestamp']}")
        print("-" * 20)


def main() -> None:
    """Main function to run the banking application."""
    # TODO for brother: Load accounts from data/accounts.json here
    # E.g., load_accounts()

    while True:
        clear_screen()
        if CURRENT_ACCOUNT is None:
            display_main_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                handle_create_account()
            elif choice == "2":
                handle_login()
            elif choice == "3":
                print("Thank you for using the Banking System. Goodbye!")
                # TODO for brother: Save accounts to data/accounts.json here
                # E.g., save_accounts()
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            account_details = get_account_details(CURRENT_ACCOUNT)
            if not account_details:
                # Should not happen if CURRENT_ACCOUNT is set correctly,
                # but a safeguard.
                print("Error: Logged-in account not found. Logging out...")
                global CURRENT_ACCOUNT
                CURRENT_ACCOUNT = None
                continue

            display_account_menu(account_details["name"])
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                handle_deposit(CURRENT_ACCOUNT)
            elif choice == "2":
                handle_withdraw(CURRENT_ACCOUNT)
            elif choice == "3":
                handle_check_balance(CURRENT_ACCOUNT)
            elif choice == "4":
                handle_transfer(CURRENT_ACCOUNT)
            elif choice == "5":
                handle_view_transactions(CURRENT_ACCOUNT)
            elif choice == "6":
                global CURRENT_ACCOUNT
                print(f"Logging out from account {ACCOUNTS[CURRENT_ACCOUNT]['name']}.")
                CURRENT_ACCOUNT = None
                input("\nLogged out. Press Enter to continue...")
                continue  # Go back to main menu immediately
            else:
                print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")  # Pause for user to read message


if __name__ == "__main__":
    main()
