import unittest
from fixtures.security import (seed, read_unscoped, read_scoped, update_unscoped,
    update_scoped, literal_lookup, redeem_once, allow_protected, dispatch_mock)

class SecurityExamples(unittest.TestCase):
    def setUp(self):
        self.db=seed(); self.addCleanup(self.db.close)
    def test_unscoped_read_reproduces_leak(self):
        self.assertEqual(read_unscoped(self.db,'alice',2),('private-b',))
    def test_scoped_read_denies_other_owner_and_allows_own(self):
        self.assertIsNone(read_scoped(self.db,'alice',2))
        self.assertEqual(read_scoped(self.db,'alice',1),('private-a',))
    def test_overbroad_binding_reproduces_role_change(self):
        update_unscoped(self.db,'alice',{'display':'A','role':'admin'})
        self.assertEqual(self.db.execute('SELECT role FROM accounts').fetchone(),('admin',))
    def test_allowlisted_update_preserves_role(self):
        update_scoped(self.db,'alice',{'display':'A','role':'admin'})
        self.assertEqual(self.db.execute('SELECT display,role FROM accounts').fetchone(),('A','reader'))
    def test_parameterized_lookup_treats_quote_as_data(self):
        self.assertEqual(literal_lookup(self.db,"private-a'"),[])
        self.assertEqual(literal_lookup(self.db,'private-a'),[(1,)])
    def test_single_use_recovery_sequential_replay(self):
        self.assertTrue(redeem_once(self.db,'synthetic-one-use'))
        self.assertFalse(redeem_once(self.db,'synthetic-one-use'))
        self.assertFalse(redeem_once(self.db,'missing'))
    def test_policy_failure_denies_protected_effect(self):
        def unavailable(*args): raise TimeoutError('synthetic')
        self.assertFalse(allow_protected(unavailable,'alice','write'))
        self.assertFalse(allow_protected(lambda *args: None,'alice','write'))
        self.assertTrue(allow_protected(lambda *args: True,'alice','write'))
    def test_mock_agent_authority_is_external(self):
        calls=[]
        self.assertFalse(dispatch_mock('delete',{'read'},calls.append,'marker'))
        self.assertEqual(calls,[])
        self.assertTrue(dispatch_mock('read',{'read'},calls.append,'marker'))
        self.assertEqual(calls,['marker'])
