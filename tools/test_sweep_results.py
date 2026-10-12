"""Regression checks for missing measurements and comparison denominators.

Run from the repository: python3 -m unittest discover -s tools -p 'test_sweep_results.py'
"""
import tempfile
import unittest
from pathlib import Path

import sweep_results as results


def run(status='ok', cost=.02, rendered=True, lower_bound=False):
    row = dict.fromkeys(results.FIELDS)
    row.update(runId=status, case='small', configuration='test', label='test',
               status=status, complete=status == 'ok', hasRecord=True, billedUsd=cost,
               uncachedUsd=cost, renderUncachedUsd=None if cost is None else cost * .25,
               checkUncachedUsd=None if cost is None else cost * .75,
               costIsLowerBound=lower_bound, durationSeconds=10 if status == 'ok' else 2,
               technicalRendered=rendered, customerRendered=False,
               technicalCharacters=100 if rendered else None,
               technicalEntries=1 if rendered else None, technicalFlags=1 if rendered else None)
    return row


class SummariesTests(unittest.TestCase):
    def test_incomplete_spend_is_counted_but_excluded_from_complete_median(self):
        cell = results.summarize([run(cost=.02), run('incomplete', .01)])[0]
        self.assertEqual(cell['complete'], 1)
        self.assertEqual(cell['attempts'], 2)
        self.assertEqual(cell['uncachedUsdMedian'], .02)
        self.assertAlmostEqual(cell['billedSpendPerCompleteUsd'], .03)
        self.assertEqual(cell['technicalRenderedRuns'], 2)

    def test_unknown_cost_is_not_zero_or_a_complete_total(self):
        cell = results.summarize([run(), run('failed', None)])[0]
        self.assertIsNone(cell['billedAllAttemptsUsd'])
        self.assertIsNone(cell['billedSpendPerCompleteUsd'])
        self.assertEqual(cell['knownBilledSubtotalUsd'], .02)
        cell = results.summarize([run(cost=None)])[0]
        self.assertIsNone(cell['knownBilledSubtotalUsd'])
        self.assertEqual(cell['knownCostAttempts'], 0)

    def test_zero_complete_runs_has_no_spend_per_complete_value(self):
        cell = results.summarize([run('incomplete', .01)])[0]
        self.assertIsNone(cell['uncachedUsdMedian'])
        self.assertIsNone(cell['billedSpendPerCompleteUsd'])
        self.assertEqual(cell['billedAllAttemptsUsd'], .01)

    def test_lower_bound_is_not_a_known_total(self):
        cell = results.summarize([run(lower_bound=True)])[0]
        self.assertIsNone(cell['billedAllAttemptsUsd'])
        self.assertEqual(cell['lowerBoundAttempts'], 1)

    def test_zero_api_cost_is_a_known_measurement(self):
        cell = results.summarize([run(cost=0)])[0]
        self.assertEqual(cell['billedAllAttemptsUsd'], 0)
        self.assertEqual(cell['billedSpendPerCompleteUsd'], 0)

    def test_phase_means_add_to_mean_total(self):
        cell = results.summarize([run(cost=.02), run(cost=.10)])[0]
        self.assertAlmostEqual(cell['renderUncachedUsdMean'] + cell['checkUncachedUsdMean'], .06)

    def test_missing_target_audience_has_no_zero_length_or_flag_value(self):
        cell = results.summarize([run(rendered=False)])[0]
        self.assertEqual(cell['technicalRenderedRuns'], 0)
        self.assertIsNone(cell['technicalCharactersMedian'])
        self.assertIsNone(cell['technicalFlagsMedian'])


class OverlapTests(unittest.TestCase):
    def test_duplicate_flags_count_once_per_rendered_run_and_pr(self):
        first, second = run(), run('incomplete')
        first['runId'], second['runId'] = 'one', 'two'
        flag = dict(runId='one', case='small', configuration='test', audience='technical', pullRequest=7)
        unknown_pr = dict(flag, pullRequest=None)
        overlap = results.flag_overlap([first, second], [flag, flag, unknown_pr])
        self.assertEqual(len(overlap), 1)
        self.assertEqual(overlap[0]['flaggedRuns'], 1)
        self.assertEqual(overlap[0]['renderedRuns'], 2)

    def test_absent_target_audience_is_excluded_from_overlap_denominator(self):
        first, second = run(), run('incomplete', rendered=False)
        flag = dict(runId=first['runId'], case='small', configuration='test', audience='technical', pullRequest=7)
        self.assertEqual(results.flag_overlap([first, second], [flag])[0]['renderedRuns'], 1)


class ProvenanceTests(unittest.TestCase):
    def test_same_fact_count_does_not_hide_changed_facts(self):
        first = run()
        first.update(toolVersion='v1', promptHash='prompt', factBaseDepth='title-and-description',
                     thoroughCheck=True, factsSha256='original', rangeFromCommit='a', rangeToCommit='b', facts=7)
        second = dict(first, factsSha256='changed')
        with self.assertRaisesRegex(ValueError, 'inconsistent or absent factsSha256'):
            results.provenance_issues([first, second], True, [])

    def test_html_and_svg_escape_untrusted_labels(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'chart.svg'
            svg = results.SVG(300, 200, '<script>', 'A & B')
            svg.text(10, 100, '<img src=x>')
            svg.save(target)
            source = target.read_text()
            self.assertNotIn('<script>', source)
            self.assertIn('&lt;img src=x&gt;', source)


if __name__ == '__main__':
    unittest.main()
