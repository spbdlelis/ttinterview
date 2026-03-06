import unittest
from unittest.mock import patch

from src.connection import Connection
from src.feed import Feed
from src.payment import Payment
from src.user import User


class TestFeed(unittest.TestCase):
    def setUp(self):
        Feed._instance = None
        self.feed = Feed()

        self.alice = User("alice1")
        self.bob = User("bobby1")
        self.carol = User("carol1")

        self.alice.add_credit_card("4111111111111111")
        self.bob.add_credit_card("4242424242424242")
        self.carol.add_credit_card("4111111111111111")

        self.alice.add_to_balance(100)
        self.bob.add_to_balance(100)
        self.carol.add_to_balance(100)

    def test_payment_creation_publishes_to_feed(self):
        payment = self.alice.pay(self.bob, 15, "Lunch")

        self.assertEqual(len(self.feed._events), 1)
        self.assertIs(self.feed._events[0], payment)
        self.assertIsInstance(payment, Payment)

    def test_add_friend_creation_publishes_connection_to_feed(self):
        connection = self.alice.add_friend(self.bob)

        self.assertEqual(len(self.feed._events), 1)
        self.assertIs(self.feed._events[0], connection)
        self.assertIsInstance(connection, Connection)
        self.assertEqual(str(connection), "alice1 added bobby1 as friends")

    def test_retrieve_feed_returns_only_user_related_events(self):
        self.alice.pay(self.bob, 5, "Coffee")
        self.bob.pay(self.carol, 7, "Snacks")
        self.carol.pay(self.alice, 11, "Gas")

        alice_feed = list(self.alice.retrieve_activity())
        bob_feed = list(self.bob.retrieve_activity())
        carol_feed = list(self.carol.retrieve_activity())

        self.assertEqual(len(alice_feed), 2)
        self.assertEqual(len(bob_feed), 2)
        self.assertEqual(len(carol_feed), 2)
        self.assertTrue(all(e.actor in [self.alice, self.bob, self.carol] for e in alice_feed))

    def test_subscriber_callback_receives_only_events_after_registration(self):
        self.alice.pay(self.bob, 3, "Before subscribe")

        received_events = []
        self.feed.subscribe(received_events.append)

        payment = self.bob.pay(self.carol, 8, "After subscribe")
        connection = self.carol.add_friend(self.alice)

        self.assertEqual(len(received_events), 2)
        self.assertIs(received_events[0], payment)
        self.assertIs(received_events[1], connection)

    def test_show_feed_for_specific_user_prints_filtered_events(self):
        relevant_event = self.alice.pay(self.bob, 5, "Coffee")
        self.carol.pay(self.bob, 7, "Snack")

        with patch("builtins.print") as mock_print:
            self.feed.show_feed(self.alice)

        self.assertEqual(mock_print.call_count, 1)
        self.assertIs(mock_print.call_args_list[0].args[0], relevant_event)

    def test_show_feed_without_user_prints_all_events(self):
        first_event = self.alice.pay(self.bob, 5, "Coffee")
        second_event = self.carol.add_friend(self.alice)

        with patch("builtins.print") as mock_print:
            self.feed.show_feed()

        self.assertEqual(mock_print.call_count, 2)
        self.assertIs(mock_print.call_args_list[0].args[0], first_event)
        self.assertIs(mock_print.call_args_list[1].args[0], second_event)

    def test_payment_str_format(self):
        payment = self.alice.pay(self.bob, 12.5, "Dinner")

        self.assertEqual(str(payment), "alice1 paid bobby1 $12.50 for Dinner")
