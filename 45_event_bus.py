"""45_event_bus.py — A tiny publish/subscribe event bus.

Demonstrates: decoupling — publishers do not know who listens,
subscribers do not know who publishes. Handlers register per
event type, unsubscribe cleanly, and one handler raising an
error must not stop the others from running.
Run: python3 45_event_bus.py
"""


class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, handler):
        self.subscribers.setdefault(event_type, []).append(handler)
        return lambda: self.subscribers[event_type].remove(handler)

    def publish(self, event_type, payload):
        for handler in list(self.subscribers.get(event_type, [])):
            try:
                handler(payload)
            except Exception:
                continue  # one bad listener never blocks the rest


def main():
    bus = EventBus()
    seen = []
    bus.subscribe("order_placed", lambda p: seen.append(f"email:{p['id']}"))
    bus.subscribe("order_placed", lambda p: seen.append(f"stock:{p['id']}"))
    bus.subscribe("order_placed", lambda p: 1 / 0)  # broken listener
    unsubscribe = bus.subscribe("order_placed", lambda p: seen.append("audit"))
    bus.publish("order_placed", {"id": 7})
    assert seen == ["email:7", "stock:7", "audit"]
    unsubscribe()
    bus.publish("order_placed", {"id": 8})
    assert seen == ["email:7", "stock:7", "audit", "email:8", "stock:8"]
    print(f"PROOF: listeners fired in order, broken one skipped, "
          f"unsubscribed listener stayed silent: {seen}")


if __name__ == "__main__":
    main()
