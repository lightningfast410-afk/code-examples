"""17_sqlite_transactions.py — Money moves only inside a transaction.

Demonstrates: ACID by example. A transfer debits one account
and credits another; a CHECK constraint blocks overdrafts and
rolls the whole transfer back, so the total never changes.
A crash mid-transfer without a transaction loses money — the
demo shows the total conserved in every case it controls.
Run: python3 17_sqlite_transactions.py
"""

import sqlite3


def setup():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE accounts (name TEXT PRIMARY KEY, "
               "balance INTEGER CHECK(balance >= 0))")
    db.executemany("INSERT INTO accounts VALUES (?, ?)",
                   [("alice", 100), ("bob", 50)])
    db.commit()
    return db


def total(db):
    return db.execute("SELECT SUM(balance) FROM accounts").fetchone()[0]


def transfer(db, sender, receiver, amount):
    """Atomic transfer; raises and rolls back on overdraft."""
    try:
        db.execute("UPDATE accounts SET balance = balance - ? WHERE name = ?",
                   (amount, sender))
        db.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?",
                   (amount, receiver))
        db.commit()
    except sqlite3.IntegrityError:
        db.rollback()
        raise


def main():
    db = setup()
    assert total(db) == 150
    transfer(db, "alice", "bob", 30)
    assert total(db) == 150
    balances = dict(db.execute("SELECT name, balance FROM accounts").fetchall())
    assert balances == {"alice": 70, "bob": 80}
    try:
        transfer(db, "alice", "bob", 1000)  # overdraft: must fail whole
        raise AssertionError("overdraft should have raised")
    except sqlite3.IntegrityError:
        pass
    assert total(db) == 150  # rollback conserved the total
    print("PROOF: after good transfer alice=70 bob=80 total=150")
    print("PROOF: after failed overdraft total still 150 (rolled back)")


if __name__ == "__main__":
    main()
