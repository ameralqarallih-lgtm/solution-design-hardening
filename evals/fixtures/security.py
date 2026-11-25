"""Small local teaching models, not production authentication/authorization code.
No networking, real credentials, shell execution, or external targets.
"""
import sqlite3


def seed():
    db = sqlite3.connect(':memory:')
    db.executescript('''CREATE TABLE records (id INTEGER PRIMARY KEY, owner TEXT, value TEXT);
        INSERT INTO records VALUES (1, 'alice', 'private-a'), (2, 'bob', 'private-b');
        CREATE TABLE accounts (name TEXT PRIMARY KEY, display TEXT, role TEXT);
        INSERT INTO accounts VALUES ('alice', 'Alice', 'reader');
        CREATE TABLE recovery (token TEXT PRIMARY KEY, consumed INTEGER NOT NULL);
        INSERT INTO recovery VALUES ('synthetic-one-use', 0);''')
    return db


def read_unscoped(db, actor, rid):
    return db.execute('SELECT value FROM records WHERE id=?', (rid,)).fetchone()


def read_scoped(db, actor, rid):
    return db.execute('SELECT value FROM records WHERE id=? AND owner=?', (rid, actor)).fetchone()


def update_unscoped(db, actor, fields):
    # Demonstrates overbroad binding; values are still parameterized.
    db.execute('UPDATE accounts SET display=?, role=? WHERE name=?', (fields['display'], fields['role'], actor))


def update_scoped(db, actor, fields):
    db.execute('UPDATE accounts SET display=? WHERE name=?', (fields['display'], actor))


def literal_lookup(db, text):
    return db.execute('SELECT id FROM records WHERE value=?', (text,)).fetchall()


def redeem_once(db, token):
    with db:
        return db.execute('UPDATE recovery SET consumed=1 WHERE token=? AND consumed=0', (token,)).rowcount == 1


def allow_protected(policy, actor, action):
    try:
        return policy(actor, action) is True
    except (TimeoutError, ValueError):
        return False


def dispatch_mock(requested_action, allowed_actions, tool, payload):
    # Authority originates outside model output; mock only.
    if requested_action not in allowed_actions:
        return False
    tool(payload)
    return True
