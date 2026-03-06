
class Feed:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._events = []
            cls._instance._subscribers = []
        return cls._instance

    def notify(self, event):
        self._events.append(event)
        for callback in self._subscribers:
            callback(event)

    def subscribe(self, callback):
        self._subscribers.append(callback)

    def for_user(self, user):
        return filter(
            lambda event: event.actor.username == user.username or event.target.username == user.username, self._events
        )

    def show_feed(self, user=None):
        if not user:
            for event in self._events:
                print(event)
        else:
            for event in self.for_user(user):
                print(event)

