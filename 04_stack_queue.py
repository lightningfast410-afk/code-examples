"""04_stack_queue.py — Stack (LIFO) and queue (FIFO) done the right way.

Demonstrates: a list as a stack, and collections.deque as a
queue. A plain list is a poor queue because popping from the
front is O(n); deque pops from either end in O(1).
Run: python3 04_stack_queue.py
"""

from collections import deque


def main():
    stack = []
    for page in ("home", "search", "article"):
        stack.append(page)  # visit pages
    back = stack.pop()  # browser "back" returns the latest page
    assert back == "article"

    queue = deque()
    for job in ("job-a", "job-b", "job-c"):
        queue.append(job)  # jobs arrive in order
    first = queue.popleft()  # jobs leave in the same order
    assert first == "job-a"
    print(f"PROOF: stack pop -> {back}, queue popleft -> {first}")
    print(f"PROOF: remaining stack {stack}, remaining queue {list(queue)}")


if __name__ == "__main__":
    main()
