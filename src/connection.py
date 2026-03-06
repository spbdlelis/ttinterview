import uuid
from src.feed import Feed


class Connection:
    def __init__(self, target, actor):
        self.id = str(uuid.uuid4())
        self.target = target
        self.actor = actor
        Feed().notify(self)

    def __str__(self):
        return f"{self.actor} added {self.target} as friends"

