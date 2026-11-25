import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from architecture import inspect
from correlate import analyze, catalog_ids

class ArchitectureDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.root=Path(self.tmp.name)
    def put(self,p,s):
        f=self.root/p; f.parent.mkdir(parents=True,exist_ok=True); f.write_text(s,encoding='utf-8'); return f
    def test_polyglot_local_dependency_and_nested_component(self):
        self.put('api/api.csproj','<Project><ItemGroup><ProjectReference Include="../domain/domain.csproj" /></ItemGroup></Project>')
        self.put('domain/domain.csproj','<Project/>')
        self.put('ui/package.json','{"dependencies":{"local":"file:../shared"}}')
        self.put('shared/package.json','{}')
        self.put('api/worker/pyproject.toml','[project]\nname="worker"')
        self.put('api/worker/handler.py','db.commit()\nbroker.publish(event)\n')
        out=inspect(self.root); ids={c['directory']:c['id'] for c in out['components']}
        self.assertEqual({(e['source'],e['target']) for e in out['declared_dependencies']},{(ids['api'],ids['domain']),(ids['ui'],ids['shared'])})
        self.assertEqual({s['component'] for s in out['boundary_signals']},{ids['api/worker']})
        self.assertTrue(all(s['status']=='Requires Verification' for s in out['boundary_signals']))
        self.assertEqual(out,inspect(self.root))
    def test_boundaries_and_risk_group_are_candidates(self):
        self.put('service/go.mod','module example\ngo 1.23\n')
        self.put('service/handler.py','db.commit()\nbroker.publish(event)\ncheck_permission(user)\nrequests.get(url, timeout=None, verify=False)\ncache.delete(key)\n')
        out=inspect(self.root)
        self.assertEqual({x['kind'] for x in out['boundary_signals']},{'commit','message-publish','authorization','external-call','cache-operation'})
        self.assertEqual(len(out['investigation_groups']),1)
        self.assertEqual(out['investigation_groups'][0]['basis'],'same file only')
        self.assertEqual(set(out['investigation_groups'][0]['problem_ids']),{'SDP-042','SDP-197'})
        self.assertNotIn('root_causes',out)
    def test_no_dependency_from_package_presence(self):
        self.put('a/package.json','{"dependencies":{"remote":"https://example.invalid/private-token"}}')
        self.put('b/package.json','{}')
        out=inspect(self.root); self.assertEqual(out['declared_dependencies'],[])
        self.assertNotIn('private-token',json.dumps(out))
    def test_exclusions_and_raw_reference_redaction(self):
        self.put('app/pyproject.toml','[project]')
        self.put('app/secrets/handler.py','db.commit() # secret-marker')
        self.put('app/.env.py','db.commit() # secret-marker')
        self.put('app/node_modules/generated.py','db.commit()')
        self.put('app/package.json','{"dependencies":{"x":"file:../../private-token"}}')
        self.put('app/handler.py','requests.get(url, verify=False) # secret-marker')
        out=inspect(self.root); raw=json.dumps(out)
        self.assertNotIn('secret-marker',raw); self.assertNotIn('private-token',raw)
        self.assertEqual({s['path'] for s in out['boundary_signals']},{'app/handler.py'})
        self.assertEqual(len(out['unresolved_references']),1)
    def test_symlink_and_oversized_file(self):
        self.put('real.py','db.commit()')
        self.put('oversize.py','x'*(1024*1024+1))
        try: (self.root/'alias.py').symlink_to(self.root/'real.py')
        except OSError: pass
        out=inspect(self.root)
        self.assertEqual([s['path'] for s in out['boundary_signals']],['real.py'])
        self.assertEqual(out['coverage']['skipped']['oversize_or_unreadable'],1)
    def test_incomplete_scan_is_explicit(self):
        self.put('a.py','db.commit()'); self.put('b.py','db.commit()')
        self.assertTrue(inspect(self.root,1)['coverage']['truncated'])
    def test_malformed_and_unresolved_manifest(self):
        self.put('a/package.json','{bad')
        self.put('b/b.csproj','<Project><ItemGroup><ProjectReference Include="../a/not-real.csproj" /></ItemGroup></Project>')
        out=inspect(self.root)
        self.assertTrue(out['coverage']['warnings']); self.assertFalse(out['declared_dependencies']); self.assertEqual(len(out['unresolved_references']),1)

class CorrelationTests(unittest.TestCase):
    def setUp(self): self.model=json.loads((ROOT/'examples/architecture-model.json').read_text()); self.known=catalog_ids()
    def test_supported_relationship_and_dependency_waves(self):
        out=analyze(self.model,self.known)
        self.assertEqual(out['task_waves'],[['REM-1'],['VER-1']]); self.assertEqual(out['unassigned_findings'],[])
        self.assertEqual(out['unknown_trust_flows'],['FLOW-1'])
        self.assertEqual({g['basis'] for g in out['groups']},{'root_causes','invariants'})
        self.assertTrue(all('not independently verified' in g['status'] for g in out['groups']))
    def test_shared_invariant_does_not_imply_root_cause(self):
        self.model['findings'][1]['root_cause_ids']=[]
        out=analyze(self.model,self.known); self.assertEqual([g['basis'] for g in out['groups']],['invariants'])
    def test_unknown_relationship_keeps_uncertainty(self):
        self.model['findings'][1]['status']='unknown'; self.model['findings'][1]['evidence_ids']=[]
        self.model['flows'][0]['transaction_relation']='unknown'
        out=analyze(self.model,self.known)
        self.assertTrue(all('requires verification' in g['status'] for g in out['groups']))
        self.assertEqual(out['unknown_transaction_flows'],['FLOW-1'])
    def test_missing_evidence_rejected(self):
        self.model['findings'][0]['evidence_ids']=[]
        with self.assertRaises(ValueError): analyze(self.model,self.known)
    def test_dangling_links_rejected(self):
        self.model['flows'][0]['target']='CMP-UNKNOWN'
        with self.assertRaises(ValueError): analyze(self.model,self.known)
    def test_cycle_rejected(self):
        self.model['tasks'][0]['depends_on']=['VER-1']
        with self.assertRaisesRegex(ValueError,'cycle'): analyze(self.model,self.known)
    def test_unassigned_finding_reported(self):
        for t in self.model['tasks']: t['finding_ids']=['FND-1']
        self.assertEqual(analyze(self.model,self.known)['unassigned_findings'],['FND-2'])
    def test_invalid_catalog_and_duplicate_ids(self):
        bad=copy.deepcopy(self.model); bad['findings'][0]['problem_ids']=['SDP-999']
        with self.assertRaises(ValueError): analyze(bad,self.known)
        bad=copy.deepcopy(self.model); bad['components'][1]['id']=bad['components'][0]['id']
        with self.assertRaises(ValueError): analyze(bad,self.known)
