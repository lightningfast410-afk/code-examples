"""47_stdp_demo.py — Spike-timing-dependent plasticity, teaching size.

Demonstrates: the textbook STDP rule — when a presynaptic
spike comes just BEFORE a postsynaptic spike, the connection
strengthens; when it comes just AFTER, it weakens; and the
effect decays as the timing gap grows. Values here are a
simplified teaching choice, not any product's parameters.
Run: python3 47_stdp_demo.py
"""

import math

TAU = 15.0       # decay window (ms), teaching value
A_PLUS = 0.05    # strengthening scale, teaching value
A_MINUS = 0.06   # weakening scale, teaching value


def stdp_update(pre_time, post_time):
    """Weight change for one pre/post spike pair (dt = post - pre)."""
    dt = post_time - pre_time
    if dt > 0:
        return A_PLUS * math.exp(-dt / TAU)   # pre before post: strengthen
    if dt < 0:
        return -A_MINUS * math.exp(dt / TAU)  # pre after post: weaken
    return 0.0


def main():
    causal = stdp_update(0, 10)      # pre 10ms before post
    anti = stdp_update(10, 0)        # pre 10ms after post
    far = stdp_update(0, 100)        # pre far before post
    assert causal > 0 and anti < 0
    assert 0 < far < causal          # distant pairs matter less
    assert abs(causal - A_PLUS * math.exp(-10 / TAU)) < 1e-12
    print(f"PROOF: causal (pre 10ms early) -> +{causal:.4f}")
    print(f"PROOF: anti-causal (pre 10ms late) -> {anti:.4f}")
    print(f"PROOF: distant pair -> +{far:.4f} (decays with gap)")


if __name__ == "__main__":
    main()
