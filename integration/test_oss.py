"""Real PostgreSQL, Redis and RabbitMQ correctness tests. Not agent evaluations."""
import subprocess, sys, time, unittest, uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from pathlib import Path
from lab import pg, cache, broker, require_lab

FILL = """if redis.call('GET',KEYS[1]) == ARGV[1] then
  redis.call('SET',KEYS[2],ARGV[2]); return 1
end; return 0"""
INVALIDATE = "redis.call('INCR',KEYS[1]); redis.call('DEL',KEYS[2]); return 1"

def concurrent(fn):
    barrier=Barrier(2,timeout=8)
    with ThreadPoolExecutor(max_workers=2) as pool:
        fs=[pool.submit(fn,barrier) for _ in range(2)]
        return [f.result(timeout=20) for f in fs]

class Postgres(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        require_lab()
        with pg() as db:
            print('PostgreSQL:', db.execute('SHOW server_version').fetchone()[0], flush=True)
            db.execute('CREATE TABLE IF NOT EXISTS orders(id text PRIMARY KEY)')
            db.execute('CREATE TABLE IF NOT EXISTS outbox(id text PRIMARY KEY)')
            db.execute('CREATE TABLE IF NOT EXISTS inventory(id text PRIMARY KEY, available int NOT NULL)')
    def fault(self,mode):
        key=uuid.uuid4().hex
        run=subprocess.run([sys.executable,str(Path(__file__).with_name('crash_writer.py')),mode,key],timeout=15)
        self.assertEqual(run.returncode,73,'Child did not reach injected crash boundary')
        with pg() as db:
            return tuple(db.execute('SELECT EXISTS(SELECT 1 FROM '+t+' WHERE id=%s)',(key,)).fetchone()[0] for t in ('orders','outbox'))
    def test_vulnerable_dual_write_crash(self):
        self.assertEqual(self.fault('dual_write'),(True,False))
    def test_atomic_outbox_crash_before_commit(self):
        self.assertEqual(self.fault('before_commit'),(False,False))
    def test_atomic_outbox_crash_after_commit(self):
        self.assertEqual(self.fault('after_commit'),(True,True))
    def reservation(self,safe):
        key=uuid.uuid4().hex
        with pg() as db: db.execute('INSERT INTO inventory VALUES (%s,1)',(key,))
        def worker(barrier):
            with pg() as db:
                count=db.execute('SELECT available FROM inventory WHERE id=%s',(key,)).fetchone()[0]
                barrier.wait()
                if safe:
                    return db.execute('UPDATE inventory SET available=available-1 WHERE id=%s AND available>0',(key,)).rowcount
                if count>0:
                    return db.execute('UPDATE inventory SET available=available-1 WHERE id=%s',(key,)).rowcount
                return 0
        results=concurrent(worker)
        with pg() as db: left=db.execute('SELECT available FROM inventory WHERE id=%s',(key,)).fetchone()[0]
        return sum(results),left
    def test_vulnerable_reservation(self): self.assertEqual(self.reservation(False),(2,-1))
    def test_atomic_reservation(self): self.assertEqual(self.reservation(True),(1,0))

class Redis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        require_lab()
        with cache() as r: print('Redis:',r.info('server')['redis_version'],flush=True)
    def race(self,safe):
        gen,value=[f'sdh:{uuid.uuid4().hex}:{k}' for k in ('generation','value')]
        with cache() as reader, cache() as writer:
            reader.set(gen,1); old_generation=reader.get(gen); old='v1'
            # Deterministic ordering: writer invalidates after reader obtains old value.
            writer.eval(INVALIDATE,2,gen,value)
            if safe: self.assertEqual(reader.eval(FILL,2,gen,value,old_generation,old),0)
            else: reader.set(value,old)
            after=reader.get(value)
            if safe:
                self.assertEqual(reader.eval(FILL,2,gen,value,reader.get(gen),'v2'),1)
                self.assertEqual(reader.get(value),'v2')
            return after
    def test_vulnerable_stale_refill(self): self.assertEqual(self.race(False),'v1')
    def test_generation_rejects_stale_refill(self): self.assertIsNone(self.race(True))

class Messaging(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        require_lab()
        with pg() as db:
            db.execute('CREATE TABLE IF NOT EXISTS inbox(id text PRIMARY KEY)')
            db.execute('CREATE TABLE IF NOT EXISTS effects(id text NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS relay_intent(id text PRIMARY KEY, sent boolean NOT NULL DEFAULT false)')
    def receive(self,ch,queue):
        deadline=time.monotonic()+8
        while time.monotonic()<deadline:
            method,props,body=ch.basic_get(queue,auto_ack=False)
            if method is not None: return method,props,body
            time.sleep(.05) # Poll for broker requeue; not used to order competing transactions.
        self.fail('Expected delivery did not arrive before deadline')
    def queue(self):
        name='sdh-'+uuid.uuid4().hex
        with broker() as b: b.channel().queue_declare(queue=name,durable=True)
        return name
    def publish(self,queue,key):
        import pika
        with broker() as b:
            ch=b.channel(); ch.confirm_delivery()
            ch.basic_publish(exchange='',routing_key=queue,body=key.encode(),mandatory=True,properties=pika.BasicProperties(message_id=key,delivery_mode=2))
    def effect(self,key,safe):
        with pg() as db:
            if safe and db.execute('INSERT INTO inbox VALUES (%s) ON CONFLICT DO NOTHING',(key,)).rowcount==0: return
            db.execute('INSERT INTO effects VALUES (%s)',(key,))
    def replay(self,safe):
        key=uuid.uuid4().hex; q=self.queue(); self.publish(q,key)
        with broker() as b:
            ch=b.channel(); _,props,_=self.receive(ch,q)
            self.effect(props.message_id,safe)
            # Disconnect after DB commit but before broker acknowledgment.
        with broker() as b:
            ch=b.channel(); method,props,_=self.receive(ch,q)
            self.assertTrue(method.redelivered); self.assertEqual(props.message_id,key)
            self.effect(key,safe); ch.basic_ack(method.delivery_tag)
            self.assertIsNone(ch.basic_get(q,auto_ack=False)[0])
        with pg() as db: return db.execute('SELECT count(*) FROM effects WHERE id=%s',(key,)).fetchone()[0]
    def test_vulnerable_duplicate_effect_on_redelivery(self): self.assertEqual(self.replay(False),2)
    def test_inbox_prevents_duplicate_on_redelivery(self): self.assertEqual(self.replay(True),1)
    def test_unroutable_publish_is_not_success(self):
        import pika
        with self.assertRaises(pika.exceptions.UnroutableError): self.publish('missing-'+uuid.uuid4().hex,uuid.uuid4().hex)
    def test_auto_ack_loses_unprocessed_delivery(self):
        q=self.queue(); self.publish(q,uuid.uuid4().hex)
        with broker() as b:
            ch=b.channel(); method,_,_=ch.basic_get(q,auto_ack=True); self.assertIsNotNone(method)
            # No business commit; connection closes after auto-ack.
        with broker() as b: self.assertIsNone(b.channel().basic_get(q,auto_ack=False)[0])
    def test_relay_confirmation_gap_is_duplicate_safe(self):
        key=uuid.uuid4().hex; q=self.queue()
        with pg() as db: db.execute('INSERT INTO relay_intent(id) VALUES (%s)',(key,))
        self.publish(q,key) # Accepted, but relay stops before marking sent.
        with pg() as db:
            self.assertFalse(db.execute('SELECT sent FROM relay_intent WHERE id=%s',(key,)).fetchone()[0])
        self.publish(q,key) # Restarted relay resends same event identity.
        with pg() as db: db.execute('UPDATE relay_intent SET sent=true WHERE id=%s',(key,))
        with broker() as b:
            ch=b.channel()
            for _ in range(2):
                method,props,_=self.receive(ch,q); self.assertEqual(props.message_id,key)
                self.effect(key,True); ch.basic_ack(method.delivery_tag)
            self.assertIsNone(ch.basic_get(q,auto_ack=False)[0])
        with pg() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM effects WHERE id=%s',(key,)).fetchone()[0],1)
            self.assertTrue(db.execute('SELECT sent FROM relay_intent WHERE id=%s',(key,)).fetchone()[0])
