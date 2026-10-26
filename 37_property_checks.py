"""37_property_checks.py — Property-style checks: invariants over many cases.

Demonstrates: the idea behind property-based testing without
a library — state an invariant (a property that must always
hold), then check it over dozens of generated cases instead
of one hand-picked example. Failures print the case that broke.
Run: python3 37_property_checks.py
"""

import random


def check(name, cases, property_fn):
    for case in cases:
        if not property_fn(case):
            raise AssertionError(f"property {name} failed on {case!r}")
    print(f"PROOF: property '{name}' held on {len(cases)} cases")


def main():
    rng = random.Random(42)  # fixed seed: the run is reproducible
    lists = [[rng.randint(0, 99) for _ in range(rng.randint(0, 10))]
             for _ in range(50)]
    check("reverse(reverse(x)) == x", lists,
          lambda xs: list(reversed(list(reversed(xs)))) == xs)
    check("sorted(x) is sorted", lists,
          lambda xs: sorted(xs) == sorted(sorted(xs)))
    check("len(set(x)) <= len(x)", lists,
          lambda xs: len(set(xs)) <= len(xs))
    check("sum(x + y) == sum(x) + sum(y)",
          [(a, b) for a, b in zip(lists[::2], lists[1::2])],
          lambda pair: sum(pair[0] + pair[1]) == sum(pair[0]) + sum(pair[1]))
    print("PROOF: all 4 properties held")


if __name__ == "__main__":
    main()
