import unittest

from src.exceptions import UsernameException, PaymentException, CreditCardException
from src.feed import Feed
from src.user import User
from unittest.mock import patch


class TestUser(unittest.TestCase):
    def setUp(self):
        Feed._instance = None

        self.user_high_amount_starting_balance = 5000
        self.user_low_amount_starting_balance = 0

        self.user_high_amount = User("username1")
        self.user_high_amount.balance = self.user_high_amount_starting_balance
        self.user_high_amount.credit_card_number = "4111111111111111"

        self.user_low_amount = User("username2")
        self.user_low_amount.credit_card_number = "4111111111111111"


    def test_create_user_success(self):

        created_user = User("username3")

        self.assertEqual(created_user.username, "username3")

    def test_create_user_invalid_username_too_long(self):
        with self.assertRaises(UsernameException):
            User("TOOOOOOOOOOLOOOONNNNGUSERNAME")

    def test_create_user_invalid_username_too_short(self):
        with self.assertRaises(UsernameException):
            User("usr")

    def test_create_user_invalid_username_chars(self):
        with self.assertRaises(UsernameException):
            User("%#&¨¨¨¨¨")

    def test_add_to_balance(self):
        self.user_low_amount.add_to_balance(50)

        self.assertEqual(self.user_low_amount.balance, 50)

    def test_add_credit_card_success(self):
        new_user = User("username3")
        new_user.add_credit_card("4111111111111111")

        self.assertEqual(new_user.credit_card_number, "4111111111111111")

    def test_add_credit_card_fail_already_exists(self):
        with self.assertRaises(CreditCardException):
            self.user_high_amount.add_credit_card("4111111111111111")

    def test_add_credit_card_invalid_number(self):
        new_user = User("username3")
        with self.assertRaises(CreditCardException):
            new_user.add_credit_card("11111111111111111")

    def test_pay_with_enough_balance_success(self):
        payment = self.user_high_amount.pay(self.user_low_amount, 50, "payment1")

        self.assertEqual(payment.amount, 50)
        self.assertEqual(self.user_high_amount.balance, self.user_high_amount_starting_balance - 50)
        self.assertEqual(self.user_low_amount.balance, self.user_low_amount_starting_balance + 50)

    @patch.object(User, "_charge_credit_card")
    def test_pay_with_no_balance(self, mock_charge):
        payment = self.user_low_amount.pay(self.user_high_amount, 50, "payment1")

        mock_charge.assert_called()
        self.assertEqual(payment.amount, 50)
        self.assertEqual(self.user_high_amount.balance, self.user_high_amount_starting_balance + 50)
        self.assertEqual(self.user_low_amount.balance, self.user_low_amount_starting_balance)

    @patch.object(User, "_charge_credit_card")
    def test_pay_with_mixed_balance_and_card(self, mock_charge):
        self.user_low_amount.balance = 15
        payment = self.user_low_amount.pay(self.user_high_amount, 50, "payment1")

        mock_charge.assert_called()
        self.assertEqual(payment.amount, 50)
        self.assertEqual(self.user_high_amount.balance, self.user_high_amount_starting_balance + 50)
        self.assertEqual(self.user_low_amount.balance, 0)

    def test_pay_fails_to_themselves(self):
        with self.assertRaises(PaymentException):
            self.user_high_amount.pay(self.user_high_amount, 50, "payment1")

    def test_pay_fails_with_non_positive_amount(self):
        with self.assertRaises(PaymentException):
            self.user_high_amount.pay(self.user_low_amount, 0, "payment1")

    def test_pay_with_card_fails_without_credit_card(self):
        user_without_card = User("username4")

        with self.assertRaises(PaymentException):
            user_without_card.pay_with_card(self.user_low_amount, 10)

    def test_charge_credit_card_noop(self):
        self.assertIsNone(self.user_high_amount._charge_credit_card("4111111111111111"))
