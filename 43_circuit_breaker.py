"""43_circuit_breaker.py — Stop calling a service that keeps failing.

Demonstrates: the circuit breaker pattern with a fake clock —
after N consecutive failures the breaker opens and requests
are rejected without touching the failing service; after a
cooldown, one probe is allowed, and a success closes it again.
Retries alone would keep hammering a dead service.
Run: python3 43_circuit_breaker.py
"""

CLOSED, OPEN, HALF_OPEN = "closed", "open", "half-open"


class CircuitBreaker:
    def __init__(self, failures_to_open=3, cooldown=60):
        self.threshold = failures_to_open
        self.cooldown = cooldown
        self.failures = 0
        self.state = CLOSED
        self.opened_at = None

    def call(self, now, service):
        if self.state == OPEN:
            if now - self.opened_at >= self.cooldown:
                self.state = HALF_OPEN
            else:
                return "rejected (breaker open)"
        try:
            result = service()
        except Exception:
            self.failures += 1
            if self.failures >= self.threshold:
                self.state = OPEN
                self.opened_at = now
            return "failed"
        self.failures = 0
        self.state = CLOSED
        return result


def main():
    breaker = CircuitBreaker(failures_to_open=3, cooldown=60)
    calls = [0]

    def failing():
        calls[0] += 1
        raise RuntimeError("service down")

    outcomes = [breaker.call(t, failing) for t in (0, 1, 2, 3)]
    assert outcomes == ["failed", "failed", "failed", "rejected (breaker open)"]
    assert calls[0] == 3  # the 4th request never touched the service

    def working():
        calls[0] += 1
        return "ok"

    assert breaker.call(70, working) == "ok"  # probe after cooldown closes it
    assert breaker.state == CLOSED
    print(f"PROOF: 3 failures opened the breaker; 4th call rejected, "
          f"service touched {calls[0]} times total (3 fails + 1 probe)")


if __name__ == "__main__":
    main()
