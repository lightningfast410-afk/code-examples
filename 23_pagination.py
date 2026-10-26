"""23_pagination.py — Paginate a collection without skipping or repeating.

Demonstrates: cursor-free page math done carefully — page
numbers start at 1, page size is capped, out-of-range pages
return an empty list (not an error), and the caller can walk
every page and recover exactly the original collection.
Run: python3 23_pagination.py
"""


def paginate(items, page, page_size):
    """Return (page_items, total_pages); validates its inputs."""
    if page < 1:
        raise ValueError("page starts at 1")
    if not 1 <= page_size <= 100:
        raise ValueError("page_size must be 1-100")
    total_pages = (len(items) + page_size - 1) // page_size
    start = (page - 1) * page_size
    return items[start:start + page_size], total_pages


def main():
    data = list(range(1, 26))  # 25 items
    page1, total = paginate(data, 1, 10)
    page3, _ = paginate(data, 3, 10)
    beyond, _ = paginate(data, 9, 10)
    assert page1 == list(range(1, 11))
    assert page3 == list(range(21, 26))
    assert beyond == [] and total == 3
    walked = []
    for page in range(1, total + 1):
        walked.extend(paginate(data, page, 10)[0])
    assert walked == data  # walking every page loses and repeats nothing
    try:
        paginate(data, 0, 10)
        raise AssertionError("page 0 should have raised")
    except ValueError:
        pass
    print("PROOF: 25 items in 3 pages of 10; walking all pages recovers all 25")


if __name__ == "__main__":
    main()
