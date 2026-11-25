"""Optional SQL Server lab: explicit EULA acceptance and x86-64 environment required."""
import time, unittest, uuid
from lab import require_lab

def connect():
    require_lab()
    import pymssql
    return pymssql.connect(server='sqlserver',user='sa',password='Sdh_Lab_Only!2026',database='tempdb',login_timeout=5,timeout=10)

class SqlServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        require_lab()
        import pymssql
        deadline=time.monotonic()+150
        while True:
            try:
                with connect() as db:
                    cur=db.cursor(); cur.execute('SELECT CAST(SERVERPROPERTY(\'ProductVersion\') AS varchar(50))'); print('SQL Server:',cur.fetchone()[0],flush=True)
                break
            except pymssql.Error:
                if time.monotonic()>=deadline: raise
                time.sleep(2)
    def transaction(self,commit):
        suffix=uuid.uuid4().hex
        orders='sdh_orders_'+suffix; outbox='sdh_outbox_'+suffix
        with connect() as db:
            cur=db.cursor(); cur.execute(f'CREATE TABLE {orders}(id int PRIMARY KEY)'); cur.execute(f'CREATE TABLE {outbox}(id int PRIMARY KEY)'); db.commit()
            cur.execute(f'INSERT INTO {orders} VALUES (1)'); cur.execute(f'INSERT INTO {outbox} VALUES (1)')
            if commit: db.commit()
            else: db.rollback()
            cur.execute(f'SELECT (SELECT count(*) FROM {orders}), (SELECT count(*) FROM {outbox})'); return cur.fetchone()
    def test_atomic_commit(self): self.assertEqual(self.transaction(True),(1,1))
    def test_atomic_rollback(self): self.assertEqual(self.transaction(False),(0,0))
    def test_rowversion_rejects_lost_update(self):
        table='sdh_version_'+uuid.uuid4().hex
        with connect() as db:
            cur=db.cursor(); cur.execute(f'CREATE TABLE {table}(id int PRIMARY KEY, amount int, rv rowversion)'); cur.execute(f'INSERT INTO {table}(id,amount) VALUES (1,10)'); db.commit()
            cur.execute(f'SELECT rv FROM {table} WHERE id=1'); old=cur.fetchone()[0]; db.commit()
        with connect() as db:
            cur=db.cursor(); cur.execute(f'UPDATE {table} SET amount=20 WHERE id=1'); db.commit()
        with connect() as db:
            cur=db.cursor(); cur.execute(f'UPDATE {table} SET amount=30 WHERE id=1 AND rv=%s',(old,)); self.assertEqual(cur.rowcount,0)
            cur.execute(f'SELECT amount FROM {table} WHERE id=1'); self.assertEqual(cur.fetchone()[0],20)
