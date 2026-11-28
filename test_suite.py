#!/usr/bin/env python3
"""
ChainLex Comprehensive Test Suite

Tests all optimization tools for optimal grip on legal frameworks:
- Framework indexing
- ChainLex API
- Domain helpers
- Framework validation
- Enhanced hypergraph integration
"""

import json
import re
import shutil
import subprocess
import unittest
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from framework_index import FrameworkIndex
from chainlex_api import ChainLex, PrinciplesAPI, RulesAPI, InferenceAPI
from domain_helpers import DomainQueryHelpers
from framework_validator import FrameworkValidator


class TestFrameworkIndex(unittest.TestCase):
    """Test framework indexing functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.index = FrameworkIndex()
    
    def test_framework_loading(self):
        """Test that all frameworks are loaded"""
        self.assertGreater(len(self.index.frameworks), 0, "Should load at least one framework")
        self.assertIn('lv1', self.index.frameworks, "Should load Level 1 principles")
    
    def test_function_indexing(self):
        """Test function indexing"""
        self.assertGreater(len(self.index.function_index), 0, "Should index functions")
        
        # Check that functions have required fields
        for func_name, func_data in list(self.index.function_index.items())[:5]:
            self.assertIn('name', func_data, "Function should have name")
            self.assertIn('framework', func_data, "Function should have framework")
    
    def test_principle_indexing(self):
        """Test principle indexing"""
        self.assertGreater(len(self.index.principle_index), 0, "Should index principles")
    
    def test_search_functions(self):
        """Test function search"""
        results = self.index.search_functions("contract")
        self.assertGreater(len(results), 0, "Should find contract-related functions")
    
    def test_find_principles_by_domain(self):
        """Test finding principles by domain"""
        principles = self.index.find_principles_by_domain("contract")
        self.assertIsInstance(principles, list, "Should return list of principles")
    
    def test_find_derived_rules(self):
        """Test finding derived rules"""
        # This might return empty if no cross-references are set up properly
        derived = self.index.find_derived_rules("pacta-sunt-servanda")
        self.assertIsInstance(derived, list, "Should return list")
    
    def test_get_stats(self):
        """Test statistics generation"""
        stats = self.index.get_framework_stats()
        self.assertIn('total_frameworks', stats, "Stats should include total frameworks")
        self.assertIn('total_functions', stats, "Stats should include total functions")
        self.assertGreater(stats['total_frameworks'], 0, "Should have frameworks")


class TestChainLexAPI(unittest.TestCase):
    """Test ChainLex API functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.api = ChainLex()
    
    def test_initialization(self):
        """Test API initialization"""
        self.assertIsNotNone(self.api.index, "Should have index")
        self.assertIsNotNone(self.api.principles, "Should have principles API")
        self.assertIsNotNone(self.api.rules, "Should have rules API")
        self.assertIsNotNone(self.api.inference, "Should have inference API")
        self.assertIsNotNone(self.api.frameworks, "Should have frameworks API")
    
    def test_universal_search(self):
        """Test universal search"""
        results = self.api.search("contract")
        self.assertIn('principles', results, "Results should include principles")
        self.assertIn('rules', results, "Results should include rules")
    
    def test_principles_api(self):
        """Test principles API"""
        all_principles = self.api.principles.all()
        self.assertIsInstance(all_principles, list, "Should return list")
        
        # Test by domain
        contract_principles = self.api.principles.by_domain("contract")
        self.assertIsInstance(contract_principles, list, "Should return list")
    
    def test_rules_api(self):
        """Test rules API"""
        # Test by framework
        lv1_rules = self.api.rules.by_framework("lv1")
        self.assertIsInstance(lv1_rules, list, "Should return list")
        
        # Test by domain
        contract_rules = self.api.rules.by_domain("contract")
        self.assertIsInstance(contract_rules, list, "Should return list")
    
    def test_frameworks_api(self):
        """Test frameworks API"""
        frameworks = self.api.frameworks.list()
        self.assertGreater(len(frameworks), 0, "Should list frameworks")
        
        stats = self.api.frameworks.stats()
        self.assertIsInstance(stats, dict, "Should return stats dict")
    
    def test_quick_reference(self):
        """Test quick reference generation"""
        ref = self.api.quick_reference()
        self.assertIsInstance(ref, str, "Should return string")
        self.assertIn("ChainLex", ref, "Should mention ChainLex")


class TestDomainHelpers(unittest.TestCase):
    """Test domain-specific query helpers"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.api = ChainLex()
        cls.helpers = DomainQueryHelpers(cls.api)
    
    def test_contract_law(self):
        """Test contract law helpers"""
        info = self.helpers.contract_law()
        self.assertIn('principles', info, "Should include principles")
        self.assertIn('rules', info, "Should include rules")
        self.assertIn('key_concepts', info, "Should include key concepts")
    
    def test_criminal_law(self):
        """Test criminal law helpers"""
        info = self.helpers.criminal_law()
        self.assertIsInstance(info, dict, "Should return dict")
        
        # Test specific helpers
        elements = self.helpers.criminal_elements()
        self.assertIsInstance(elements, list, "Should return list")
    
    def test_labour_law(self):
        """Test labour law helpers"""
        info = self.helpers.labour_law()
        self.assertIsInstance(info, dict, "Should return dict")
        
        dismissal = self.helpers.dismissal_law()
        self.assertIsInstance(dismissal, list, "Should return list")
    
    def test_quick_lookup(self):
        """Test quick topic lookup"""
        contract_info = self.helpers.quick_lookup('contract')
        self.assertIsInstance(contract_info, dict, "Should return dict")
        self.assertNotIn('error', contract_info, "Should not error for valid topic")
        
        invalid_info = self.helpers.quick_lookup('invalid_topic')
        self.assertIn('error', invalid_info, "Should error for invalid topic")


class TestFrameworkValidator(unittest.TestCase):
    """Test framework validation"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.validator = FrameworkValidator()
    
    def test_validation_runs(self):
        """Test that validation runs without errors"""
        results = self.validator.validate_all()
        self.assertIsInstance(results, dict, "Should return results dict")
        self.assertIn('passed', results, "Should indicate pass/fail")
        self.assertIn('errors', results, "Should include errors")
        self.assertIn('warnings', results, "Should include warnings")
    
    def test_framework_structure(self):
        """Test framework structure check"""
        self.validator.check_framework_structure()
        # Should complete without exception
        self.assertTrue(True)
    
    def test_cross_references(self):
        """Test cross-reference check"""
        self.validator.check_cross_references()
        # Should complete without exception
        self.assertTrue(True)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.api = ChainLex()
        cls.helpers = DomainQueryHelpers(cls.api)
    
    def test_search_to_principle_workflow(self):
        """Test workflow: search → find principle → find derived rules"""
        # 1. Search for concept
        results = self.api.search("contract")
        self.assertGreater(len(results['rules']), 0, "Should find rules")
        
        # 2. Get principles
        principles = self.api.principles.by_domain("contract")
        if principles:
            # 3. Find derived rules
            derived = self.api.rules.derived_from(principles[0]['name'])
            self.assertIsInstance(derived, list, "Should return list")
    
    def test_domain_exploration_workflow(self):
        """Test workflow: domain lookup → explore concepts → analyze"""
        # 1. Domain lookup
        labour_info = self.helpers.labour_law()
        self.assertIn('rules', labour_info, "Should have rules")
        
        # 2. Explore specific concept
        dismissal = self.helpers.dismissal_law()
        self.assertIsInstance(dismissal, list, "Should return list")
        
        # 3. Get framework stats
        stats = self.api.stats()
        self.assertIn('domains', stats, "Should have domain stats")
    
    def test_validation_workflow(self):
        """Test workflow: validate → fix → re-validate"""
        validator = FrameworkValidator()
        
        # 1. Initial validation
        results1 = validator.validate_all()
        self.assertIsInstance(results1, dict, "Should return results")
        
        # Note: We can't actually fix issues in tests, but we verify
        # the validation runs consistently
        
        # 2. Re-validate
        validator2 = FrameworkValidator()
        results2 = validator2.validate_all()
        
        # Results should be consistent
        self.assertEqual(
            results1['passed'],
            results2['passed'],
            "Validation results should be consistent"
        )


class TestShippedArtifactParity(unittest.TestCase):
    """Shipped index and hypergraph snapshots must match the Scheme sources"""

    D1_REMOVED = {'benefit-to-accused?', 'actual-benefit-received?', 'potential-benefit?'}

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        base = Path(__file__).parent
        cls.live = {
            code: {f['name'] for f in fw['functions']}
            for code, fw in FrameworkIndex().frameworks.items()
        }
        with open(base / 'framework_index.json', encoding='utf-8') as f:
            cls.shipped_index = json.load(f)
        with open(base / 'hypergraph' / 'tuples.json', encoding='utf-8') as f:
            tuples = json.load(f)
        cls.shipped_criminal_rules = {
            r['name'] for r in tuples['nodes']['rules']
            if r.get('legal_domain') == 'criminal'
        }
        cls.pickle_file = base / 'hypergraph' / 'scmlex_hypergraph.pkl'

    def test_framework_index_matches_sources(self):
        """framework_index.json lists the same functions as the Scheme files"""
        for code, names in self.live.items():
            shipped = {f['name'] for f in self.shipped_index['frameworks'][code]['functions']}
            self.assertEqual(names, shipped, f"framework_index.json is stale for '{code}'")

    def test_tuples_contain_criminal_rules(self):
        """hypergraph/tuples.json covers every criminal-law rule"""
        # extract_tuples.py only recognises names matching [a-z\-\?]+
        extractable = {n for n in self.live['cri'] if re.fullmatch(r'[a-z\-\?]+', n)}
        missing = extractable - self.shipped_criminal_rules
        self.assertFalse(missing, f"tuples.json missing criminal rules: {sorted(missing)}")
        stale = self.D1_REMOVED & self.shipped_criminal_rules
        self.assertFalse(stale, f"tuples.json still has removed rules: {sorted(stale)}")

    def test_hypergraph_pickle_matches_tuples(self):
        """scmlex_hypergraph.pkl carries the same criminal-law rules as tuples.json"""
        try:
            import networkx  # noqa: F401
        except ImportError:
            self.skipTest("networkx not installed")
        import pickle
        with open(self.pickle_file, 'rb') as f:
            graph = pickle.load(f)['graph']
        rules = {
            d.get('name') for _, d in graph.nodes(data=True)
            if d.get('node_type') == 'rule' and d.get('legal_domain') == 'criminal'
        }
        self.assertEqual(rules, self.shipped_criminal_rules)


FRAUD_THEFT_TRUTH_TABLE = r"""
(define (has-attribute act attr) (and (assq attr act) #t))
(define (get-attribute act attr . d)
  (let ((p (assq attr act))) (if p (cdr p) (if (null? d) #f (car d)))))
(primitive-load "cri/za/south_african_criminal_law.scm")
;; Stub only elements this repair did not change; the D1 helpers
;; (misrepresentation?, potential-prejudice?, intention-to-defraud?,
;; claim-of-right?) read the case-fact attributes directly.
(define (flag name) (lambda (act) (has-attribute act name)))
(set! unlawful-act? (flag 'unlawful))
(set! causation? (flag 'causation))
(set! appropriation? (flag 'appropriation))
(set! movable-property? (flag 'movable))
(set! belonging-to-another? (flag 'another))
(set! intention-to-permanently-deprive? (flag 'deprive))
(set! private-defence? (flag 'private-defence))
(set! statutory-authority? (flag 'statutory-authority))
(define (row . attrs) (map (lambda (a) (cons a #t)) attrs))
(define fraud-facts
  '(unlawful false-representation factual-assertion knew-false
    intent-to-deceive intent-to-induce-prejudice))
(define (without x lst) (filter (lambda (a) (not (eq? a x))) lst))
(define (show x) (display (if x "1" "0")))
(show (fraud? (apply row 'risk-of-loss fraud-facts)))
(show (fraud? (apply row 'financial-loss 'causation fraud-facts)))
(show (fraud? (apply row 'financial-loss fraud-facts)))
(show (fraud? (apply row 'risk-of-loss (without 'unlawful fraud-facts))))
(show (fraud? (apply row 'risk-of-loss (without 'intent-to-induce-prejudice fraud-facts))))
(show (fraud? (apply row 'risk-of-loss 'suppressed-truth (without 'factual-assertion fraud-facts))))
(show (fraud? (apply row 'risk-of-loss (without 'false-representation fraud-facts))))
(show (theft? (row 'unlawful 'appropriation 'movable 'another 'deprive)))
(show (theft? (row 'unlawful 'appropriation 'movable 'another 'deprive 'bona-fide-claim-of-right)))
(show (self-defence? (row 'private-defence)))
(show (legal-authority? (row 'statutory-authority)))
"""


@unittest.skipUnless(shutil.which('guile'), "guile not installed")
class TestCriminalRuleSemantics(unittest.TestCase):
    """fraud? and theft? element logic after the Defect D1 repair"""

    def test_fraud_and_theft_truth_table(self):
        result = subprocess.run(
            ['guile', '--no-auto-compile', '-c', FRAUD_THEFT_TRUTH_TABLE],
            cwd=str(Path(__file__).parent), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True, timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        # fraud: potential prejudice; actual loss + causation; actual loss without
        # causation; not unlawful; no intent to induce prejudice; concealment;
        # no false representation. theft: no claim of right; bona fide claim of
        # right. self-defence? and legal-authority? aliases.
        self.assertEqual(result.stdout.strip(), '11000101011')


def run_tests():
    """Run all tests and generate report"""
    print("\n" + "="*70)
    print("ChainLex Optimization Test Suite")
    print("="*70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestFrameworkIndex))
    suite.addTests(loader.loadTestsFromTestCase(TestChainLexAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestDomainHelpers))
    suite.addTests(loader.loadTestsFromTestCase(TestFrameworkValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestShippedArtifactParity))
    suite.addTests(loader.loadTestsFromTestCase(TestCriminalRuleSemantics))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    exit(run_tests())
