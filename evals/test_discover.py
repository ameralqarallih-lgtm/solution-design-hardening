import unittest,tempfile,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from discover import discover
class Discovery(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.root=Path(self.tmp.name)
    def write(self,name,content=''):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content); return p
    def test_polyglot(self):
        self.write('a/go.mod','module a\ngo 1.23.2\n'); self.write('b/Cargo.toml'); self.write('c/mix.exs')
        rows=discover(self.root)['signals']; self.assertEqual(len(rows),3); self.assertEqual(rows[0]['declared_toolchain_version'],'1.23.2'); self.assertTrue(all(r['deployed_version'] is None for r in rows))
    def test_declared_not_deployed(self):
        self.write('global.json','{"sdk":{"version":"9.0.100"}}'); self.write('Dockerfile','FROM thing:latest')
        rows=discover(self.root)['signals']; self.assertEqual(rows[1]['declared_toolchain_version'],'9.0.100'); self.assertIsNone(rows[0]['declared_toolchain_version']); self.assertTrue(all(r['capability_status']=='Unknown' for r in rows))
    def test_no_secret_values(self):
        self.write('package.json','{"token":"secret-value"}'); self.write('.env','TOKEN=secret-value'); self.write('global.json','{"sdk":{"version":"https://secret-value"}}')
        out=json.dumps(discover(self.root)); self.assertNotIn('secret-value',out); self.assertNotIn('.env',out)
    def test_skip_generated(self):
        self.write('node_modules/pkg/package.json'); self.write('.git/package.json'); self.write('app/package.json'); self.assertEqual(len(discover(self.root)['signals']),1)
    def test_unknown_stack_not_certified(self):
        self.write('custom.manifest','private engine'); out=discover(self.root); self.assertEqual(out['signals'],[]); self.assertTrue(any('custom' in x for x in out['limitations']))
    def test_malformed_manifest(self):
        self.write('global.json','{ invalid'); self.assertIsNone(discover(self.root)['signals'][0]['declared_toolchain_version'])
    def test_symlink(self):
        target=self.write('target.txt','secret'); link=self.root/'package.json'
        try: link.symlink_to(target)
        except (OSError,NotImplementedError): self.skipTest('symlink unavailable')
        self.assertEqual(discover(self.root)['signals'],[])
