"""02_sorting.py — Merge sort and quick sort, verified against sorted().

Demonstrates: two classic divide-and-conquer sorts written as
pure functions (inputs are not mutated), plus a comparison count
so the work each algorithm does is visible.
Run: python3 02_sorting.py
"""


def merge_sort(items):
    """Return a sorted copy; count comparisons via a wrapper list."""
    count = [0]

    def merge(left, right):
        out = []
        i = j = 0
        while i < len(left) and j < len(right):
            count[0] += 1
            if left[i] <= right[j]:
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
        return out + left[i:] + right[j:]

    def sort(seq):
        if len(seq) <= 1:
            return list(seq)
        mid = len(seq) // 2
        return merge(sort(seq[:mid]), sort(seq[mid:]))

    return sort(items), count[0]


def quick_sort(items):
    """Return a sorted copy using a middle pivot."""
    if len(items) <= 1:
        return list(items)
    pivot = items[len(items) // 2]
    left = [x for x in items if x < pivot]
    mid = [x for x in items if x == pivot]
    right = [x for x in items if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


def main():
    data = [31, 7, 42, 3, 19, 58, 12, 24]
    merged, comparisons = merge_sort(data)
    quicked = quick_sort(data)
    assert merged == sorted(data) == quicked
    assert data == [31, 7, 42, 3, 19, 58, 12, 24]  # inputs untouched
    print(f"PROOF: merge_sort -> {merged} ({comparisons} comparisons)")
    print(f"PROOF: quick_sort  -> {quicked}")


if __name__ == "__main__":
    main()
