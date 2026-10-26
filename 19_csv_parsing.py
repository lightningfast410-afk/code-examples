"""19_csv_parsing.py — Parse CSV defensively: bad rows never kill the run.

Demonstrates: csv.DictReader, type conversion with per-row
error handling, skipping malformed rows while counting them,
and aggregating the good rows. Real-world CSVs always contain
a broken line; a parser must survive it and say so.
Run: python3 19_csv_parsing.py
"""

import csv
import io

SAMPLE = """name,score
alice,90
bob,not-a-number
carol,80
,70
dave,85
"""


def parse(text):
    good, bad = [], 0
    for row in csv.DictReader(io.StringIO(text)):
        try:
            name = row["name"].strip()
            score = int(row["score"])
            if not name:
                raise ValueError("empty name")
        except (ValueError, KeyError, AttributeError):
            bad += 1
            continue
        good.append((name, score))
    return good, bad


def main():
    good, bad = parse(SAMPLE)
    assert good == [("alice", 90), ("carol", 80), ("dave", 85)]
    assert bad == 2  # bob's bad score + the nameless row
    average = sum(score for _, score in good) / len(good)
    assert average == 85.0
    print(f"PROOF: good rows = {good}, bad rows skipped = {bad}")
    print(f"PROOF: average score = {average}")


if __name__ == "__main__":
    main()
