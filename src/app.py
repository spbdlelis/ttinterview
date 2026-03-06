from src.exceptions import PaymentException
from src.feed import Feed
from src.user import User

class MiniVenmo:
    def create_user(self, username, balance, credit_card_number):
        created_user = User(username)
        created_user.add_to_balance(balance)
        created_user.add_credit_card(credit_card_number)

        return created_user

    @staticmethod
    def render_feed(user):
        feed = Feed()
        feed.show_feed(user)

        def callback(event):
            if event.actor.username == user.username or event.target.username == user.username:
                print(event)

        feed.subscribe(callback)

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")
        james = venmo.create_user("James", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")

            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")

            james.pay(bobby, 15.00, "Note1")

            # this does not show on bobby's feed
            james.pay(carol, 15.00, "Note2")

            carol.pay(bobby, 15.00, "Note3")
        except PaymentException as e:
            print(e)

        # no need to call retrieve feed here, simply pass the user with this approach of subscriber + feed singleton.
        # the only use for retrieve feed would be to get filtered events regarding of a particular user
        venmo.render_feed(bobby)

        bobby.add_friend(carol)
