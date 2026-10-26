"""08_recursion.py — Recursion done carefully: base cases first.

Demonstrates: factorial, summing a nested tree, and the Tower
of Hanoi move list for 3 disks. Every recursive function here
names its base case before its recursive case, and the Hanoi
demo proves the move count formula 2^n - 1.
Run: python3 08_recursion.py
"""


def factorial(n):
    if n < 0:
        raise ValueError("factorial is undefined for negatives")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def tree_sum(node):
    """Sum a nested dict tree: {'value': int, 'children': [...]}."""
    total = node["value"]
    for child in node.get("children", []):
        total += tree_sum(child)
    return total


def hanoi(n, source, target, spare, moves):
    if n == 0:
        return
    hanoi(n - 1, source, spare, target, moves)
    moves.append(f"{source} -> {target}")
    hanoi(n - 1, spare, target, source, moves)


def main():
    assert factorial(5) == 120
    tree = {"value": 1, "children": [
        {"value": 2, "children": []},
        {"value": 3, "children": [{"value": 4, "children": []}]},
    ]}
    assert tree_sum(tree) == 10
    moves = []
    hanoi(3, "A", "C", "B", moves)
    assert len(moves) == 2 ** 3 - 1 == 7
    print(f"PROOF: factorial(5) = 120, tree sum = 10, Hanoi(3) = {len(moves)} moves")


if __name__ == "__main__":
    main()
