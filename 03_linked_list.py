"""03_linked_list.py — A singly linked list with insert, delete, reverse.

Demonstrates: pointer-style structure in Python, edge cases
(empty list, deleting the head, deleting a missing value), and
converting back to a plain list for inspection.
Run: python3 03_linked_list.py
"""


class Node:
    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        if self.head is None:
            self.head = Node(value)
            return
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = Node(value)

    def delete(self, value):
        """Remove the first node holding value; return True if removed."""
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            return True
        cur = self.head
        while cur.next is not None and cur.next.value != value:
            cur = cur.next
        if cur.next is None:
            return False
        cur.next = cur.next.next
        return True

    def reverse(self):
        prev, cur = None, self.head
        while cur is not None:
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        self.head = prev

    def to_list(self):
        out, cur = [], self.head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out


def main():
    lst = LinkedList()
    for value in (10, 20, 30):
        lst.append(value)
    assert lst.delete(20) is True
    assert lst.delete(99) is False  # missing value: clean False, no crash
    lst.reverse()
    result = lst.to_list()
    assert result == [30, 10]
    print(f"PROOF: after delete(20) + reverse -> {result}")


if __name__ == "__main__":
    main()
