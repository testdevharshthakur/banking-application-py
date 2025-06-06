import unittest
from unittest.mock import patch, MagicMock
from src.accounts import ACCOUNTS, create_account
from src.transactions import (
    record_transaction,
    deposit,
    withdraw,
    transfer,
    get_transaction_history,
)


class TestTransactions(unittest.TestCase):
    def setUp(self):
        """Clears ACCOUNTS and creates a test account before each test."""
        ACCOUNTS.clear()
        self.account_num1 = create_account("Test User One", "1111", 1000.0)
        self.account_num2 = create_account("Test User Two", "2222", 500.0)

    def test_record_transaction(self):
        """Test that transactions are correctly recorded."""
        record_transaction(self.account_num1, "test_type", 50.0)
        history = ACCOUNTS[self.account_num1]["transactions"]
        self.assertEqual(len(history), 2)  # Initial deposit + new transaction
        self.assertEqual(history[1]["type"], "test_type")
        self.assertEqual(history[1]["amount"], 50.0)
        self.assertIsNotNone(history[1]["timestamp"])

        record_transaction(self.account_num1, "transfer_sent", 100.0, "999999")
        self.assertEqual(len(ACCOUNTS[self.account_num1]["transactions"]), 3)
        self.assertEqual(
            ACCOUNTS[self.account_num1]["transactions"][2]["target_account"],
            "999999",
        )

    @patch("src.transactions.record_transaction")
    def test_deposit_success(self, mock_record_transaction):
        """Test successful deposit."""
        initial_balance = ACCOUNTS[self.account_num1]["balance"]
        self.assertTrue(deposit(self.account_num1, 200.0))
        self.assertEqual(
            ACCOUNTS[self.account_num1]["balance"], initial_balance + 200.0
        )
        mock_record_transaction.assert_called_once_with(
            self.account_num1, "deposit", 200.0
        )

    def test_deposit_negative_amount(self):
        """Test deposit with negative amount."""
        initial_balance = ACCOUNTS[self.account_num1]["balance"]
        self.assertFalse(deposit(self.account_num1, -50.0))
        self.assertEqual(ACCOUNTS[self.account_num1]["balance"], initial_balance)

    def test_deposit_zero_amount(self):
        """Test deposit with zero amount."""
        initial_balance = ACCOUNTS[self.account_num1]["balance"]
        self.assertFalse(deposit(self.account_num1, 0.0))
        self.assertEqual(ACCOUNTS[self.account_num1]["balance"], initial_balance)

    def test_deposit_non_existent_account(self):
        """Test deposit to a non-existent account."""
        self.assertFalse(deposit("000000", 100.0))

    @patch("src.transactions.record_transaction")
    def test_withdraw_success(self, mock_record_transaction):
        """Test successful withdrawal."""
        initial_balance = ACCOUNTS[self.account_num1]["balance"]
        self.assertTrue(withdraw(self.account_num1, 300.0))
        self.assertEqual(
            ACCOUNTS[self.account_num1]["balance"], initial_balance - 300.0
        )
        mock_record_transaction.assert_called_once_with(
            self.account_num1, "withdraw", 300.0
        )

    def test_withdraw_insufficient_funds(self):
        """Test withdrawal with insufficient funds."""
        initial_balance = ACCOUNTS[self.account_num1]["balance"]
        self.assertFalse(withdraw(self.account_num1, 1500.0))
        self.assertEqual(ACCOUNTS[self.account_num1]["balance"], initial_balance)

    def test_withdraw_negative_amount(self):
        """Test withdrawal with negative amount."""
        initial_balance = ACCOUNTS[self.account_num1]["balance"]
        self.assertFalse(withdraw(self.account_num1, -50.0))
        self.assertEqual(ACCOUNTS[self.account_num1]["balance"], initial_balance)

    def test_withdraw_zero_amount(self):
        """Test withdrawal with zero amount."""
        initial_balance = ACCOUNTS[self.account_num1]["balance"]
        self.assertFalse(withdraw(self.account_num1, 0.0))
        self.assertEqual(ACCOUNTS[self.account_num1]["balance"], initial_balance)

    def test_withdraw_non_existent_account(self):
        """Test withdrawal from a non-existent account."""
        self.assertFalse(withdraw("000000", 100.0))

    @patch("src.transactions.record_transaction")
    def test_transfer_success(self, mock_record_transaction):
        """Test successful transfer."""
        sender_initial_balance = ACCOUNTS[self.account_num1]["balance"]
        receiver_initial_balance = ACCOUNTS[self.account_num2]["balance"]
        transfer_amount = 200.0

        self.assertTrue(transfer(self.account_num1, self.account_num2, transfer_amount))

        self.assertEqual(
            ACCOUNTS[self.account_num1]["balance"],
            sender_initial_balance - transfer_amount,
        )
        self.assertEqual(
            ACCOUNTS[self.account_num2]["balance"],
            receiver_initial_balance + transfer_amount,
        )

        # Check transaction records for both accounts
        # Mock will capture calls, so we check arg patterns
        # Call 1: sender's 'transfer_sent'
        mock_record_transaction.assert_any_call(
            self.account_num1, "transfer_sent", transfer_amount, self.account_num2
        )
        # Call 2: receiver's 'transfer_received'
        mock_record_transaction.assert_any_call(
            self.account_num2,
            "transfer_received",
            transfer_amount,
            self.account_num1,
        )
        self.assertEqual(mock_record_transaction.call_count, 2)

    def test_transfer_insufficient_funds(self):
        """Test transfer with insufficient funds."""
        sender_initial_balance = ACCOUNTS[self.account_num1]["balance"]
        receiver_initial_balance = ACCOUNTS[self.account_num2]["balance"]

        self.assertFalse(transfer(self.account_num1, self.account_num2, 1500.0))
        self.assertEqual(ACCOUNTS[self.account_num1]["balance"], sender_initial_balance)
        self.assertEqual(
            ACCOUNTS[self.account_num2]["balance"], receiver_initial_balance
        )

    def test_transfer_negative_amount(self):
        """Test transfer with negative amount."""
        sender_initial_balance = ACCOUNTS[self.account_num1]["balance"]
        receiver_initial_balance = ACCOUNTS[self.account_num2]["balance"]

        self.assertFalse(transfer(self.account_num1, self.account_num2, -50.0))
        self.assertEqual(ACCOUNTS[self.account_num1]["balance"], sender_initial_balance)
        self.assertEqual(
            ACCOUNTS[self.account_num2]["balance"], receiver_initial_balance
        )

    def test_transfer_zero_amount(self):
        """Test transfer with zero amount."""
        sender_initial_balance = ACCOUNTS[self.account_num1]["balance"]
        receiver_initial_balance = ACCOUNTS[self.account_num2]["balance"]

        self.assertFalse(transfer(self.account_num1, self.account_num2, 0.0))
        self.assertEqual(ACCOUNTS[self.account_num1]["balance"], sender_initial_balance)
        self.assertEqual(
            ACCOUNTS[self.account_num2]["balance"], receiver_initial_balance
        )

    def test_transfer_same_account(self):
        """Test transfer to the same account."""
        initial_balance = ACCOUNTS[self.account_num1]["balance"]
        self.assertFalse(transfer(self.account_num1, self.account_num1, 100.0))
        self.assertEqual(ACCOUNTS[self.account_num1]["balance"], initial_balance)

    def test_transfer_non_existent_source(self):
        """Test transfer from a non-existent source account."""
        receiver_initial_balance = ACCOUNTS[self.account_num2]["balance"]
        self.assertFalse(transfer("000000", self.account_num2, 100.0))
        self.assertEqual(
            ACCOUNTS[self.account_num2]["balance"], receiver_initial_balance
        )

    def test_transfer_non_existent_target(self):
        """Test transfer to a non-existent target account."""
        sender_initial_balance = ACCOUNTS[self.account_num1]["balance"]
        self.assertFalse(transfer(self.account_num1, "000000", 100.0))
        self.assertEqual(ACCOUNTS[self.account_num1]["balance"], sender_initial_balance)

    def test_get_transaction_history(self):
        """Test retrieving transaction history."""
        history = get_transaction_history(self.account_num1)
        # Initial deposit + transactions from setUp or previous tests
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[0]["type"], "initial_deposit")
        self.assertEqual(history[0]["amount"], 1000.0)

        # Perform a deposit and check history
        deposit(self.account_num1, 50.0)
        history = get_transaction_history(self.account_num1)
        self.assertEqual(history[-1]["type"], "deposit")
        self.assertEqual(history[-1]["amount"], 50.0)

        # Check history for non-existent account
        self.assertEqual(get_transaction_history("999999"), [])


if __name__ == "__main__":
    unittest.main()
