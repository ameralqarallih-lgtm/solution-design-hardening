"""Child process used to terminate a real DB connection at precise commit boundaries."""
import os,sys
from lab import pg

def main():
    mode, key = sys.argv[1:]
    if mode not in {'before_commit','after_commit','dual_write'}:
        raise ValueError('invalid fault')
    db=pg()
    db.execute('INSERT INTO orders(id) VALUES (%s)',(key,))
    if mode == 'dual_write':
        db.commit()
        os._exit(73)
    db.execute('INSERT INTO outbox(id) VALUES (%s)',(key,))
    if mode == 'after_commit':
        db.commit()
    os._exit(73)

if __name__=='__main__': main()
