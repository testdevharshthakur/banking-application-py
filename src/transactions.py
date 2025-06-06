import datetime
from typing import Dict, Any, List
from src.accounts import ACCOUNTS, update_account_balance


def record_transaction(
    account_number: str, type: str, amount: float, target_account: str = None
) -> None:
    """
    Records a transaction for the given account in its transaction history.

    Args:
        account_number (str): The account number for which to record the transaction.
        type (str): The type of transaction (e.g., 'deposit', 'withdraw',
                    'transfer_sent', 'transfer_received', 'initial_deposit').
        amount (float): The amount involved in the transaction.
        target_account (str, optional): The other account involved in a transfer,
                                        if applicable. Defaults to None.
    """
    transaction: Dict[str, Any] = {
        "type": type,
        "amount": amount,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    if target_account:
        transaction["target_account"] = target_account

    if account_number in ACCOUNTS:
        ACCOUNTS[account_number]["transactions"].append(transaction)


def deposit(account_number: str, amount: float) -> bool:
    """
    Deposits funds into a specified account.

    Args:
        account_number (str): The account number to deposit into.
        amount (float): The amount to deposit.

    Returns:
        bool: True if the deposit was successful, False otherwise.
    """
    if amount <= 0:
        print("Error: Deposit amount must be positive.")
        return False
    if account_number not in ACCOUNTS:
        print("Error: Account not found.")
        return False

    update_account_balance(account_number, amount)
    record_transaction(account_number, "deposit", amount)
    return True


def withdraw(account_number: str, amount: float) -> bool:
    """
    Withdraws funds from a specified account.

    Args:
        account_number (str): The account number to withdraw from.
        amount (float): The amount to withdraw.

    Returns:
        bool: True if the withdrawal was successful, False otherwise.
    """
    if amount <= 0:
        print("Error: Withdrawal amount must be positive.")
        return False
    if account_number not in ACCOUNTS:
        print("Error: Account not found.")
        return False

    if ACCOUNTS[account_number]["balance"] < amount:
        print("Error: Insufficient funds.")
        return False

    update_account_balance(account_number, -amount)  # Deduct amount
    record_transaction(account_number, "withdraw", amount)
    return True


def transfer(
    source_account_number: str, target_account_number: str, amount: float
) -> bool:
    """
    Transfers funds from a source account to a target account.

    Args:
        source_account_number (str): The account number to transfer from.
        target_account_number (str): The account number to transfer to.
        amount (float): The amount to transfer.

    Returns:
        bool: True if the transfer was successful, False otherwise.
    """
    if amount <= 0:
        print("Error: Transfer amount must be positive.")
        return False

    if source_account_number not in ACCOUNTS:
        print("Error: Source account not found.")
        return False
    if target_account_number not in ACCOUNTS:
        print("Error: Target account not found.")
        return False
    if source_account_number == target_account_number:
        print("Error: Cannot transfer to the same account.")
        return False

    if ACCOUNTS[source_account_number]["balance"] < amount:
        print("Error: Insufficient funds in source account for transfer.")
        return False

    # Deduct from source
    update_account_balance(source_account_number, -amount)
    record_transaction(
        source_account_number, "transfer_sent", amount, target_account_number
    )

    # Add to target
    update_account_balance(target_account_number, amount)
    record_transaction(
        target_account_number, "transfer_received", amount, source_account_number
    )

    return True


def get_transaction_history(account_number: str) -> List[Dict[str, Any]]:
    """
    Retrieves the transaction history for a specified account.

    Args:
        account_number (str): The account number to retrieve history for.

    Returns:
        List[Dict[str, Any]]: A list of transaction dictionaries, or an empty list
                               if the account is not found or has no transactions.
    """
    if account_number in ACCOUNTS:
        return ACCOUNTS[account_number]["transactions"]
    return []
