import json
import unittest
from evaluation.main import metrics
from ghostgraph.contract import step,ordered

class EvaluationTests(unittest.TestCase):
    def row(self,steps,status='INCOMPLETE'):
        return dict(case_id='independent',deletion_status=status,steps_json=json.dumps(steps))

    def test_metrics_separate_wrong_evidence_and_state_from_missing(self):
        expected=ordered([step('REPORT_REMAINING_RECORD','service','record_1','evidence_1'),step('DELETE_RECORD','service','record_1')])
        actual=[dict(s) for s in expected];actual[0]['evidence_id']='evidence_2';actual[1]['state']='PRESENT'
        m=metrics([self.row(actual)],[self.row(expected)])
        d=m['mismatches'][0]
        self.assertEqual(d['missing_steps'],[]);self.assertEqual(d['extra_steps'],[])
        self.assertEqual(len(d['wrong_states']),1);self.assertEqual(len(d['wrong_evidence']),1)
        self.assertFalse(d['incorrect_ordering']);self.assertEqual(m['step_f1'],0)

    def test_duplicate_steps_are_counted_and_omissions_are_not_order_errors(self):
        s=step('REPORT_REMAINING_RECORD','service','record_1','evidence_1');s['step_no']=1
        m=metrics([self.row([s,s])],[self.row([s])])
        self.assertEqual(m['step_precision'],.5);self.assertEqual(m['step_recall'],1)
        self.assertAlmostEqual(m['step_f1'],2/3)
        self.assertEqual(len(m['mismatches'][0]['extra_steps']),1)
        second=dict(s,resource_id='record_2',step_no=2)
        m=metrics([self.row([second])],[self.row([s,second])])
        self.assertFalse(m['mismatches'][0]['incorrect_ordering'])

    def test_reordering_and_status_are_distinct(self):
        expected=ordered([step('DELETE_RECORD','service','record_1'),step('DELETE_RECORD','service','record_2')])
        m=metrics([self.row(list(reversed(expected)),'COMPLETE')],[self.row(expected)])
        self.assertTrue(m['mismatches'][0]['incorrect_ordering']);self.assertEqual(m['step_f1'],1)
        self.assertEqual(m['status_accuracy'],0);self.assertEqual(m['exact_sequence_accuracy'],0)

    def test_empty_step_metric_and_duplicate_case_ids(self):
        row=self.row([],'NOT_APPLICABLE');m=metrics([row],[row])
        self.assertIsNone(m['step_f1']);self.assertEqual(m['exact_row_accuracy'],1)
        with self.assertRaises(ValueError):metrics([row,row],[row])

if __name__=='__main__':unittest.main()
