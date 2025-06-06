import unittest
from unittest.mock import patch
from src.accounts import (
    ACCOUNTS,
    generate_account_number,
    create_account,
    authenticate_account,
    get_account_details,
    update_account_balance,
)


class TestAccounts(unittest.TestCase):
    def setUp(self):
        """Clears the ACCOUNTS dictionary before each test."""
        ACCOUNTS.clear()

    def test_generate_account_number(self):
        """Test that generated account numbers are unique and 6 digits."""
        numbers = set()
        for _ in range(100):
            num = generate_account_number()
            self.assertEqual(len(num), 6)
            self.assertTrue(num.isdigit())
            self.assertNotIn(num, numbers)
            numbers.add(num)
            # Temporarily add to ACCOUNTS to ensure uniqueness check works
            ACCOUNTS[num] = {"dummy": True}
        ACCOUNTS.clear()  # Clear for other tests

    @patch("src.accounts.generate_account_number", return_value="123456")
    def test_create_account_success(self, mock_generate):
        """Test successful account creation."""
        account_num = create_account("Alice Smith", "1234", 100.0)
        self.assertIsNotNone(account_num)
        self.assertEqual(account_num, "123456")
        self.assertIn("123456", ACCOUNTS)
        self.assertEqual(ACCOUNTS["123456"]["name"], "Alice Smith")
        self.assertEqual(ACCOUNTS["123456"]["pin"], "1234")
        self.assertEqual(ACCOUNTS["123456"]["balance"], 100.0)
        self.assertEqual(len(ACCOUNTS["123456"]["transactions"]), 1)
        self.assertEqual(
            ACCOUNTS["123456"]["transactions"][0]["type"], "initial_deposit"
        )

    def test_create_account_invalid_name(self):
        """Test account creation with empty name."""
        self.assertIsNone(create_account("", "1234", 100.0))
        self.assertEqual(len(ACCOUNTS), 0)

    def test_create_account_invalid_pin(self):
        """Test account creation with invalid PIN."""
        self.assertIsNone(create_account("Bob", "123", 100.0))
        self.assertIsNone(create_account("Bob", "abcd", 100.0))
        self.assertEqual(len(ACCOUNTS), 0)

    def test_create_account_negative_deposit(self):
        """Test account creation with negative initial deposit."""
        self.assertIsNone(create_account("Charlie", "5678", -10.0))
        self.assertEqual(len(ACCOUNTS), 0)

    def test_authenticate_account_success(self):
        """Test successful account authentication."""
        create_account("David", "9999", 500.0)
        test_account_num = list(ACCOUNTS.keys())[0]  # Get the actual generated num
        self.assertEqual(
            authenticate_account(test_account_num, "9999"), test_account_num
        )

    def test_authenticate_account_invalid_number(self):
        """Test authentication with non-existent account number."""
        create_account("Eve", "1111", 200.0)
        self.assertIsNone(authenticate_account("000000", "1111"))

    def test_authenticate_account_invalid_pin(self):
        """Test authentication with incorrect PIN."""
        create_account("Frank", "2222", 300.0)
        test_account_num = list(ACCOUNTS.keys())[0]
        self.assertIsNone(authenticate_account(test_account_num, "wrong"))

    def test_get_account_details_success(self):
        """Test retrieving account details."""
        account_num = create_account("Grace", "3333", 400.0)
        details = get_account_details(account_num)
        self.assertIsNotNone(details)
        self.assertEqual(details["name"], "Grace")
        self.assertEqual(details["balance"], 400.0)

    def test_get_account_details_not_found(self):
        """Test retrieving details for non-existent account."""
        self.assertIsNone(get_account_details("987654"))

    def test_update_account_balance_add(self):
        """Test adding to account balance."""
        account_num = create_account("Heidi", "4444", 100.0)
        self.assertTrue(update_account_balance(account_num, 50.0))
        self.assertEqual(ACCOUNTS[account_num]["balance"], 150.0)

    def test_update_account_balance_deduct(self):
        """Test deducting from account balance."""
        account_num = create_account("Ivan", "5555", 200.0)
        self.assertTrue(update_account_balance(account_num, -75.0))
        self.assertEqual(ACCOUNTS[account_num]["balance"], 125.0)

    def test_update_account_balance_non_existent(self):
        """Test updating balance for non-existent account."""
        self.assertFalse(update_account_balance("000000", 100.0))


if __name__ == "__main__":
    unittest.main()
