"""16_sqlite_crud.py — SQLite create, read, update, delete, done safely.

Demonstrates: an in-memory database, parameterized queries
(the ? placeholder — never string-format values into SQL),
and row access by name. A hostile value is stored as data,
never executed as SQL.
Run: python3 16_sqlite_crud.py
"""

import sqlite3


def main():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    db.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("alice", 30))
    db.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("bob", 25))
    # Hostile input: stored as a name, not run as SQL.
    db.execute("INSERT INTO users (name, age) VALUES (?, ?)",
               ("x'); DROP TABLE users; --", 99))
    db.execute("UPDATE users SET age = ? WHERE name = ?", (31, "alice"))
    db.execute("DELETE FROM users WHERE name = ?", ("bob",))
    rows = db.execute("SELECT name, age FROM users ORDER BY name").fetchall()
    names = [row["name"] for row in rows]
    assert "alice" in names and "bob" not in names
    assert len(names) == 2  # table survived the hostile insert
    alice = db.execute("SELECT age FROM users WHERE name = 'alice'").fetchone()
    assert alice["age"] == 31
    print(f"PROOF: rows after CRUD = {[(r['name'], r['age']) for r in rows]}")
    print("PROOF: hostile input stored as data; table intact")


if __name__ == "__main__":
    main()
