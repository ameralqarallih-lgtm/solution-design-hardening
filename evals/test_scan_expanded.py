import json,tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from scan import scan,RULES

class ScannerCoverage(unittest.TestCase):
    def test_all_rules_have_positive_fixture(self):
        examples={
            'dirty-read':('a.sql','SELECT * FROM t WITH (NOLOCK)'),
            'fanout-map':('a.ts','Promise.all(items.map(run))'),
            'auto-ack':('a.py','channel.basic_consume(auto_ack=True)'),
            'sensitive-log':('a.py','logger.info(password)'),
            'blocking-dotnet':('a.cs','task.GetAwaiter().GetResult()'),
            'unbounded-queue':('a.py','q = asyncio.Queue()'),
            'no-http-timeout':('a.py','requests.get(url, timeout=None)'),
            'unlimited-prefetch':('a.py','channel.basic_qos(prefetch_count=0)'),
            'requeue-always':('a.py','ch.basic_nack(tag, requeue=True)'),
            'process-lock':('a.py','lock = threading.Lock()'),
            'runtime-migration':('a.cs','db.Database.MigrateAsync()'),
            'force-schema-sync':('a.ts','sequelize.sync({force: true})'),
            'floating-image':('a.yaml','image: my-app:latest'),
            'short-termination':('a.yaml','terminationGracePeriodSeconds: 3'),
            'unbounded-metric-label':('a.py','metric.labels(user_id)'),
            'blind-offset-commit':('a.py','enable_auto_commit=True'),
            'tls-verify-disabled':('a.py', 'requests.get(url, verify=False)'),
            'shell-execution':('a.py', 'subprocess.run(args, shell=True)'),
            'native-deserialization':('a.py', 'pickle.loads(data)'),
            'unsafe-html-sink':('a.ts', 'element.innerHTML = value'),
            'privileged-container':('a.yaml', 'privileged: true'),
            'wildcard-cors':('a.cs', 'policy.AllowAnyOrigin()'),
            'debug-enabled':('a.py', 'DEBUG = True'),
            'anonymous-route':('a.cs', '[AllowAnonymous]'),
            'token-validation-setting':('a.py', 'options={"verify_signature": False}'),
            'weak-digest':('a.py', 'hashlib.md5(data)'),
            'infinite-retry':('a.cs','Policy.Handle<Exception>().RetryForever()'),
        }
        self.assertEqual(set(examples),{r[0] for r in RULES})
        for rule,(name,source) in examples.items():
            with self.subTest(rule=rule), tempfile.TemporaryDirectory() as d:
                p=Path(d); (p/name).write_text(source); hits=list(scan(p))
                self.assertIn(rule,{x['rule_id'] for x in hits}); self.assertTrue(all(x['status']=='Requires Verification' for x in hits))
    def test_safe_controls(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'safe.py').write_text('q=asyncio.Queue(maxsize=10)\nchannel.basic_consume(auto_ack=False)\nchannel.basic_qos(prefetch_count=20)\nrequests.get(url, timeout=5)\n')
            (p/'safe_security.py').write_text('requests.get(url, verify=True)\nsubprocess.run(args, shell=False)\njson.loads(data)\nDEBUG = False\nhashlib.sha256(data)\n'); (p/'safe_security.cs').write_text('policy.WithOrigins(allowed);'); (p/'safe_security.yaml').write_text('privileged: false'); (p/'safe.sql').write_text('SELECT * FROM t'); (p/'safe.yaml').write_text('image: app:1.2.3\nterminationGracePeriodSeconds: 30\n'); self.assertEqual(list(scan(p)),[])
    def test_excluded_files_and_no_source_output(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'secrets.yaml').write_text('image: secret-value:latest'); (p/'.hidden.py').write_text('logger.info(password)'); (p/'vendor').mkdir(); (p/'vendor'/'a.py').write_text('logger.info(password)'); (p/'app.py').write_text('logger.info(password + "do-not-emit-123")')
            hits=list(scan(p)); self.assertEqual(len(hits),1); self.assertNotIn('do-not-emit-123',json.dumps(hits)); self.assertEqual(hits[0]['file'],'app.py')
    def test_language_gate(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'app.py').write_text('text = "NOLOCK"'); self.assertEqual(list(scan(p)),[])
