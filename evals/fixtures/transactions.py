"""Small offline SQLite teaching fixture; no production credentials or services."""
import sqlite3

def setup(path):
    with sqlite3.connect(path) as db:
        db.executescript('CREATE TABLE orders(id TEXT PRIMARY KEY); CREATE TABLE outbox(id TEXT PRIMARY KEY); CREATE TABLE effects(id TEXT); CREATE TABLE inbox(id TEXT PRIMARY KEY);')

def vulnerable_order(path, key, crash=False):
    with sqlite3.connect(path) as db:
        db.execute('INSERT INTO orders VALUES (?)', (key,))
    if crash:
        raise RuntimeError('interrupted after commit')
    with sqlite3.connect(path) as db:
        db.execute('INSERT INTO outbox VALUES (?)', (key,))

def corrected_order(path, key, crash=False):
    with sqlite3.connect(path) as db:
        db.execute('INSERT INTO orders VALUES (?)', (key,))
        if crash:
            raise RuntimeError('interrupted before atomic commit')
        db.execute('INSERT INTO outbox VALUES (?)', (key,))

def vulnerable_consumer(path, key):
    with sqlite3.connect(path) as db:
        db.execute('INSERT INTO effects VALUES (?)', (key,))

def corrected_consumer(path, key):
    with sqlite3.connect(path) as db:
        claim = db.execute('INSERT INTO inbox VALUES (?) ON CONFLICT(id) DO NOTHING', (key,))
        if claim.rowcount == 1:
            db.execute('INSERT INTO effects VALUES (?)', (key,))
