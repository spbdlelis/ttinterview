import uuid
from src.feed import Feed

class Payment:

    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note
        Feed().notify(self)

    def __str__(self):
        return f"{self.actor} paid {self.target} ${self.amount:.2f} for {self.note}"
