import unittest, tempfile, sqlite3
from pathlib import Path
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from fixtures import transactions as tx
from fixtures.cache import VulnerableCache, CorrectedCache

class Transactions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)/'test.db'
        tx.setup(self.path)
    def count(self, table):
        with closing(sqlite3.connect(self.path)) as db:
            return db.execute('SELECT count(*) FROM '+table).fetchone()[0]
    def test_vulnerable_dual_write(self):
        with self.assertRaises(RuntimeError): tx.vulnerable_order(self.path,'1',True)
        self.assertEqual((self.count('orders'),self.count('outbox')),(1,0))
    def test_corrected_atomic_rollback(self):
        with self.assertRaises(RuntimeError): tx.corrected_order(self.path,'1',True)
        self.assertEqual((self.count('orders'),self.count('outbox')),(0,0))
    def test_corrected_atomic_success(self):
        tx.corrected_order(self.path,'1')
        self.assertEqual((self.count('orders'),self.count('outbox')),(1,1))
    def concurrent(self, handler):
        barrier = Barrier(2, timeout=5)
        def call():
            barrier.wait(); handler(self.path,'event-1')
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(call) for _ in range(2)]
            for f in futures: f.result(timeout=10)
    def test_vulnerable_duplicate(self):
        self.concurrent(tx.vulnerable_consumer)
        self.assertEqual(self.count('effects'),2)
    def test_corrected_duplicate(self):
        self.concurrent(tx.corrected_consumer)
        self.assertEqual(self.count('effects'),1)

class Cache(unittest.TestCase):
    def race(self, cls):
        c=cls(); old=c.read(); c.update(); c.fill(old); return c
    def test_vulnerable_stale_refill(self):
        self.assertEqual(self.race(VulnerableCache).cache,(1,'old'))
    def test_corrected_stale_refill(self):
        c=self.race(CorrectedCache); self.assertIsNone(c.cache); c.fill(c.read()); self.assertEqual(c.cache,(2,'new'))

if __name__=='__main__': unittest.main()
