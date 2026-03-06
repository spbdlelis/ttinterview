import re

from src.connection import Connection
from src.exceptions import UsernameException, CreditCardException, PaymentException
from src.feed import Feed
from src.payment import Payment

class User:

    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')

    def __str__(self):
        return self.username

    def retrieve_activity(self):
        return Feed().for_user(self)

    def add_friend(self, new_friend):
        return Connection(new_friend, self)

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException('Invalid credit card number.')

    def _validate_payment(self, target, amount):
        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')
        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')


    def pay(self, target, amount, note):
        if  0 < self.balance < amount:
            remaining_amount = amount - self.balance
            self.pay_with_balance(target, self.balance)
            self.pay_with_card(target, remaining_amount)
        elif self.balance == 0:
            self.pay_with_card(target, amount)
        else:
            self.pay_with_balance(target, amount)

        return Payment(amount, self, target, note)


    def pay_with_card(self, target, amount):
        amount = float(amount)
        self._validate_payment(target, amount)
        if self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')

        self._charge_credit_card(self.credit_card_number)
        target.add_to_balance(amount)


    def pay_with_balance(self, target, amount):
        self._validate_payment(target, amount)

        self.balance -= amount
        target.add_to_balance(amount)

    @staticmethod
    def _is_valid_credit_card(credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    @staticmethod
    def _is_valid_username(username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass
