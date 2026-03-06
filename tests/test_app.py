import unittest
from unittest.mock import MagicMock, patch

from src.exceptions import PaymentException
from src.app import MiniVenmo
from src.feed import Feed


class TestMiniVenmoRenderFeed(unittest.TestCase):
    def setUp(self):
        Feed._instance = None
        self.venmo = MiniVenmo()
        self.alice = self.venmo.create_user("alice1", 50, "4111111111111111")
        self.bob = self.venmo.create_user("bobby1", 50, "4242424242424242")
        self.carol = self.venmo.create_user("carol1", 50, "4111111111111111")

    def test_render_feed_prints_only_user_events_existing_and_post_facto(self):
        first_payment = self.alice.pay(self.bob, 10, "Coffee")
        unrelated_event = self.carol.pay(self.alice, 5, "Snack")

        with patch("builtins.print") as mock_print:
            self.venmo.render_feed(self.bob)

            self.assertEqual(mock_print.call_count, 1)
            self.assertIs(mock_print.call_args_list[0].args[0], first_payment)
            self.assertIsNot(mock_print.call_args_list[0].args[0], unrelated_event)

            new_connection = self.alice.add_friend(self.bob)
            self.assertEqual(mock_print.call_count, 2)
            self.assertIs(mock_print.call_args_list[1].args[0], new_connection)

            self.carol.add_friend(self.alice)
            self.assertEqual(mock_print.call_count, 2)
