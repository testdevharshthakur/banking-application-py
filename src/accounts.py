import random
from typing import Dict, Any, Optional

# Global dictionary to store accounts in memory.
# This data is NOT persistent across application runs.
# It's structured as:
# {
#     "account_number": {
#         "name": str,
#         "pin": str,
#         "balance": float,
#         "transactions": List[Dict]
#     },
#     ...
# }
ACCOUNTS: Dict[str, Dict[str, Any]] = {}


def generate_account_number() -> str:
    """
    Generates a unique 6-digit account number.

    Returns:
        str: A unique 6-digit string representing the account number.
    """
    while True:
        account_number = "".join(random.choices("0123456789", k=6))
        if account_number not in ACCOUNTS:
            return account_number


def create_account(name: str, pin: str, initial_deposit: float) -> Optional[str]:
    """
    Creates a new banking account and adds it to the in-memory ACCOUNTS storage.

    Args:
        name (str): The name of the account holder.
        pin (str): The 4-digit PIN for the account.
        initial_deposit (float): The initial amount to deposit into the account.

    Returns:
        Optional[str]: The newly generated account number if successful,
                       None otherwise (e.g., if input validation fails).
    """
    if not name.strip():
        print("Error: Name cannot be empty.")
        return None
    if not (len(pin) == 4 and pin.isdigit()):
        print("Error: PIN must be a 4-digit number.")
        return None
    if initial_deposit < 0:
        print("Error: Initial deposit cannot be negative.")
        return None

    account_number = generate_account_number()
    ACCOUNTS[account_number] = {
        "name": name.strip(),
        "pin": pin,
        "balance": initial_deposit,
        "transactions": [],
    }
    # A simple initial deposit transaction record.
    # This will be refined by the transactions module later.
    ACCOUNTS[account_number]["transactions"].append(
        {
            "type": "initial_deposit",
            "amount": initial_deposit,
            "timestamp": None,  # Timestamp will be added by record_transaction
        }
    )
    return account_number


def authenticate_account(account_number: str, pin: str) -> Optional[str]:
    """
    Authenticates a user by checking their account number and PIN.

    Args:
        account_number (str): The account number to authenticate.
        pin (str): The PIN associated with the account.

    Returns:
        Optional[str]: The account number if authentication is successful,
                       None otherwise.
    """
    if account_number in ACCOUNTS and ACCOUNTS[account_number]["pin"] == pin:
        return account_number
    return None


def get_account_details(account_number: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves the full details of an account.

    Args:
        account_number (str): The account number.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing account details
                                  if the account exists, None otherwise.
    """
    return ACCOUNTS.get(account_number)


def update_account_balance(account_number: str, amount: float) -> bool:
    """
    Updates the balance of a specified account.

    Args:
        account_number (str): The account number whose balance is to be updated.
        amount (float): The amount to add to the balance. Can be negative for
                        deductions.

    Returns:
        bool: True if the balance was updated successfully, False otherwise
              (e.g., account not found).
    """
    if account_number in ACCOUNTS:
        ACCOUNTS[account_number]["balance"] += amount
        return True
    return False
